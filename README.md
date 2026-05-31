# BIM Data Quality Engineering & AI Analysis PoC

## 管理情報

PoC管理フォルダ：  
`bim_quality_poc`

PoC名：  
`BIM Data Quality Engineering & AI Analysis PoC`

日本語名：  
`BIMデータ品質エンジニアリング・AI分析PoC`

---

## Overview

このPoCは、Revit/BIMデータをPythonで処理し、BIM品質ルールに基づく品質チェック、品質メトリクス作成、特徴量データセット作成、Streamlitによる簡易可視化までを検証する個人開発PoCです。

目的は、建築BIMデータをAI・機械学習・データ分析で扱うために必要となる、データ整形、ルールベース判定、品質評価、品質スコア算出、特徴量設計、修正優先度分類プロトタイプ、生成AI連携前処理までの一連の流れを実装することです。

現時点では、Revitから書き出した集計表TXTをPython/pandasで読み込み、品質チェック用CSVへ変換し、データクレンジング、RuleIdベース品質チェック、品質メトリクス作成、特徴量データセット作成、Streamlit簡易画面での可視化までを実装済みです。

なお、本PoCはAIモデルそのものの精度を追求するものではなく、建築BIMデータをAI・機械学習で扱うために必要な前処理、品質評価、特徴量設計、可視化、機械学習プロトタイプ、生成AI連携前処理までの一連の流れを検証するものです。

---

## Purpose

このPoCの目的は、BIM/Revit導入支援の経験を活かしながら、建築BIMデータをAI・機械学習・データ分析で扱うためのデータ処理パイプラインを設計・実装することです。

単なるBIM品質チェックツールではなく、Revit/BIMデータをPythonで読み込み、データ整形、品質チェック、品質メトリクス作成、特徴量設計、品質スコア算出、Streamlit簡易可視化、機械学習プロトタイプ、生成AI向け構造化コンテキスト生成へつなげる一連の流れを検証します。

特に、以下の点を重視しています。

- PythonによるRevit/BIMデータ処理
- pandasによるデータ読み込み・整形・欠損処理
- RuleIdを用いたBIM品質ルール管理
- ルールベースによるBIMデータ品質チェック
- BIM品質チェック結果のCSV出力
- 品質メトリクス、品質スコア、特徴量データセットの作成
- FixPriority仮ラベルの設計
- Streamlitによる簡易UI化
- Power BIによる補助的な可視化
- RuleId、違反内容、重大度、修正優先度をもとにした生成AI向け構造化コンテキスト生成への拡張
- 将来的なRAG、Azure AI、ローカルLLM、pyRevit、Revit API連携への拡張

---

## Background

BIM導入支援の現場では、Revitモデルそのものを作成するだけでなく、BIMデータをどのように標準化し、品質管理し、分析やAI活用に接続するかが重要になります。

BIMデータに未入力項目、分類コード不足、命名規則違反、属性情報のばらつきがある場合、そのままではBI、機械学習、生成AI、RAGなどに活用しにくくなります。

このPoCでは、BIM導入支援で扱ってきた品質ルールや運用ルールを、Pythonで処理可能なデータとして整理し、BIMデータをAI・機械学習で扱える状態に整えることを目指します。

---

## このPoCで示したいこと

- Revit/BIMデータをPythonで読み込み、構造化データとして処理できる
- Revit集計表TXTをpandasで読み込み、品質チェック用CSVへ変換できる
- BIM品質ルールをRuleIdとして定義し、ルールベース判定を実装できる
- BIM導入支援で扱ってきた品質ルールや運用ルールを、Pythonで処理可能なデータとして整理できる
- pandasを用いてデータの読み込み、欠損判定、分類、集計ができる
- BIM品質チェック結果をRuleId、重大度、修正ガイド付きのCSVとして出力できる
- BIM品質チェック結果から、品質メトリクスや分析用データを作成できる
- 要素ごとの違反数、未入力項目数、重大度スコア、品質スコアなどの特徴量を設計できる
- BIM品質チェック結果を、機械学習や分析に利用できる特徴量データセットへ変換できる
- 修正優先度 High / Medium / Low の仮ラベルを設計し、修正優先度分類プロトタイプへ拡張できる
- Streamlitで、品質指標、違反傾向、品質スコア、特徴量データセットを可視化できる
- Power BIを補助的な可視化手段として使える
- 生成AIに自由回答させるのではなく、RuleIdや入力情報を制御したAI活用設計へ拡張できる
- 将来的なRAG、Azure AI、ローカルLLM、pyRevit、Revit API連携に拡張できる設計にする

