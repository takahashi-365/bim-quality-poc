# clean_bim_data.py 設計メモ

## 目的

`clean_bim_data.py` は、Revit/BIM由来データを品質チェックや特徴量作成に使いやすい形へ整えるための前処理スクリプトです。

Revitから書き出した集計表TXT/CSVは、そのままでは列名、空欄、不要行、データ型、カテゴリ名などが品質チェック用データとして安定していない可能性があります。

そのため、`clean_bim_data.py` では、Revit由来データをPython/pandasで扱いやすい構造化データに整形し、後続の `check_bim_quality.py`、`calculate_quality_metrics.py`、`create_bim_features.py` に渡せる状態にすることを目的とします。

## 位置づけ

このスクリプトは、PoC全体の中では以下の位置にあります。

```text
Revit集計表TXT / CSV
↓
convert_revit_schedule.py
↓
clean_bim_data.py
↓
check_bim_quality.py
↓
calculate_quality_metrics.py
↓
create_bim_features.py
↓
train_fix_priority_model.py
↓
generate_ai_context.py