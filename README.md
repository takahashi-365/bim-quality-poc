# BIM Data Quality & AI Readiness Assessment PoC

## 管理情報

PoC管理フォルダ：
`bim_quality_poc`

現在のPoC名：
`BIM Data Quality & AI Readiness Assessment PoC`

日本語名：
`BIMデータ品質・AI活用準備度評価PoC`

第1段階のPoC名：
`BIM Data Quality Engineering & AI Analysis PoC`

第1段階の日本語名：
`BIMデータ品質エンジニアリング・AI分析PoC`

本リポジトリは、第1段階で作成したBIMデータ品質チェックPoCを継続利用し、第2段階としてAI Readiness Assessmentへ拡張するものです。

---

## Overview

このPoCは、Revit/BIMデータをPythonで処理し、BIM品質ルールに基づく品質チェック、品質スコア算出、特徴量データセット作成、修正優先度分類プロトタイプ、AI Readiness Score算出、生成AI向け構造化コンテキスト生成、Fix Guide Markdown生成、Streamlitによる簡易可視化までを検証する個人開発PoCです。

第1段階では、Revit由来データをPython/pandasで読み込み、RuleIdベース品質チェック、QualityScore算出、特徴量設計、修正優先度分類プロトタイプ、生成AI向け構造化コンテキスト生成 v001 までを実装しました。

第2段階では、既存PoCを **BIM Data Quality & AI Readiness Assessment PoC** として再定義し、BIMデータがBI、機械学習、生成AI、将来的なRAGに活用できる状態かを評価する仕組みへ拡張しました。

本PoCの主目的は、生成AIにBIMデータをそのまま判断させることではありません。BIM品質ルール、品質チェック結果、業務影響、AI活用時の影響、AI Readiness Score、修正ガイドを構造化し、AIへ渡す前のデータ品質と文脈を整理することを重視しています。

---

## Purpose

このPoCの目的は、BIM/Revit導入支援の経験を活かしながら、建築BIMデータをAI・機械学習・データ分析で扱うためのデータ品質評価パイプラインを設計・実装することです。

第1段階では、Revit/BIMデータをPythonで読み込み、データ整形、品質チェック、品質メトリクス作成、特徴量設計、QualityScore算出、Streamlit簡易可視化、修正優先度分類プロトタイプ、生成AI向け構造化コンテキスト生成までを実装しました。

第2段階では、これをさらに拡張し、BIMデータがAIやデータ活用に使える状態かを評価するAI Readiness Assessmentを追加しました。

特に、以下の点を重視しています。

* PythonによるRevit/BIMデータ処理
* pandasによるデータ読み込み・整形・欠損処理
* RuleIdを用いたBIM品質ルール管理
* ルールベースによるBIMデータ品質チェック
* QualityScoreによるBIMデータ品質の簡易評価
* AI Readiness ScoreによるAI活用準備度の簡易評価
* 品質チェック結果のCSV出力
* 品質メトリクス、特徴量データセットの作成
* FixPriority仮ラベルの設計
* scikit-learnによる修正優先度分類プロトタイプ
* Streamlitによる簡易UI化
* Power BIによる補助的な可視化
* RuleId、違反内容、重大度、修正優先度、業務影響、AI活用時の影響をもとにした生成AI向け構造化コンテキスト生成
* AI Context JSON / Markdown v002生成
* Fix Guide Markdown生成
* 将来的なRAG、Azure AI、ローカルLLM、pyRevit、Revit API連携への拡張検討

なお、本PoCはAIモデルそのものの精度を追求するものではなく、AI活用前に必要となるBIMデータ品質評価、構造化コンテキスト生成、修正ガイド生成の流れを検証するものです。

---

## Background

BIM導入支援の現場では、Revitモデルそのものを作成するだけでなく、BIMデータをどのように標準化し、品質管理し、分析やAI活用に接続するかが重要になります。

BIMデータに未入力項目、分類コード不足、命名規則違反、属性情報のばらつきがある場合、そのままではBI、機械学習、生成AI、RAGなどに活用しにくくなります。

このPoCでは、BIM導入支援で扱ってきた品質ルールや運用ルールを、Pythonで処理可能なデータとして整理し、BIMデータをAI・機械学習で扱える状態に整えることを目指します。

---

## このPoCで示したいこと