---

## Current Status

現時点では、7月応募可能MVPとして、以下の処理フローを実装済みです。

```text
Revit書き出しTXT
↓
convert_revit_schedule.py で品質チェック用CSVへ変換
↓
door_schedule_converted_v002.csv
↓
clean_bim_data.py でクレンジング
↓
cleaned_bim_data_v001.csv
↓
check_bim_quality.py でRuleIdベース品質チェック
↓
check_results_revit_v002.csv
↓
calculate_quality_metrics.py で品質メトリクス作成
↓
quality_metrics_v001.csv
rule_summary_v001.csv
category_summary_v001.csv
element_summary_v001.csv
↓
create_bim_features.py で特徴量データセット作成
↓
bim_features_v001.csv
↓
streamlit_app.py で簡易可視化
```

この構成により、Revit/BIM由来のデータをPythonで前処理し、品質チェック、品質メトリクス、特徴量データセット、簡易UI表示へ接続する流れを構築しています。

なお、現時点のRevit由来データ対応は初期試作であり、列マッピングは一部仮設定です。今後、Revit集計表の各列の意味を確認し、正式な列マッピングを整理します。

---

## Data Source

Autodesk日本仕様 意匠サンプルモデル Revit 2024を検証用データとして使用します。

実案件データ・社外秘データは使用しません。

このPoCは、転職活動用ポートフォリオとして説明しやすいように、公開可能なサンプルデータを前提に構成しています。

---

## Target Categories

初期PoCでは、対象カテゴリを以下の3つに限定します。

- 壁 / Walls
- ドア / Doors
- 部屋 / Rooms

現時点でRevit由来データとして実処理しているのは、ドア建具表の書き出しTXTです。

---

## Existing Schedule Export Check

確認済み集計表は以下です。

- 20 ドア 建具表 SD  
  出力ファイル：`03_input_csv/door_schedule_SD_export_test_v001.txt`

- 04 材料表 作業用  
  出力ファイル：`03_input_csv/material_schedule_export_test_v001.txt`

- 05 部屋 仕上表  
  出力ファイル：`03_input_csv/room_finish_schedule_export_test_v001.txt`

上記3ファイルは、Revitからタブ区切りテキストとして書き出し、Excelで開けることを確認済みです。

現時点では、ドア建具表TXTを対象に、Pythonでの変換、クレンジング、品質チェック、メトリクス作成、特徴量データセット作成まで実装しています。

---

## Out of Scope

初期PoCでは、以下は対象外とします。

- 床
- 天井
- 窓
- 家具
- 設備
- 構造
- 外構
- Revit APIによる直接操作
- Revitモデルの自動修正
- 設計判断、施工判断、モデル修正の自動化

---

## Tech Stack

現時点で使用している技術は以下です。

- Python 3.12.10
- pandas 2.3.3
- pytest 9.0.3
- Streamlit 1.52.1
- CSV / TXT
- Revit Schedule Export
- Power BI Desktop
- Markdown
- RuleId-based Quality Check

今後追加予定の技術は以下です。

- scikit-learn
- JSON / Markdown Context Generation
- RAG
- Azure AI
- pyRevit
- Revit API

---

## Setup

PowerShellで、`bim_quality_poc` フォルダへ移動します。

```powershell
cd path\to\bim_quality_poc
```

`requirements.txt` を使用して、必要なライブラリをインストールします。

```powershell
python -m pip install -r requirements.txt
```

pandas のバージョンを確認します。

```powershell
python -c "import pandas as pd; print(pd.__version__)"
```

Streamlit の起動確認は以下で行います。

```powershell
streamlit run .\app\streamlit_app.py
```

---

## requirements.txt

配置場所：

```text
bim_quality_poc/requirements.txt
```

現時点の記載内容：

```text
pandas>=2.2,<3
pytest==9.0.3
streamlit==1.52.1
```

目的は、Python品質チェックツール、テスト、Streamlit簡易画面の実行に必要な外部ライブラリを明示し、別環境でも再現しやすくすることです。

