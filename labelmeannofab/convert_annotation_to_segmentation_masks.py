import argparse
import copy
import logging
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw

from labelmeannofab.common.utils import set_logger

logger = logging.getLogger(__name__)


def create_segmentation_masks(labelme_shapes: list[dict[str, Any]], output_png: Path, image_height: int, image_width: int):
    image = Image.new(mode="RGBA", size=(image_width, image_height), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    for shape in labelme_shapes:
        color = (255, 255, 255, 255)
        points = shape["points"]
        if shape["shape_type"] == "polygon":
            xy = [(e[0], e[1]) for e in points]
            draw.polygon(xy, fill=color)
        elif shape["shape_type"] == "rectangle":
            xy = [([0][0], points[0][1]), (points[1][0], points[1][1])]
            draw.rectangle(xy, fill=color)

    with output_png.open("wb") as f:
        image.save(f, format="PNG")


def convert_annotation_json(labelme_json: Path, output_dir: Path, semantic_segmentation_labels: list[str] | None | None = None) -> None:
    """
        labelmeのアノテーションJSONを、Annofabのフォーマットに変換します。

    {
        "details": [
            {
                "label": "car",
                "data": {
                    "left_top": {
                        "x": 878,
                        "y": 566
                    },
                    "right_bottom": {
                        "x": 1065,
                        "y": 701
                    },
                    "_type": "BoundingBox"
                },
                "attributes": {}
            },
            {
                "label": "road",
                "data": {
                    "data_uri": "b803193f-827f-4755-8228-e2c67d0786d9",
                    "_type": "SegmentationV2"
                },
                "attributes": {}
            },
            {
                "label": "weather",
                "data": {
                    "_type": "Classification"
                },
                "attributes": {
                    "sunny": true
                }
            }
        ]
    }

    """
    with labelme_json.open() as f:
        labelme_annotation = json.load(f)

    shapes = labelme_annotation["shapes"]
    for semantic_segmentation_label in semantic_segmentation_labels:
        [e for e in shapes if e["label"] == semantic_segmentation_label]

    dataset = DataSet(str(input_dir))
    _sequence_id_list = sequence_id_list if sequence_id_list is not None else dataset.sequences()

    dataset_accessor = DataSetAccessor(dataset)

    data: list[dict[str, Any]] = []
    for sequence_id in _sequence_id_list:
        logger.debug(f"{sequence_id=} :: cuboidのlabelごとのオブジェクト数を取得します。")

        try:
            cuboid_counts_list = dataset_accessor.get_cuboid_counts_list(sequence_id)
            for cuboid_counts in cuboid_counts_list:
                tmp: dict[str, Any] = copy.deepcopy(cuboid_counts.counts)
                tmp["frame_no"] = cuboid_counts.frame_no
                tmp["sequence_id"] = cuboid_counts.sequence_id
                data.append(tmp)
        except Exception:
            logger.warning(f"{sequence_id=} :: labelごとのオブジェクト数の取得に失敗しました。", exc_info=True)
            continue

    df = pandas.DataFrame(data)
    df = df.fillna(0)
    df = df.set_index(["sequence_id", "frame_no"])

    # columnを辞書順に並び替える
    df = df[sorted(df.columns)]
    return df


def main() -> None:
    args = parse_args()
    set_logger()

    df = create_cuboid_counts_dataframe(args.input_dir, args.sequence_id)
    output_file = args.output
    output_file.parent.mkdir(exist_ok=True, parents=True)
    df.to_csv(str(output_file))


def parse_args() -> argparse.Namespace:
    parser = ArgumentParser(
        description=(
            "LabelMeのアノテーションJSONをAnnofabのフォーマットに変更します。その際Annofabの塗りつぶしアノテーションに変換します。"
            "shape_typeがrectangle,polygonのアノテーションが変換対象です。"
            "labelmeの'image_path'はAnnofabのinput_data_idに変換します。"
        ),
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("input_dir", type=Path, required=True, help="LabelMeのアノテーションJSONが存在するディレクトリ")
    parser.add_argument("output_dir", type=Path, required=True, help="Annofabのアノテーションの出力先。")

    parser.add_argument(
        "--json_filename", type=str, nargs="+", required=False, help="`input_dir`に存在するJSONの中で、変換対象のJSONを指定してください。"
    )

    parser.add_argument(
        "--semantic_segmentation_label",
        type=str,
        nargs="+",
        required=False,
        help="AnnofabのSemantic Segmentation用のマスク画像に変換するラベルを指定してください。",
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()