* Revit/BIMデータをPythonで読み込み、構造化データとして処理できること
* Revit集計表TXTをpandasで読み込み、品質チェック用CSVへ変換できること
* BIM品質ルールをRuleIdとして定義し、ルールベース判定を実装できること
* BIM導入支援で扱ってきた品質ルールや運用ルールを、Pythonで処理可能なデータとして整理できること
* BIM品質チェック結果から、品質メトリクスや分析用データを作成できること
* 要素ごとの違反数、未入力項目数、重大度スコア、品質スコアなどの特徴量を設計できること
* BIM品質チェック結果を、機械学習や分析に利用できる特徴量データセットへ変換できること
* 修正優先度 High / Medium / Low の仮ラベルを設計し、修正優先度分類プロトタイプへ拡張できること
* AI Readiness Scoreにより、AI活用前のBIMデータ準備度を簡易評価できること
* Rule Master v003により、RuleIdごとのAI活用影響と減点値を管理できること
* AI Context v002により、品質チェック結果とAI Readiness情報を生成AI向け構造化コンテキストへ接続できること
* Fix Guide Markdownにより、RuleIdベースの修正方針を人間確認向けに整理できること
* Streamlitで、品質指標、違反傾向、品質スコア、AI Readiness Score、AI Context v002、Fix Guide Markdownを確認できること
* Power BIを補助的な可視化手段として使えること
* 生成AIに自由回答させるのではなく、RuleIdや品質チェック結果をもとにAIへ渡す情報を制御する設計にできること
* 将来的なRAG、Azure AI、ローカルLLM、pyRevit、Revit API連携に拡張できる設計にすること

---

## Current Status