Streamlit 1.52.1 は pandas 3系に対応していないため、pandas は以下の範囲指定としています。

```text
pandas>=2.2,<3
```

---

## Folder Structure

```text
bim_quality_poc/
├── README.md
├── requirements.txt
├── app/
│   └── streamlit_app.py
├── 01_revit_model/
│   └── README.md
├── 02_rule_master/
│   ├── bim_rule_master_v001.csv
│   └── bim_rule_master_v002.csv
├── 03_input_csv/
│   ├── sample_bim_data_v001.csv
│   ├── door_schedule_SD_export_test_v001.txt
│   ├── material_schedule_export_test_v001.txt
│   ├── room_finish_schedule_export_test_v001.txt
│   ├── door_schedule_converted_v001.csv
│   ├── door_schedule_converted_v002.csv
│   └── cleaned_bim_data_v001.csv
├── 04_output_csv/
│   ├── check_results_v001.csv
│   ├── check_results_revit_v001.csv
│   ├── check_results_revit_v002.csv
│   ├── quality_metrics_v001.csv
│   ├── rule_summary_v001.csv
│   ├── category_summary_v001.csv
│   ├── element_summary_v001.csv
│   └── bim_features_v001.csv
├── 05_powerbi/
│   └── README.md
├── 06_ai_demo/
│   ├── ruleid_lookup_demo.py
│   ├── ruleid_prompt_generator_demo.py
│   └── generated_prompts/
├── 07_portfolio/
│   ├── portfolio_outline_v001.md
│   └── screenshots/
├── 08_python/
│   ├── check_bim_quality_v001.py
│   ├── check_bim_quality.py
│   ├── test_read_revit_txt.py
│   ├── convert_revit_schedule_v001.py
│   └── convert_revit_schedule.py
├── 00_docs/
│   ├── python_code_explanation_memo.md
│   ├── create_bim_features_concept_memo.md
│   ├── fix_priority_model_design_memo.md
│   ├── clean_bim_data_design_memo.md
│   ├── calculate_quality_metrics_design_memo.md
│   └── generate_ai_context_design_memo.md
├── docs/
│   ├── system_overview.md
│   ├── portfolio_summary.md
│   ├── may_deliverables_260524.md
│   ├── next_steps_260524.md
│   ├── data_dictionary.md
│   ├── rule_specification.md
│   ├── limitations.md
│   ├── business_requirements_mapping.md
│   ├── evaluation_policy.md
│   └── streamlit_app_design.md
├── tests/
│   └── test_quality_rules.py
└── src/
    ├── clean_bim_data.py
    ├── calculate_quality_metrics.py
    ├── create_bim_features.py
    ├── convert_revit_schedule.py
    ├── check_bim_quality.py
    ├── train_fix_priority_model.py
    ├── generate_ai_context.py
    └── utils.py
```
※ `.rvt` ファイルおよび `.pbix` ファイル本体は、容量・配布条件を考慮し、GitHub公開対象外としています。

---

## Folder Role

現時点の各フォルダの役割は以下です。

```text
08_python/：5月〜6月前半のPython試作・検証コード
06_ai_demo/：RuleId検索・生成AI向け説明生成デモ
src/：今後の本実装用コード
app/：Streamlit簡易画面
docs/：設計資料・ポートフォリオ説明資料
00_docs/：5月時点の設計メモ・コード説明メモ
tests/：RuleIdベース品質チェックの最小テスト
05_powerbi/：補助的な可視化成果物
07_portfolio/：ポートフォリオPDF・説明資料・スクリーンショット素材
```

今後は、`08_python` で検証した処理を必要に応じて `src` に移行し、再利用しやすい本実装コードとして整理します。

---

## RuleId-based Quality Check

### RuleIdルールマスタ

ファイル名：

```text
02_rule_master/bim_rule_master_v002.csv
```

目的：

Python品質チェック、品質メトリクス作成、特徴量データセット作成、Streamlit簡易画面、RuleId検索デモ、生成AI向け構造化コンテキスト生成で共通して使用するチェックルールIDを定義します。

初期ルール：

- R-001：必須パラメータ未入力
- R-002：分類コード未入力
- R-003：ファミリ命名規則違反

v002では、v001に含まれていた不要な空行を削除し、3行 × 10列のルールマスタとして整理しています。

