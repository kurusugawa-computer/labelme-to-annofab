# labelme-to-annofab
アノテーションツールLabelMe(やAnyLabeling)のJSONフォーマットをAnnofabのアノテーションフォーマットに変換するツールです。


# 事前準備
VSCode devcontainerを起動して、開発環境を構築してください。

# 使い方

lablemeのlabel'car','bike'であるオブジェクトを、Annofabの塗りつぶしアノテーションに変換します。


```
# LabelMeのアノテーションフォーマットを確認
$ ls ${LABELME_JSON_DIR} -1
image1.json
image2.json


$ cat image1.json
{
    "version": "0.2.23",
    "flags": {},
    "shapes": [
      {
        "label": "car",
        "text": "",
        "points": [
          [
            1918.0,
            528.0
          ],
          [
            1914.0,
            528.0
          ],
          [
            1912.0,
            530.0
          ]
        ],
        "group_id": null,
        "shape_type": "polygon",
        "flags": {}
      },        
      {
        "label": "bike",
        "text": "",
        "points": [
          [
            671.0,
            532.0
          ],
          [
            663.0,
            525.0
          ]
        ],
        "group_id": null,
        "shape_type": "rectangle",
        "flags": {}
      }
    ],
    "imagePath": "image1.jpg",
    "imageData": null,
    "imageHeight": 1080,
    "imageWidth": 1920
  }
```


```
# LabelMeのアノテーションをAnnofabフォーマットに変換
$ poetry run python -m labelmeannofab.convert_annotation_to_segmentation_masks ${LABELME_JSON_DIR} ${ANNOFAB_DIR} --semantic_segmentation_label car bike
```

```
$ ls -1 ${ANNOFAB_DIR}
image1.json
image2.json
image1/
image2/

$ ls -1 ${ANNOFAB_DIR}/image1
672af8c3-8ec5-414e-bcbd-8561602f5461
1738ad90-5cd8-490c-9c28-3aaabfd4fde7
```


```
$ cat out/annofab2/sample_1/image1.json | jq
{
  "details": [
    {
      "label": "car",
      "annotation_id": "672af8c3-8ec5-414e-bcbd-8561602f5461",
      "data": {
        "data_uri": "672af8c3-8ec5-414e-bcbd-8561602f5461",
        "_type": "SegmentationV2"
      },
      "attributes": {}
    },
    {
      "label": "bike",
      "annotation_id": "1738ad90-5cd8-490c-9c28-3aaabfd4fde7",
      "data": {
        "data_uri": "1738ad90-5cd8-490c-9c28-3aaabfd4fde7",
        "_type": "SegmentationV2"
      },
      "attributes": {}
    }
  ]
}
```

## Annofabにアノテーションをインポートする
Annofabのアノテーションフォーマットには、タスクという概念をディレクトリで表す必要があります。
タスクの構成に合わせて、`convert_annotation_to_segmentation_masks`での出力結果を適切に移動してください。
以下のようなイメージです。

```
task1/
  - image1.json
  - image1/
  - image2.json
  - image2/
task2/
  - image3.json
  - image3/
  - image4.json
  - image4/
```

なお、jsonファイルの拡張子を除いた部分がAnnofabの"input_data_id"に相当します。

[annofabcli annotatation import](https://annofab-cli.readthedocs.io/ja/latest/command_reference/annotation/import.html)コマンドを実行して、アノテーションをAnnofabにインポートできます。


```
$ annofab annotation import --project_id ${PROJECT_ID} --annotation ${ANNOFAB_DIR2}
```