現時点では、第1段階の応募準備用MVPに加えて、第2段階のAI Readiness Assessment拡張として、以下の処理フローを実装済みです。

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
train_fix_priority_model.py で修正優先度分類プロトタイプを実行
↓
fix_priority_classification_report_v001.csv
fix_priority_confusion_matrix_v001.csv
fix_priority_predictions_v001.csv
↓
calculate_ai_readiness_score.py でAI Readiness Scoreを算出
↓
ai_readiness_scores_v001.csv
↓
generate_ai_context.py で生成AI向け構造化コンテキスト v002 を生成
↓
ai_context_v002.json
ai_context_v002.md
↓
generate_fix_guide.py でFix Guide Markdownを生成
↓
fix_guides_v001.md
↓
streamlit_app.py でAI Readiness Assessmentを含む簡易可視化
```

この構成により、Revit/BIM由来のデータをPythonで前処理し、品質チェック、品質メトリクス、特徴量データセット、修正優先度分類、AI Readiness Score、生成AI向け構造化コンテキスト、Fix Guide Markdown、Streamlit簡易UI表示へ接続する流れを構築しています。

なお、現時点のRevit由来データ対応は初期試作であり、列マッピングは一部仮設定です。今回のAI Readiness Assessment拡張では、仮マッピングを隠さず、docsに前提条件と将来改善方針を整理しています。

---

## Data Source

Autodesk日本仕様 意匠サンプルモデル Revit 2024を検証用データとして使用します。

実案件データ・社外秘データは使用しません。

このPoCは、転職活動用ポートフォリオとして説明しやすいように、公開可能なサンプルデータを前提に構成しています。

---

## Revit Sample Model

検証には、Autodesk公式の日本仕様 意匠サンプルモデル Revit 2024を使用しています。

`.rvt` ファイル本体は、容量および配布条件を考慮し、GitHub公開対象外としています。

![Revit sample model](07_portfolio/screenshots/revit_sample_model_3d_view.png)

### Revit Schedule Used

本PoCでは、Revit集計表 `20 ドア 建具表 SD` をTXTとして書き出し、Python処理の入力データとして使用しています。

![Revit door schedule](07_portfolio/screenshots/revit_door_schedule_view.png)

---

## Target Categories

設計上の想定カテゴリは以下の3つです。

* 壁 / Walls
* ドア / Doors
* 部屋 / Rooms

ただし、現時点でRevit由来データとして実処理しているのは、ドア建具表の書き出しTXTです。

---

## Existing Schedule Export Check

現時点でGitHub公開対象として扱っているRevit集計表書き出しデータは以下です。

* 20 ドア 建具表 SD
  出力ファイル：`03_input_csv/door_schedule_SD_export_test_v001.txt`

このファイルは、Revitからタブ区切りテキストとして書き出し、Python/pandasで読み込めることを確認済みです。

現時点では、ドア建具表TXTを対象に、Pythonでの変換、クレンジング、品質チェック、メトリクス作成、特徴量データセット作成、修正優先度分類プロトタイプ、AI Readiness Score算出、AI Context v002生成、Fix Guide Markdown生成、Streamlit表示まで実装しています。

---

## Out of Scope

現時点では、以下は対象外とします。

* 本格的なRAGシステム構築
* Azure AI Search連携
* 生成AI API接続
* Revit API / pyRevitによる本格実装
* Revitモデルの自動修正
* 設計判断、施工判断、モデル修正の自動化
* 機械学習モデルの精度追求
* 深層学習
* 複雑なPower BIダッシュボード再設計

本PoCでは、AI活用前のBIMデータ品質評価、構造化コンテキスト生成、修正ガイド生成に集中します。

---

## Tech Stack

現時点で使用している技術は以下です。

* Python 3.12.10
* pandas 2.3.3
* pytest 9.0.3
* Streamlit 1.52.1
* scikit-learn 1.8.0
* CSV / TXT
* JSON / Markdown Context Generation
* Revit Schedule Export
* Power BI Desktop
* Markdown
* RuleId-based Quality Check

将来的な拡張候補として検討している技術は以下です。

* RAG
* Azure AI
* pyRevit
* Revit API

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

pytest の全体確認は以下で行います。

```powershell
python -m pytest tests -v
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
scikit-learn==1.8.0
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
├── .gitignore
├── app/
│   └── streamlit_app.py
├── 01_revit_model/
│   └── README.md
├── 02_rule_master/
│   ├── bim_rule_master_v002.csv
│   └── bim_rule_master_v003.csv
├── 03_input_csv/
│   ├── cleaned_bim_data_v001.csv
│   ├── door_schedule_SD_export_test_v001.txt
│   └── door_schedule_converted_v002.csv
├── 04_output_csv/
│   ├── ai_context_v001.json
│   ├── ai_context_v001.md
│   ├── ai_context_v002.json
│   ├── ai_context_v002.md
│   ├── ai_readiness_scores_v001.csv
│   ├── bim_features_v001.csv
│   ├── category_summary_v001.csv
│   ├── check_results_revit_v002.csv
│   ├── element_summary_v001.csv
│   ├── fix_guides_v001.md
│   ├── fix_priority_classification_report_v001.csv
│   ├── fix_priority_confusion_matrix_v001.csv
│   ├── fix_priority_predictions_v001.csv
│   ├── quality_metrics_v001.csv
│   └── rule_summary_v001.csv
├── 05_powerbi/
│   └── README.md
├── 07_portfolio/
│   ├── bim_quality_poc_portfolio_v003.pdf
│   └── screenshots/
│       ├── powerbi_dashboard_v001.png
│       ├── revit_sample_model_3d_view.png
│       └── revit_door_schedule_view.png
├── docs/
│   ├── ai_readiness_assessment_plan.md
│   ├── data_dictionary.md
│   ├── evaluation_policy.md
│   ├── limitations.md
│   ├── portfolio_summary.md
│   ├── revit_api_pyrevit_integration_plan.md
│   ├── revit_schedule_column_mapping.md
│   ├── rule_specification.md
│   └── system_overview.md
├── src/
│   ├── calculate_ai_readiness_score.py
│   ├── calculate_quality_metrics.py
│   ├── check_bim_quality.py
│   ├── clean_bim_data.py
│   ├── convert_revit_schedule.py
│   ├── create_bim_features.py
│   ├── generate_ai_context.py
│   ├── generate_fix_guide.py
│   ├── train_fix_priority_model.py
│   └── utils.py
└── tests/
    ├── test_ai_readiness_score.py
    └── test_quality_rules.py