ルール数を増やすことよりも、RuleIdを共通キーとして、Pythonチェック結果、補助的な可視化、RuleId検索、生成AI向け構造化コンテキスト生成を接続することを重視します。

---

## Revit Schedule TXT Conversion

作成ファイル：

```text
08_python/convert_revit_schedule.py
```

入力TXT：

```text
03_input_csv/door_schedule_SD_export_test_v001.txt
```

変換後CSV：

```text
03_input_csv/door_schedule_converted_v002.csv
```

目的：

Revitから書き出した集計表TXTをPython/pandasで読み込み、品質チェック用CSVへ変換します。

v0.2では、元TXTの先頭非データ行を除外し、`ElementId` が空欄の行を除外する処理を追加しています。

実行コマンド：

```powershell
python .\08_python\convert_revit_schedule.py
```

実行結果：

```text
Raw data shape: (26, 33)
Removed non-data rows: 1
Converted data shape: (25, 10)
```

注意点：

現時点の列マッピングは仮設定です。

- `ElementId` はRevit内部ElementIdではなく、建具表上の建具番号を仮IDとして使用しています。
- `FamilyName` はRevitファミリ名ではなく、建具表上の種別記号 `SD` を仮格納しています。
- `TypeName` はRevitタイプ名ではなく、設置場所・室名に近い列を仮格納しています。

---

## Data Cleaning

作成ファイル：

```text
src/clean_bim_data.py
```

入力CSV：

```text
03_input_csv/door_schedule_converted_v002.csv
```

出力CSV：

```text
03_input_csv/cleaned_bim_data_v001.csv
```

目的：

変換後CSVを、品質チェックや特徴量設計に使いやすい形へ整えます。

主な処理：

- 必要列の確認
- 不足列がある場合の空列追加
- 列順の標準化
- NaNの空文字化
- 文字列の前後スペース削除
- `ElementId` 空欄行の除外
- 完全一致の重複行の除外

実行コマンド：

```powershell
python .\src\clean_bim_data.py
```

実行結果：

```text
Input data shape: (25, 10)
Removed rows with blank ElementId: 0
Removed duplicate rows: 0
Cleaned data shape: (25, 10)
```

---

## Quality Check

作成ファイル：

```text
08_python/check_bim_quality.py
```

入力CSV：

```text
03_input_csv/cleaned_bim_data_v001.csv
```

ルールマスタ：

```text
02_rule_master/bim_rule_master_v002.csv
```

出力CSV：

```text
04_output_csv/check_results_revit_v002.csv
```

目的：

クレンジング済みのRevit由来CSVを入力し、RuleIdベース品質チェックを実行します。

実行コマンド：

```powershell
python .\08_python\check_bim_quality.py
```

実行結果：

```text
Input data shape: (25, 10)
Rule master shape: (3, 10)
Check completed. Results: 100 issues found.
```

RuleId別内訳：

- R-001：50件
- R-002：25件
- R-003：25件

5月版では26行を対象に104件でしたが、6月v0.2では先頭の非データ行を除外し、25行を対象に100件の違反として出力しています。

---

## Quality Metrics

作成ファイル：

```text
src/calculate_quality_metrics.py
```

入力CSV：

```text
04_output_csv/check_results_revit_v002.csv
```

出力CSV：

```text
04_output_csv/quality_metrics_v001.csv
04_output_csv/rule_summary_v001.csv
04_output_csv/category_summary_v001.csv
04_output_csv/element_summary_v001.csv
```

目的：

品質チェック結果CSVを読み込み、分析・可視化・特徴量作成に使いやすい品質メトリクスへ変換します。

主な処理：

- 総違反件数の集計
- RuleId別違反件数の集計
- Severity別違反件数の集計
- Category別違反件数の集計
- ElementId別違反件数の集計
- SeverityScoreの算出
- QualityScoreの算出

実行コマンド：

```powershell
python .\src\calculate_quality_metrics.py
```

実行結果：

```text
Input data shape: (100, 16)
Rule summary shape: (3, 4)
Category summary shape: (1, 2)
Element summary shape: (25, 9)
Quality metrics shape: (10, 3)
```

---

## Feature Engineering

作成ファイル：

```text
src/create_bim_features.py
```

入力CSV：

```text
04_output_csv/check_results_revit_v002.csv
04_output_csv/element_summary_v001.csv
```

