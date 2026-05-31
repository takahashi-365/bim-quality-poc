# calculate_quality_metrics.py 設計メモ

## 目的

`calculate_quality_metrics.py` は、BIM品質チェック結果CSVをもとに、品質状態を分析・可視化・特徴量作成に使いやすい集計データへ変換するためのスクリプトです。

`check_bim_quality.py` は、BIM要素ごとの違反内容をRuleId付きで出力します。  
一方で、そのままのチェック結果CSVだけでは、全体の品質傾向、カテゴリ別の問題、RuleId別の発生状況、重大度別のリスクを把握しにくい場合があります。

そのため、`calculate_quality_metrics.py` では、品質チェック結果を集計し、品質メトリクスとして整理することを目的とします。

この処理により、Power BI / Streamlitでの可視化、`create_bim_features.py` による特徴量作成、`train_fix_priority_model.py` による簡易機械学習モデルへ接続しやすくします。

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