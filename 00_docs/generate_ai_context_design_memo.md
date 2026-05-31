# generate_ai_context.py 設計メモ

## 目的

`generate_ai_context.py` は、BIM品質チェック結果、RuleIdルール情報、品質メトリクス、修正優先度などをもとに、生成AIへ渡すための構造化コンテキストを作成するスクリプトです。

従来の「生成AI向けプロンプト生成」では、RuleIdに紐づくルール内容を文章として整理するところまでを行っていました。

今後はそれを発展させ、単なるプロンプト文ではなく、RuleId、違反内容、対象要素、重大度、修正方針、修正優先度、品質スコアなどを整理した **生成AI向け構造化コンテキスト** を作成することを目的とします。

この処理により、生成AIに自由に回答させるのではなく、参照ルールや入力情報を制御したうえで、BIM品質改善に関する説明や修正方針の提示に活用できる構成を目指します。

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
↓
Power BI / Streamlit / 生成AI活用