出力CSV：

```text
04_output_csv/bim_features_v001.csv
```

目的：

BIM品質チェック結果CSVとElementId別集計CSVを読み込み、機械学習や分析に使える特徴量データセットを作成します。

作成する主な特徴量：

- RuleViolationCount
- MissingFieldCount
- HighViolationCount
- MediumViolationCount
- LowViolationCount
- HasClassificationCode
- FamilyNameValid
- SeverityScore
- QualityScore
- FixPriority

実行コマンド：

```powershell
python .\src\create_bim_features.py
```

実行結果：

```text
Check results shape: (100, 16)
Element summary shape: (25, 9)
Features shape: (25, 16)
FixPriority:
High 25
```

現時点では、`FixPriority` は実務の正解ラベルではなく、QualityScoreとHigh違反件数をもとにした仮ラベルです。

---

## QualityScore

本PoCでは、BIM品質チェック結果をもとに、要素ごとの簡易品質スコアである `QualityScore` を作成しています。

初期設計では、100点を初期値とし、検出された違反の重大度に応じて減点します。

| Severity | 減点 |
|---|---:|
| High | 10点 |
| Medium | 5点 |
| Low | 1点 |

計算式：

```text
QualityScore = 100 - SeverityScore
```

今回の初期データでは、各要素に `High` 違反が3件、`Medium` 違反が1件発生しているため、1要素あたりの減点は以下となります。

```text
High 3件 × 10点 = 30点
Medium 1件 × 5点 = 5点
合計減点 = 35点
QualityScore = 100 - 35 = 65点
```

このスコアは、現時点では正確な実務評価ではなく、品質チェック結果を数値化し、特徴量設計やStreamlit表示へ接続するための簡易スコアとして扱います。

---

## Streamlit App

作成ファイル：

```text
app/streamlit_app.py
```

目的：

BIM品質チェック結果、品質メトリクス、特徴量データセットを画面で確認できる簡易UIを作成します。

実行コマンド：

```powershell
streamlit run .\app\streamlit_app.py
```

表示内容：

- 品質メトリクス概要
- RuleId別違反件数
- Category別違反件数
- ElementId別品質スコア
- 特徴量データセット
- FixPriority件数
- 品質チェック結果一覧
- RuleId / Severity / Category フィルタ
- CSVダウンロード
- 現時点の注意点

この画面は、本格的な業務アプリではなく、面接・ポートフォリオ説明用のMVPとして位置づけます。

---

## Visualization

### Streamlit

Streamlitは、7月応募可能MVPの主な簡易UIとして位置づけます。

Pythonで作成した品質チェック結果、品質メトリクス、特徴量データセットを画面で確認できるようにしています。

### Power BI

Power BIは、Pythonで処理したBIM品質データの分析結果を確認するための補助的な可視化手段として使用します。

作成ファイル：

```text
05_powerbi/bim_quality_dashboard_v001.pbix
```

入力データ：

```text
04_output_csv/check_results_v001.csv
```

作成した可視化：

- 総違反件数カード
- RuleId別違反件数
- Severity別違反件数
- Category別違反件数
- 違反一覧テーブル

初期版では1ページ構成とし、複雑なDAXや複数ページ構成は行いません。

---

## RuleId Lookup Demo

作成ファイル：

```text
06_ai_demo/ruleid_lookup_demo.py
```

参照データ：

```text
02_rule_master/bim_rule_master_v001.csv
```

目的：

Power BIなどで確認したRuleIdをもとに、該当するBIM品質ルールの内容、重大度、業務影響、AI活用時の影響、修正方針を確認できるようにします。

実行コマンド：

```powershell
python .\06_ai_demo\ruleid_lookup_demo.py
```

確認できる内容：

- RuleId
- RuleName
- Category
- Severity
- TargetField
- CheckLogic
- BusinessImpact
- AIUseImpact
- FixGuide
- Reference

将来的には、検索したルール内容を生成AI向け構造化コンテキストへ接続します。

---

## RuleId-based AI Context Generation Demo

作成ファイル：

```text
06_ai_demo/ruleid_prompt_generator_demo.py
```

参照データ：

```text
02_rule_master/bim_rule_master_v001.csv
```

出力先：

```text
06_ai_demo/generated_prompts
```

