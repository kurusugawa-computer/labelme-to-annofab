import argparse
import json
import logging
import uuid
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw

from labelmeannofab.common.utils import set_logger

logger = logging.getLogger(__name__)


def write_segmentation_masks(labelme_shapes: list[dict[str, Any]], output_png: Path, image_height: int, image_width: int) -> None:
    image = Image.new(mode="RGBA", size=(image_width, image_height), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    for shape in labelme_shapes:
        color = (255, 255, 255, 255)
        points = shape["points"]
        shape_type = shape["shape_type"]
        if shape_type == "polygon":
            xy = [(e[0], e[1]) for e in points]
            draw.polygon(xy, fill=color)
        elif shape_type == "rectangle":
            xy = [([0][0], points[0][1]), (points[1][0], points[1][1])]
            draw.rectangle(xy, fill=color)
        else:
            logger.warning(f"{shape_type=}であるアノテーションはAnnofabのマスク画像に変換できません。 :: lable={shape['label']}")
            continue

    with output_png.open("wb") as f:
        image.save(f, format="PNG")


def convert_annotation_json(labelme_json: Path, output_dir: Path, semantic_segmentation_labels: list[str]) -> None:
    """
    labelmeのアノテーションJSONを、Annofabのフォーマットに変換します。

    """
    with labelme_json.open() as f:
        labelme_annotation = json.load(f)

    shapes = labelme_annotation["shapes"]
    # TODO: slashが含まれていたら、なにかに変換する
    input_data_id = labelme_annotation["imagePath"]
    image_width = labelme_annotation["imageWidth"]
    image_height = labelme_annotation["imageHeight"]

    input_data_dir = output_dir / input_data_id
    input_data_dir.mkdir(exist_ok=True, parents=True)

    annofab_details: list[dict[str, Any]] = []
    for semantic_segmentation_label in semantic_segmentation_labels:
        tmp_shapes = [e for e in shapes if e["label"] == semantic_segmentation_label]

        annotation_id = str(uuid.uuid4())

        annofab_detail = {
            "label": semantic_segmentation_label,
            "annotation_id": annotation_id,
            "data": {"data_uri": annotation_id, "_type": "SegmentationV2"},
        }

        write_segmentation_masks(tmp_shapes, output_png=input_data_dir / annotation_id, image_height=image_height, image_width=image_width)
        annofab_details.append(annofab_detail)

    annofab_annotation: dict[str, Any] = {"details": annofab_details}
    with (output_dir / f"{input_data_id}.json").open("w", encoding="utf-8") as f:
        json.dump(annofab_annotation, f, ensure_ascii=False)


def convert_annotation(input_dir: Path, output_dir: Path, *, semantic_segmentation_labels: list[str]) -> None:
    success_count = 0
    total_count = 0
    logger.info(f"{input_dir}のlabelmeのアノテーションJSONを、Annofabフォーマットに変換して{output_dir}に出力します。")
    for labelme_json in input_dir.glob("*.json"):
        total_count += 1
        try:
            logger.info(f"{labelme_json}のlabelmeのアノテーションJSONを変換します。")
            convert_annotation_json(labelme_json, output_dir, semantic_segmentation_labels)
            success_count += 1
        except Exception:
            logger.warning(f"{labelme_json} の変換に失敗しました。", exc_info=True)
            continue

    logger.info(f"{input_dir}のlabelmeのアノテーションJSONを、{success_count} / {total_count} 件変換しました。")


def main() -> None:
    args = parse_args()
    set_logger()

    convert_annotation(args.input_dir, args.output_dir, semantic_segmentation_labels=args.semantic_segmentation_label)


def parse_args() -> argparse.Namespace:
    parser = ArgumentParser(
        description=(
            "LabelMeのアノテーションJSONをAnnofabのフォーマットに変更します。その際Annofabの塗りつぶしアノテーションに変換します。"
            "shape_typeがrectangle,polygonのアノテーションが変換対象です。"
            "labelmeの'image_path'はAnnofabのinput_data_idに変換します。"
        ),
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("input_dir", type=Path, help="LabelMeのアノテーションJSONが存在するディレクトリ")
    parser.add_argument("output_dir", type=Path, help="Annofabのアノテーションの出力先。")

    # parser.add_argument(
    #     "--json_filename", type=str, nargs="+", required=False, help="`input_dir`に存在するJSONの中で、変換対象のJSONを指定してください。"
    # )
    # TODO: insntance segmentationにも変換できるようにする
    parser.add_argument(
        "--semantic_segmentation_label",
        type=str,
        nargs="+",
        required=True,
        help="AnnofabのSemantic Segmentation用のマスク画像に変換するラベルを指定してください。",
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()