```

※ `.rvt` ファイルおよび `.pbix` ファイル本体は、容量・配布条件を考慮し、GitHub公開対象外としています。

---

## Folder Role

現時点の各フォルダの役割は以下です。

* `src/`：BIMデータ変換、クレンジング、品質チェック、品質メトリクス作成、特徴量作成、修正優先度分類、AI Readiness Score算出、AI Context生成、Fix Guide生成の本実装コード
* `app/`：Streamlit簡易画面
* `docs/`：設計資料、制約、評価方針、ポートフォリオ要約、拡張計画、業務要件対応、Revit列マッピング整理
* `tests/`：RuleIdベース品質チェックとAI Readiness Assessment関連ロジックの最小テスト
* `02_rule_master/`：BIM品質チェック用ルールマスタ、AI Readiness Score用拡張ルールマスタ
* `03_input_csv/`：Revit書き出しTXT、変換後CSV、クレンジング済みCSV
* `04_output_csv/`：品質チェック結果、品質メトリクス、特徴量、AI Readiness Score、AI Context、Fix Guide、修正優先度分類結果
* `05_powerbi/`：Power BI可視化に関する説明
* `07_portfolio/`：提出用ポートフォリオPDFと補助スクリーンショット

旧試作コード、応募文面、面接メモ、個人作業メモ、旧CSV、旧README、`.rvt` 本体、`.pbix` 本体はGitHub公開対象外としています。

---

## RuleId-based Quality Check

### RuleIdルールマスタ

第1段階のルールマスタ：

```text
02_rule_master/bim_rule_master_v002.csv
```

第2段階のAI Readiness対応ルールマスタ：

```text
02_rule_master/bim_rule_master_v003.csv
```

目的：

Python品質チェック、品質メトリクス作成、特徴量データセット作成、Streamlit簡易画面、修正優先度分類プロトタイプ、AI Readiness Score算出、生成AI向け構造化コンテキスト生成、Fix Guide Markdown生成で共通して使用するチェックルールIDを定義します。

初期ルール：

* R-001：必須パラメータ未入力
* R-002：分類コード未入力
* R-003：ファミリ命名規則違反

v002では、v001に含まれていた不要な空行を削除し、3行 × 10列のルールマスタとして整理しています。

v003では、AI Readiness Scoreの算出に対応するため、以下の列を追加しています。

* `AIReadinessImpact`
* `AIReadinessPenalty`

初期ペナルティ設定は以下です。

| RuleId | 内容         | AIReadinessImpact | AIReadinessPenalty |
| ------ | ---------- | ----------------- | -----------------: |
| R-001  | 必須パラメータ未入力 | High              |                 15 |
| R-002  | 分類コード未入力   | High              |                 20 |
| R-003  | ファミリ命名規則違反 | Medium            |                 10 |

ルール数を増やすことよりも、RuleIdを共通キーとして、Pythonチェック結果、補助的な可視化、修正優先度分類、AI Readiness Score、生成AI向け構造化コンテキスト生成、Fix Guide Markdown生成を接続することを重視します。

---

## Revit Schedule TXT Conversion

作成ファイル：

```text
src/convert_revit_schedule.py
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
python .\src\convert_revit_schedule.py
```

実行結果：

```text
Raw data shape: (26, 33)
Removed non-data rows: 1
Converted data shape: (25, 10)
```

注意点：

現時点の列マッピングは仮設定です。

* `ElementId` はRevit内部ElementIdではなく、建具表上の建具番号を仮IDとして使用しています。
* `FamilyName` はRevitファミリ名ではなく、建具表上の種別記号 `SD` を仮格納しています。
* `TypeName` はRevitタイプ名ではなく、設置場所・室名に近い列を仮格納しています。

詳細は以下に整理しています。

```text
docs/data_dictionary.md
docs/revit_schedule_column_mapping.md
```

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

* 必要列の確認
* 不足列がある場合の空列追加
* 列順の標準化
* NaNの空文字化
* 文字列の前後スペース削除
* `ElementId` 空欄行の除外
* 完全一致の重複行の除外

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
src/check_bim_quality.py
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
python .\src\check_bim_quality.py
```

実行結果：

```text
Input data shape: (25, 10)
Rule master shape: (3, 10)
Check completed. Results: 100 issues found.
```

RuleId別内訳：

* R-001：50件
* R-002：25件
* R-003：25件

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

* 総違反件数の集計
* RuleId別違反件数の集計
* Severity別違反件数の集計
* Category別違反件数の集計
* ElementId別違反件数の集計
* SeverityScoreの算出
* QualityScoreの算出

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

* RuleViolationCount
* MissingFieldCount
* HighViolationCount
* MediumViolationCount
* LowViolationCount
* HasClassificationCode
* FamilyNameValid
* SeverityScore
* QualityScore
* FixPriority

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

| Severity |  減点 |
| -------- | --: |
| High     | 10点 |
| Medium   |  5点 |
| Low      |  1点 |

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

## Fix Priority Classification Prototype

作成ファイル：

```text
src/train_fix_priority_model.py
```

入力CSV：