目的：

RuleIdをキーにルールマスタから該当ルールを取得し、生成AIへ渡す情報を制御するための初期デモです。

現時点では、OpenAI APIなどを直接呼び出すのではなく、生成AIに渡すためのプロンプト文を作成するところまでを検証しています。

今後は、RuleId、違反内容、重大度、品質スコア、修正優先度を含む、生成AI向け構造化コンテキスト生成へ発展させます。

---

## Tests

作成ファイル：

```text
tests/test_quality_rules.py
```

目的：

RuleIdベース品質チェックの基本動作をpytestで確認します。

確認した内容：

- R-001：必須パラメータ未入力を検出できるか
- R-002：分類コード未入力を検出できるか
- R-003：ファミリ命名規則違反を検出できるか
- 正常なファミリ名の場合、違反なしとして扱えるか
- 1要素に複数の違反がある場合、想定どおり検出できるか

実行コマンド：

```powershell
python -m pytest tests/test_quality_rules.py -v
```

実行結果：

```text
collected 5 items
5 passed
```

現時点では、`tests/test_quality_rules.py` は本実装関数を直接テストするものではなく、RuleIdベース品質チェックの期待動作を固定するための最小テストとして位置づけます。

今後、`src/check_bim_quality.py` へ本実装を移行した後、このテストを本実装関数に接続します。

---

## Output Files

現時点で出力・確認済みの主なファイルは以下です。

```text
03_input_csv/door_schedule_converted_v002.csv
03_input_csv/cleaned_bim_data_v001.csv
04_output_csv/check_results_revit_v002.csv
04_output_csv/quality_metrics_v001.csv
04_output_csv/rule_summary_v001.csv
04_output_csv/category_summary_v001.csv
04_output_csv/element_summary_v001.csv
04_output_csv/bim_features_v001.csv
06_ai_demo/generated_prompts/prompt_R-001_20260517_172551.txt
06_ai_demo/generated_prompts/prompt_R-002_20260517_172615.txt
06_ai_demo/generated_prompts/prompt_R-003_20260517_172644.txt
05_powerbi/bim_quality_dashboard_v001.pbix
```

---

## Current Deliverables

7月応募可能MVP時点での主な成果は以下です。

- Revitサンプルモデルを使った検証環境の準備
- Revit集計表TXTの書き出し確認
- 検証用サンプルCSVの作成
- RuleIdルールマスタ初版・整理版の作成
- Python品質チェックツール初期版・v0.2版の作成
- Revit書き出しTXTのPython/pandas読み込み確認
- Revit書き出しTXTから品質チェック用CSVへの変換
- Revit由来CSVのクレンジング
- RuleIdベース品質チェックの実行
- RuleId付きチェック結果CSVの出力
- 品質メトリクスCSVの作成
- RuleId別、Category別、ElementId別集計CSVの作成
- QualityScoreの算出
- 特徴量データセットの作成
- FixPriority仮ラベルの作成
- Streamlit簡易画面の作成
- pytestによる最小テスト
- Power BIによる補助的な可視化
- RuleId検索デモの作成
- RuleIdベース生成AI向け構造化コンテキスト生成の前段階となるプロンプト生成デモの作成
- system_overview.md の更新
- portfolio_summary.md の作成
- data_dictionary.md の作成
- rule_specification.md の作成
- limitations.md の作成
- business_requirements_mapping.md の作成
- evaluation_policy.md の作成
- streamlit_app_design.md の作成

---

## Limitations

現時点の制約と注意点は以下です。

- Revit由来データ対応は初期試作です。
- `door_schedule_converted_v002.csv` の列マッピングは仮設定です。
- `ElementId` はRevit内部ElementIdではなく、建具表上の建具番号を仮IDとして使用しています。
- `FamilyName` はRevitファミリ名ではなく、建具表上の種別記号 `SD` を仮格納しています。
- `TypeName` はRevitタイプ名ではなく、設置場所・室名に近い列を仮格納しています。
- `BIM_ClassificationCode`、`BIM_ModelRole`、`BIM_Zone` は現時点では空欄であり、未入力チェック対象として使用しています。
- `check_results_revit_v002.csv` の100件の違反は、正確な品質評価ではなく、処理フロー確認のための結果です。
- `QualityScore` はPoC用の簡易指標であり、実務上の正式な品質評価基準ではありません。
- `FixPriority` は実務の正解ラベルではなく、QualityScoreとHigh違反件数をもとにした仮ラベルです。
- 機械学習プロトタイプは未実装です。
- 生成AI向け構造化コンテキスト生成は未実装です。
- Revit APIやpyRevitとの直接連携は未実装です。
- RevitモデルやBIMデータの自動修正は対象外です。
- 設計判断、施工判断、モデル修正の最終判断は人間が行う前提です。

