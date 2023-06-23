# labelme-to-annofab
アノテーションツールLabelMe(やAnyLabeling)のJSONフォーマットをAnnofabのアノテーションフォーマットに変換するツールです。



# sample

lablemeのlabel'car','bike'であるオブジェクトを、Annofabの塗りつぶしアノテーションに変換します。

```
$ poetry run python -m labelmeannofab.convert_annotation_to_segmentation_masks ${LABELME_JSON_DIR} ${ANNOFAB_DIR} --semantic_segmentation_label car bike
```

## TODO
annofab import