```text
04_output_csv/bim_features_v001.csv
```

出力CSV：

```text
04_output_csv/fix_priority_classification_report_v001.csv
04_output_csv/fix_priority_confusion_matrix_v001.csv
04_output_csv/fix_priority_predictions_v001.csv
```

目的：

特徴量データセットをもとに、scikit-learnを用いた修正優先度分類プロトタイプを作成します。

現時点では、`FixPriority` は実務の正解ラベルではなく、QualityScoreとHigh違反件数をもとにした仮ラベルです。

そのため、この分類プロトタイプは機械学習モデルの精度を追求するものではなく、BIM品質チェック結果を特徴量化し、分類処理へ接続できることを確認するための初期実装として位置づけます。

---

## AI Readiness Score

作成ファイル：

```text
src/calculate_ai_readiness_score.py
```

入力ファイル：

```text
04_output_csv/check_results_revit_v002.csv
02_rule_master/bim_rule_master_v003.csv
```

出力ファイル：

```text
04_output_csv/ai_readiness_scores_v001.csv
```

目的：

品質チェック結果とRule Master v003をもとに、ElementIdごとのAI Readiness Scoreを算出します。

AI Readiness Scoreは、BIMデータがBI、機械学習、生成AI、将来的なRAGに活用できる状態かを簡易評価するためのPoC指標です。

計算式：

```text
AIReadinessScore = 100 - AIReadinessPenalty合計
```

スコアが0未満になる場合は0とします。

初期レベル分類：

| Score Range | Level  |
| ----------- | ------ |
| 80-100      | High   |
| 60-79       | Medium |
| 0-59        | Low    |

出力CSVの主な列：

* `ElementId`
* `Category`
* `RuleViolationCount`
* `AIReadinessPenaltyTotal`
* `AIReadinessScore`
* `AIReadinessLevel`
* `BlockingRuleIds`
* `HighImpactRuleCount`
* `MediumImpactRuleCount`
* `HumanReviewRequired`

今回の初期データでは、25要素すべてが以下の結果となっています。

```text
AIReadinessScore = 40
AIReadinessLevel = Low
HumanReviewRequired = True
```

これは不具合ではなく、各要素に必須パラメータ未入力、分類コード未入力、ファミリ命名規則違反が含まれているためです。

---

## AI Context Generation

作成ファイル：

```text
src/generate_ai_context.py
```

入力CSV：

```text
04_output_csv/check_results_revit_v002.csv
04_output_csv/bim_features_v001.csv
04_output_csv/ai_readiness_scores_v001.csv
```

出力ファイル：

```text
04_output_csv/ai_context_v002.json
04_output_csv/ai_context_v002.md
```

目的：

RuleId、違反内容、重大度、品質スコア、修正優先度、AI Readiness Score、AI Readiness Level、人間確認要否、修正ガイドを含む、生成AI向け構造化コンテキストを生成します。

現時点では、OpenAI APIなどの生成AI APIを直接呼び出すのではなく、将来的に生成AIやRAGへ渡す前段階の構造化JSON / Markdownを作成するところまでを対象としています。

v002では、v001の構造化コンテキストに加えて、以下を追加しています。

* `AIReadinessScore`
* `AIReadinessLevel`
* `AIReadinessPenaltyTotal`
* `BlockingRuleIds`
* `HighImpactRuleCount`
* `MediumImpactRuleCount`
* `HumanReviewRequired`

これにより、BIM品質チェック結果とAI活用準備度評価を、生成AI向けの参照情報として接続できるようにしています。

---

## Fix Guide Markdown Generation

作成ファイル：

```text
src/generate_fix_guide.py
```

入力ファイル：

```text
04_output_csv/check_results_revit_v002.csv
02_rule_master/bim_rule_master_v003.csv
04_output_csv/ai_readiness_scores_v001.csv
```

出力ファイル：

```text
04_output_csv/fix_guides_v001.md
```

目的：

品質チェック結果、Rule Master v003、AI Readiness Scoreをもとに、RuleIdベースの修正ガイドMarkdownを生成します。

この処理では、生成AI APIは使用していません。RuleId、Severity、AIReadinessImpact、AIReadinessPenalty、FixGuideをもとに、テンプレート方式で人間確認向けの修正方針を出力します。

出力Markdownには以下を含めています。

* Summary
* Input Files
* AI Readiness Level Summary
* Blocking Rule Summary
* ElementId別 Fix Guide
* Limitations