詳細は以下の資料に整理しています。

```text
docs/limitations.md
docs/evaluation_policy.md
docs/data_dictionary.md
```

---

## Future Work

今後は、7月応募可能MVPをもとに、機械学習プロトタイプと生成AI向け構造化コンテキスト生成へ拡張します。

### Machine Learning Prototype

- scikit-learnを用いた修正優先度分類プロトタイプ
- classification_report の出力
- confusion_matrix の出力
- feature_importance の出力
- FixPriority仮ラベルの妥当性整理
- 実務適用に必要な教師データの整理

### AI Context Generation

- RuleId、違反内容、重大度、品質スコア、修正優先度を含むJSON生成
- Markdown形式のAI向け説明文生成
- 生成AI向け構造化コンテキスト生成
- 将来的なRAG構成、ローカルLLM、Azure AI連携への拡張

### Revit / BIM Integration

- Revit集計表の列マッピング精度向上
- Revit内部ElementId、FamilyName、TypeName、Levelの取得確認
- pyRevit連携の検討
- Revit API連携の検討

### Streamlit / Visualization

- CSVアップロード機能
- 品質チェックの画面実行
- 特徴量データセット表示の改善
- 修正優先度分類結果の表示
- 生成AI向け構造化コンテキスト表示
- CSV / JSON ダウンロード機能の拡張

### Portfolio

- GitHub整理
- ポートフォリオPDF本体作成
- 職務経歴書への反映
- AI活用範囲と人間確認範囲の整理
- 開発部門へ渡せる仕様整理
- 面接用説明文の整理

---

## Next Priorities

次工程の優先順位は以下です。

1. READMEとportfolio_summary.mdを7月応募可能MVP版へ更新する
2. `docs/july_mvp_summary_260731.md` を作成する
3. Streamlit画面のスクリーンショットを保存する
4. GitHub公開用に不要ファイル・説明文を整理する
5. `src/check_bim_quality.py` へ品質チェック処理を移行する
6. scikit-learnによる修正優先度分類プロトタイプを作成する
7. 生成AI向け構造化コンテキスト生成へ拡張する
8. ポートフォリオPDF本体に整理する
9. 職務経歴書へBIM×AI/Data Engineeringのストーリーとして反映する

---

## Portfolio Summary

このPoCでは、Revit/BIMデータを対象に、Python/pandasによるデータ読み込み、データクレンジング、RuleIdベースの品質チェック、品質メトリクス作成、特徴量データセット作成、Streamlit簡易可視化までを実装しました。

初期版では、品質チェック用に整形したサンプルCSVを入力として使用し、必須パラメータ未入力、分類コード未入力、ファミリ命名規則違反をRuleId付きで検出しました。

その後、Revitから書き出した集計表TXTを `convert_revit_schedule.py` で品質チェック用CSVへ変換し、`clean_bim_data.py` で整形したうえで、`check_bim_quality.py` に入力して、Revit由来データの品質チェック結果 `check_results_revit_v002.csv` を出力できることを確認しました。

さらに、品質チェック結果から `calculate_quality_metrics.py` で品質メトリクスを作成し、`create_bim_features.py` で特徴量データセット `bim_features_v001.csv` を作成しました。

Streamlit簡易画面では、品質メトリクス概要、RuleId別違反件数、Category別違反件数、ElementId別品質スコア、特徴量データセット、品質チェック結果一覧を確認できます。

現時点のRevit由来データ対応は初期試作であり、列マッピングは仮設定です。

今後は、修正優先度分類プロトタイプ、生成AI向け構造化コンテキスト生成、Revit API / pyRevit連携へ拡張する予定です。

BIMデータをAI・機械学習・データ分析で扱うための前処理、ルールベース判定、品質メトリクス作成、特徴量設計、簡易可視化までの一連のPoCとして構築しています。
