from pathlib import Path

from labelmeannofab.convert_annotation_to_segmentation_masks import write_segmentation_masks

output_dir = Path("out")
output_dir.mkdir(exist_ok=True, parents=True)

rectangle_shapes = [{"label": "white-knight", "points": [[128.5, 44.0], [168.5, 110.5]], "group_id": None, "shape_type": "rectangle", "flags": {}}]

polygon_shapes = [
    {
        "label": "car",
        "text": "",
        "points": [
            [671.0, 532.0],
            [663.0, 525.0],
            [513.4602076124568, 533.5640138408304],
            [463.28719723183394, 534.9480968858131],
            [452.2145328719723, 537.7162629757785],
            [423.0, 566.0],
            [405.0, 568.0],
            [393.0, 571.0],
            [382.0, 583.0],
            [375.0, 586.0],
            [371.0, 594.0],
            [361.0, 603.0],
            [360.0, 609.0],
            [354.0, 615.0],
            [350.0, 615.0],
            [345.0, 618.0],
            [343.0, 626.0],
            [333.0, 633.0],
            [376.0, 759.0],
            [384.0, 744.0],
            [390.9688581314879, 744.2906574394464],
            [397.8892733564014, 743.9446366782007],
            [435.0, 736.0],
            [436.9896193771626, 741.5224913494809],
            [461.0, 735.0],
            [465.01730103806227, 741.5224913494809],
            [603.0, 708.0],
            [609.0, 708.0],
            [611.0380622837371, 706.9204152249134],
            [614.4982698961937, 717.6470588235294],
            [633.0, 716.0],
            [639.0, 710.0],
            [641.0, 705.0],
            [641.0, 652.0],
            [639.0, 650.0],
            [639.0, 631.0],
            [631.0, 626.0],
            [631.0, 620.0],
            [630.0, 618.0],
            [667.0, 586.0],
            [669.0, 581.0],
            [680.0, 560.0],
            [678.0, 547.0],
        ],
        "group_id": None,
        "shape_type": "polygon",
        "flags": {},
    }
]


def test__write_segmentation_masks():
    write_segmentation_masks(polygon_shapes, output_dir / "segmentation_masks_polygon.png", image_height=1080, image_width=1920)
    write_segmentation_masks(rectangle_shapes, output_dir / "segmentation_masks_rectangle.png", image_height=1080, image_width=1920)