ElementId別 Fix Guideでは、各要素について以下を確認できます。

* AI Readiness Score
* AI Readiness Level
* AI Readiness Penalty Total
* Blocking RuleIds
* Human Review Required
* RuleId別のFixGuide

---

## Streamlit App

作成ファイル：

```text
app/streamlit_app.py
```

目的：

BIM品質チェック結果、品質メトリクス、特徴量データセット、修正優先度分類結果、AI Readiness Score、生成AI向け構造化コンテキスト v002、Fix Guide Markdownを画面で確認できる簡易UIを作成します。

実行コマンド：

```powershell
streamlit run .\app\streamlit_app.py
```

表示内容：

* 品質メトリクス概要
* RuleId別違反件数
* Category別違反件数
* ElementId別品質スコア
* 特徴量データセット
* FixPriority件数
* 品質チェック結果一覧
* RuleId / Severity / Category フィルタ
* AI Readiness Assessment
* AI Readiness Score概要
* AI Readiness Level別件数
* ElementId別AI Readiness Score
* AI活用を阻害しているRuleIdランキング
* Element Detail
* 修正優先度分類プロトタイプ結果
* 生成AI向け構造化コンテキスト v002
* AI Context JSON / Markdown Preview
* Fix Guide Markdown Preview
* CSV / JSON / Markdown ダウンロード
* 現時点の注意点

この画面は、本格的な業務アプリではなく、面接・ポートフォリオ説明用のMVPとして位置づけます。

---

## Visualization

### Streamlit

Streamlitは、応募準備用MVPおよびAI Readiness Assessment拡張の主な簡易UIとして位置づけます。

Pythonで作成した品質チェック結果、品質メトリクス、特徴量データセット、修正優先度分類結果、AI Readiness Score、AI Context v002、Fix Guide Markdownを画面で確認できるようにしています。

### Power BI

Power BIは、Pythonで処理したBIM品質データの分析結果を確認するための補助的な可視化手段として使用します。

`.pbix` ファイル本体は、容量・配布条件を考慮し、GitHub公開対象外としています。

代替として、Power BIダッシュボードのスクリーンショットを以下に配置しています。

```text
07_portfolio/screenshots/powerbi_dashboard_v001.png
```

---

## Tests

作成ファイル：

```text
tests/test_quality_rules.py
tests/test_ai_readiness_score.py
```

目的：

RuleIdベース品質チェックと、AI Readiness Assessment関連ロジックの基本動作をpytestで確認します。

`tests/test_quality_rules.py` で確認している内容：

* R-001：必須パラメータ未入力を検出できるか
* R-002：分類コード未入力を検出できるか
* R-003：ファミリ命名規則違反を検出できるか
* 正常なファミリ名の場合、違反なしとして扱えるか
* 1要素に複数の違反がある場合、想定どおり検出できるか

`tests/test_ai_readiness_score.py` で確認している内容：

* AI Readiness Level分類
* AI Readiness Score計算
* スコア下限0の扱い
* HumanReviewRequired判定
* Rule Master v003必須列確認
* Rule Master v003必須列不足時のエラー確認
* ElementId表示整形

実行コマンド：

```powershell
python -m pytest tests -v
```

実行結果：

```text
collected 16 items
16 passed
```

内訳：

```text
tests/test_ai_readiness_score.py：11件 passed
tests/test_quality_rules.py：5件 passed
合計：16件 passed
```

現時点では、これらのテストは本格的な網羅テストではなく、RuleIdベース品質チェックとAI Readiness Assessment関連ロジックの期待動作を固定するための最小テストとして位置づけます。

---

## Output Files

現時点で出力・確認済みの主な公開対象ファイルは以下です。

```text
03_input_csv/door_schedule_SD_export_test_v001.txt
03_input_csv/door_schedule_converted_v002.csv
03_input_csv/cleaned_bim_data_v001.csv
02_rule_master/bim_rule_master_v002.csv
02_rule_master/bim_rule_master_v003.csv
04_output_csv/check_results_revit_v002.csv
04_output_csv/quality_metrics_v001.csv
04_output_csv/rule_summary_v001.csv
04_output_csv/category_summary_v001.csv
04_output_csv/element_summary_v001.csv
04_output_csv/bim_features_v001.csv
04_output_csv/fix_priority_classification_report_v001.csv
04_output_csv/fix_priority_confusion_matrix_v001.csv
04_output_csv/fix_priority_predictions_v001.csv
04_output_csv/ai_readiness_scores_v001.csv
04_output_csv/ai_context_v001.json
04_output_csv/ai_context_v001.md
04_output_csv/ai_context_v002.json
04_output_csv/ai_context_v002.md
04_output_csv/fix_guides_v001.md
07_portfolio/bim_quality_poc_portfolio_v003.pdf
07_portfolio/screenshots/powerbi_dashboard_v001.png
07_portfolio/screenshots/revit_sample_model_3d_view.png
07_portfolio/screenshots/revit_door_schedule_view.png
```

---

## Current Deliverables

現時点での主な成果は以下です。

* Revitサンプルモデルを使った検証環境の準備
* Revit集計表TXTの書き出し確認
* RuleIdルールマスタ整理版の作成
* Rule Master v003の作成
* Revit書き出しTXTのPython/pandas読み込み確認
* Revit書き出しTXTから品質チェック用CSVへの変換
* Revit由来CSVのクレンジング
* RuleIdベース品質チェックの実行
* RuleId付きチェック結果CSVの出力
* 品質メトリクスCSVの作成
* RuleId別、Category別、ElementId別集計CSVの作成
* QualityScoreの算出
* 特徴量データセットの作成
* FixPriority仮ラベルの作成
* scikit-learnによる修正優先度分類プロトタイプ
* AI Readiness Scoreの算出
* AI Readiness Levelの分類
* HumanReviewRequiredの判定
* AI Context v002の生成
* Fix Guide Markdownの生成
* Streamlit簡易画面のAI Readiness対応
* pytestによる最小テスト
* `tests/test_quality_rules.py` の作成
* `tests/test_ai_readiness_score.py` の作成
* 全体テスト `16 passed` の確認
* Power BIによる補助的な可視化
* `docs/system_overview.md` の更新
* `docs/portfolio_summary.md` の更新
* `docs/data_dictionary.md` の更新
* `docs/revit_schedule_column_mapping.md` の新規作成
* `docs/rule_specification.md` の更新
* `docs/limitations.md` の更新
* `docs/evaluation_policy.md` の更新
* `docs/ai_readiness_assessment_plan.md` の更新
* `docs/revit_api_pyrevit_integration_plan.md` の作成
* ポートフォリオPDF v002の作成
* GitHub公開構成の整理

---

## Limitations

現時点の制約と注意点は以下です。

* Revit由来データ対応は初期試作です。
* `door_schedule_converted_v002.csv` の列マッピングは仮設定です。
* `ElementId` はRevit内部ElementIdではなく、建具表上の建具番号を仮IDとして使用しています。
* `FamilyName` はRevitファミリ名ではなく、建具表上の種別記号 `SD` を仮格納しています。
* `TypeName` はRevitタイプ名ではなく、設置場所・室名に近い列を仮格納しています。
* `BIM_ClassificationCode`、`BIM_ModelRole`、`BIM_Zone` は現時点では空欄であり、未入力チェック対象として使用しています。
* `check_results_revit_v002.csv` の100件の違反は、正確な品質評価ではなく、処理フロー確認のための結果です。
* `QualityScore` はPoC用の簡易指標であり、実務上の正式な品質評価基準ではありません。
* `FixPriority` は実務の正解ラベルではなく、QualityScoreとHigh違反件数をもとにした仮ラベルです。
* 修正優先度分類プロトタイプは初期実装済みですが、現時点の `FixPriority` は `High` のみであり、本格的な分類精度評価は未実施です。
* `AIReadinessScore` はPoC用の簡易指標であり、実務上の正式なAI活用準備度基準ではありません。
* `AIReadinessPenalty` はPoC用の仮設定であり、今後、社内BIM標準、分類体系、プロジェクト要件、AI利用目的に応じて調整する前提です。
* `AI Context v002` は生成AIやRAGへ渡す前段階の構造化コンテキストであり、生成AI APIの呼び出しは未実装です。
* `Fix Guide Markdown` は生成AI APIではなく、RuleIdベースのテンプレート方式で生成しています。
* Revit APIやpyRevitとの直接連携は未実装です。
* RevitモデルやBIMデータの自動修正は対象外です。
* 設計判断、施工判断、モデル修正の最終判断は人間が行う前提です。

詳細は以下の資料に整理しています。

```text
docs/limitations.md
docs/evaluation_policy.md
docs/data_dictionary.md
docs/revit_schedule_column_mapping.md
docs/ai_readiness_assessment_plan.md
```

---

## Future Work

今後は、第2段階で実装したAI Readiness Assessmentをもとに、GitHub公開範囲の確認、Streamlit画面スクリーンショットの整理、必要に応じたポートフォリオPDF v003化を検討します。

### GitHub Publication

* GitHub公開対象ファイルの最終確認
* `.rvt` ファイル本体を公開対象外とする
* `.pbix` ファイル本体を公開対象外とする
* 実案件データ、社外秘データ、個人情報が含まれていないことを確認する
* 旧試作コード、応募文面、面接メモ、個人作業メモを公開対象外とする
* READMEとdocsの記載内容が公開対象ファイルと一致しているか確認する

### Portfolio

* Streamlit画面スクリーンショットの保存
* AI Readiness Assessment拡張内容の説明反映
* 必要に応じたポートフォリオPDF v003化検討
* 面接用説明文の整理
* 職務経歴書向け要約の更新

### Revit / BIM Integration

* Revit内部ElementId、FamilyName、TypeName、Level、RoomNameの正式取得検討
* Revit集計表の列マッピング精度向上
* pyRevit / Revit API連携の検討

### AI / RAG Extension

* 生成AI API接続の検討
* RAG構成の検討
* Azure AI Search連携の検討
* AI Context v002を将来的なRAG前処理として活用する方針の検討

---

## Next Priorities

次工程の優先順位は以下です。

1. GitHub公開範囲を確認する
2. 公開対象外ファイルを確認する
3. READMEとdocsの最終整合性を確認する
4. Streamlit画面スクリーンショットを保存する
5. 必要に応じてポートフォリオPDF v003化を検討する

---

## Portfolio Summary

このPoCでは、Revit/BIMデータを対象に、Python/pandasによるデータ読み込み、データクレンジング、RuleIdベースの品質チェック、品質メトリクス作成、特徴量データセット作成、修正優先度分類プロトタイプ、AI Readiness Score算出、生成AI向け構造化コンテキスト生成、Fix Guide Markdown生成、Streamlit簡易可視化までを実装しました。

初期版では、品質チェック用に整形したサンプルCSVを入力として使用し、必須パラメータ未入力、分類コード未入力、ファミリ命名規則違反をRuleId付きで検出しました。

その後、Revitから書き出した集計表TXTを `convert_revit_schedule.py` で品質チェック用CSVへ変換し、`clean_bim_data.py` で整形したうえで、`check_bim_quality.py` に入力して、Revit由来データの品質チェック結果 `check_results_revit_v002.csv` を出力できることを確認しました。

さらに、品質チェック結果から `calculate_quality_metrics.py` で品質メトリクスを作成し、`create_bim_features.py` で特徴量データセット `bim_features_v001.csv` を作成しました。

修正優先度分類プロトタイプでは、`bim_features_v001.csv` をもとに、scikit-learnでFixPriority分類の初期処理を実装しました。

第2段階では、既存PoCを `BIM Data Quality & AI Readiness Assessment PoC` として再定義し、`bim_rule_master_v003.csv`、`calculate_ai_readiness_score.py`、`ai_readiness_scores_v001.csv` を追加して、BIMデータがAI活用に使える状態かを簡易評価できるようにしました。

生成AI向け構造化コンテキスト生成では、AI Context v002として、RuleId、違反内容、重大度、品質スコア、修正優先度、AI Readiness Score、AI Readiness Level、人間確認要否を含むJSON / Markdownを出力できるようにしました。

Fix Guide Markdown生成では、品質チェック結果、Rule Master v003、AI Readiness Scoreをもとに、RuleIdベースの修正方針をMarkdownとして出力できるようにしました。

Streamlit簡易画面では、品質メトリクス概要、RuleId別違反件数、Category別違反件数、ElementId別品質スコア、特徴量データセット、修正優先度分類結果、AI Readiness Assessment、AI Context v002、Fix Guide Markdown Preview、品質チェック結果一覧を確認できます。

現時点のRevit由来データ対応は初期試作であり、列マッピングは仮設定です。

BIMデータをAI・機械学習・データ分析で扱うための前処理、ルールベース判定、品質メトリクス作成、特徴量設計、AI活用準備度評価、構造化コンテキスト生成、修正ガイド生成、簡易可視化までの一連のPoCとして構築しています。
