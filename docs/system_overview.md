# System Overview

## BIM Data Quality & AI Readiness Assessment PoC

## この資料の目的

この資料は、`BIM Data Quality & AI Readiness Assessment PoC` の全体構成、処理フロー、各Pythonファイルの役割を整理するためのものです。

READMEはPoC全体の説明、`portfolio_summary.md` はポートフォリオ用の要約、`system_overview.md` はシステム構成と処理の流れを説明する資料として位置づけます。

本資料では、第1段階のBIMデータ品質チェックPoCに加えて、第2段階で追加したAI Readiness Score、AI Context v002、Fix Guide Markdown、Streamlit画面拡張までを含めた現時点のシステム構成を整理します。

---

## PoC全体の目的

このPoCは、Revit/BIMデータをPythonで処理し、品質チェック、品質メトリクス作成、特徴量化、修正優先度分類プロトタイプ、AI Readiness Score算出、生成AI向け構造化コンテキスト生成、Fix Guide Markdown生成、Streamlit簡易可視化へつなげるデータ処理パイプラインを検証するものです。

単なるBIM品質チェックツールではなく、建築BIMデータをAI・機械学習・データ分析で扱える状態に整えるための、BIMデータ品質・AI活用準備度評価PoCとして位置づけます。

本PoCでは、生成AIにBIMデータをそのまま自由判断させるのではなく、RuleId、品質チェック結果、QualityScore、FixPriority、AIReadinessScore、HumanReviewRequired、FixGuideなどを構造化し、AIへ渡す前段階の情報整理を重視します。

---

## 第1段階と第2段階の位置づけ

### 第1段階

第1段階のPoC名：

`BIM Data Quality Engineering & AI Analysis PoC`

第1段階では、Revit由来データをPythonで読み込み、RuleIdベースでBIMデータ品質チェックを行う仕組みを作成しました。

主な内容は以下です。

* Revit書き出しTXTのPython読み込み
* 品質チェック用CSVへの変換
* データクレンジング
* RuleIdベース品質チェック
* QualityScore算出
* 品質メトリクス作成
* 特徴量データセット作成
* FixPriority仮ラベル作成
* scikit-learnによる修正優先度分類プロトタイプ
* 生成AI向け構造化コンテキスト v001
* Streamlit簡易画面
* Power BI補助可視化

### 第2段階

第2段階のPoC名：

`BIM Data Quality & AI Readiness Assessment PoC`

日本語名：

`BIMデータ品質・AI活用準備度評価PoC`

第2段階では、既存PoCを発展させ、BIMデータがBI、機械学習、生成AI、将来的なRAGに活用できる状態かを評価できる構成に拡張しました。

主な内容は以下です。

* Rule Master v003
* AI Readiness Score
* AI Context JSON / Markdown v002
* Fix Guide Markdown
* Streamlit上でのAI Readiness表示
* Revit列マッピングの前提整理

---

## 全体処理フロー

現時点の全体処理フローは以下です。

```text
Revit書き出しTXT
↓
1. convert_revit_schedule.py
   Revit集計表TXTを品質チェック用CSVへ変換
↓
door_schedule_converted_v002.csv
↓
2. clean_bim_data.py
   品質チェック前のデータクレンジング
↓
cleaned_bim_data_v001.csv
↓
3. check_bim_quality.py
   RuleIdベース品質チェック
↓
check_results_revit_v002.csv
↓
4. calculate_quality_metrics.py
   品質メトリクス作成
↓
quality_metrics_v001.csv
rule_summary_v001.csv
category_summary_v001.csv
element_summary_v001.csv
↓
5. create_bim_features.py
   特徴量データセット作成
↓
bim_features_v001.csv
↓
6. train_fix_priority_model.py
   修正優先度分類プロトタイプ
↓
fix_priority_classification_report_v001.csv
fix_priority_confusion_matrix_v001.csv
fix_priority_predictions_v001.csv
↓
7. calculate_ai_readiness_score.py
   AI Readiness Score算出
↓
ai_readiness_scores_v001.csv
↓
8. generate_ai_context.py
   生成AI向け構造化コンテキスト v002 生成
↓
ai_context_v002.json
ai_context_v002.md
↓
9. generate_fix_guide.py
   Fix Guide Markdown生成
↓
fix_guides_v001.md
↓
10. streamlit_app.py
    Streamlitによる簡易可視化
```

---

## 現時点で確認済みの処理フロー

現時点では、以下のルートを確認済みです。

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

確認済みの内容は以下です。

* Revit書き出しTXTをPython/pandasで読み込めること
* タブ区切りTXTを表データとして扱えること
* Revit書き出しTXTを品質チェック用CSVへ変換できること
* 先頭の非データ行を除外できること
* 変換後CSVをクレンジングできること
* クレンジング済みCSVを品質チェックツールに入力できること
* RuleId付き品質チェック結果CSVを出力できること
* 品質メトリクスとQualityScoreを算出できること
* 特徴量データセットを作成できること
* FixPriority仮ラベルを作成できること
* scikit-learnによる修正優先度分類プロトタイプを実行できること
* AI Readiness ScoreをElementIdごとに算出できること
* AI Context v002としてJSON / Markdownを出力できること
* Fix Guide Markdownを出力できること
* Streamlit上でAI Readiness Assessment、AI Context v002、Fix Guide Markdownを確認できること

---

## 入力データ

### Revit書き出しTXT

Revitから書き出したドア建具表データです。

現時点でGitHub公開対象として扱っているファイル：

```text
03_input_csv/door_schedule_SD_export_test_v001.txt
```

このファイルは、Autodesk日本仕様 意匠サンプルモデル Revit 2024をもとにした検証用データです。

実案件データ・社外秘データは使用していません。

### Revit由来変換CSV

Revit書き出しTXTを品質チェック用に変換したCSVです。

```text
03_input_csv/door_schedule_converted_v002.csv
```

現時点では、列マッピングは一部仮設定です。

### クレンジング済みCSV

品質チェック前に、列順、空欄、重複、文字列などを整理したCSVです。

```text
03_input_csv/cleaned_bim_data_v001.csv
```

---

## ルール定義

### RuleIdルールマスタ v002

第1段階の品質チェック用ルールマスタです。

```text
02_rule_master/bim_rule_master_v002.csv
```

主な役割：

* 品質チェックルールを外部CSVとして管理する
* Python品質チェックで参照する
* 品質メトリクス作成でRuleIdを利用する
* 特徴量データセット作成でRuleIdを利用する
* AI Context生成でRuleIdを利用する

初期ルール：

* R-001：必須パラメータ未入力
* R-002：分類コード未入力
* R-003：ファミリ命名規則違反

### Rule Master v003

第2段階のAI Readiness Score算出用に拡張したルールマスタです。

```text
02_rule_master/bim_rule_master_v003.csv
```

v003では、既存のRule Master v002に以下の列を追加しています。

* `AIReadinessImpact`
* `AIReadinessPenalty`

初期ペナルティ設定は以下です。

| RuleId | 内容         | AIReadinessImpact | AIReadinessPenalty |
| ------ | ---------- | ----------------- | -----------------: |
| R-001  | 必須パラメータ未入力 | High              |                 15 |
| R-002  | 分類コード未入力   | High              |                 20 |
| R-003  | ファミリ命名規則違反 | Medium            |                 10 |

Rule Master v003は、AI Readiness Score、AI Context v002、Fix Guide Markdown生成で使用します。

---

## 出力データ

### 品質チェック結果CSV

RuleIdベース品質チェックによって出力されるCSVです。

```text
04_output_csv/check_results_revit_v002.csv
```

主な出力項目：

* CheckId
* ElementId
* Category
* FamilyName
* TypeName
* Level
* ParameterName
* CurrentValue
* RuleId
* RuleName
* Severity
* Status
* FixGuide
* DetectedAt
* SourceFile
* ModelName

現時点の出力結果：

```text
対象要素数: 25
品質チェック結果: 100件
```

RuleId別内訳：

| RuleId | 内容         | 件数 |
| ------ | ---------- | -: |
| R-001  | 必須パラメータ未入力 | 50 |
| R-002  | 分類コード未入力   | 25 |
| R-003  | ファミリ命名規則違反 | 25 |

### 品質メトリクスCSV

品質チェック結果から作成する品質メトリクスです。

```text
04_output_csv/quality_metrics_v001.csv
04_output_csv/rule_summary_v001.csv
04_output_csv/category_summary_v001.csv
04_output_csv/element_summary_v001.csv
```

主な内容：

* 総違反件数
* RuleId別違反件数
* Severity別違反件数
* Category別違反件数
* ElementId別違反件数
* SeverityScore
* QualityScore

### 特徴量データセット

品質チェック結果とElementId別集計をもとに作成する特徴量データセットです。

```text
04_output_csv/bim_features_v001.csv
```

主な特徴量：

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

### 修正優先度分類プロトタイプ出力

scikit-learnによる修正優先度分類プロトタイプの出力です。

```text
04_output_csv/fix_priority_classification_report_v001.csv
04_output_csv/fix_priority_confusion_matrix_v001.csv
04_output_csv/fix_priority_predictions_v001.csv
```

現時点では、FixPriorityは実務の正解ラベルではなく、QualityScoreとHigh違反件数をもとにした仮ラベルです。

### AI Readiness Score出力

AI Readiness Score算出結果です。

```text
04_output_csv/ai_readiness_scores_v001.csv
```

主な列：

* ElementId
* Category
* RuleViolationCount
* AIReadinessPenaltyTotal
* AIReadinessScore
* AIReadinessLevel
* BlockingRuleIds
* HighImpactRuleCount
* MediumImpactRuleCount
* HumanReviewRequired

現時点の出力結果：

```text
AIReadinessScore = 40
AIReadinessLevel = Low
HumanReviewRequired = True
```

全25要素が同じ結果です。

### AI Context v002

生成AIや将来的なRAGへ渡す前段階の構造化コンテキストです。

```text
04_output_csv/ai_context_v002.json
04_output_csv/ai_context_v002.md
```

主な内容：

* Project情報
* 入力ファイル情報
* Summary
* Rule Summary
* FixPriority Summary
* AI Readiness Level Summary
* ElementId別Context
* Quality Summary
* AI Readiness情報
* RuleId別違反詳細
* AI向け指示条件
* Limitations

### Fix Guide Markdown

品質チェック結果、Rule Master v003、AI Readiness Scoreをもとに作成する修正ガイドMarkdownです。

```text
04_output_csv/fix_guides_v001.md
```

主な内容：

* Summary
* Input Files
* AI Readiness Level Summary
* Blocking Rule Summary
* ElementId別 Fix Guide
* Limitations

---

## Pythonファイル構成

現時点では、主要な実装コードは `src/` に集約しています。

### `src/convert_revit_schedule.py`

Revit集計表TXTを読み込み、品質チェック用CSVへ変換するスクリプトです。

主な処理：

* TXT読み込み
* タブ区切りデータの読み込み
* 先頭非データ行の除外
* 必要列の抽出
* PoC用標準列へのマッピング
* `Category`、`SourceFile`、`ModelName` の付与
* 品質チェック用CSV出力

入力：

```text
03_input_csv/door_schedule_SD_export_test_v001.txt
```

出力：

```text
03_input_csv/door_schedule_converted_v002.csv
```

### `src/clean_bim_data.py`

品質チェック前のBIMデータクレンジングを行うスクリプトです。

主な処理：

* 必要列の確認
* 不足列がある場合の空列追加
* 列順の標準化
* NaNの空文字化
* 文字列の前後スペース削除
* ElementId空欄行の除外
* 重複行の除外

入力：

```text
03_input_csv/door_schedule_converted_v002.csv
```

出力：

```text
03_input_csv/cleaned_bim_data_v001.csv
```

### `src/check_bim_quality.py`

RuleIdベースでBIM品質チェックを行う中心スクリプトです。

主な処理：

* クレンジング済みCSV読み込み
* Rule Master v002読み込み
* 必須パラメータ未入力チェック
* 分類コード未入力チェック
* 命名規則チェック
* RuleId付きチェック結果CSV出力

入力：

```text
03_input_csv/cleaned_bim_data_v001.csv
02_rule_master/bim_rule_master_v002.csv
```

出力：

```text
04_output_csv/check_results_revit_v002.csv
```

### `src/calculate_quality_metrics.py`

品質チェック結果から品質メトリクスを作成するスクリプトです。

主な処理：

* 総違反件数の集計
* RuleId別違反件数の集計
* Severity別違反件数の集計
* Category別違反件数の集計
* ElementId別違反件数の集計
* SeverityScoreの算出
* QualityScoreの算出

入力：

```text
04_output_csv/check_results_revit_v002.csv
```

出力：

```text
04_output_csv/quality_metrics_v001.csv
04_output_csv/rule_summary_v001.csv
04_output_csv/category_summary_v001.csv
04_output_csv/element_summary_v001.csv
```

### `src/create_bim_features.py`

BIM品質チェック結果から、機械学習や分析に使う特徴量データセットを作成するスクリプトです。

主な処理：

* 品質チェック結果CSV読み込み
* ElementId別集計CSV読み込み
* ElementIdごとの特徴量作成
* QualityScoreの付与
* FixPriority仮ラベルの作成

入力：

```text
04_output_csv/check_results_revit_v002.csv
04_output_csv/element_summary_v001.csv
```

出力：

```text
04_output_csv/bim_features_v001.csv
```

### `src/train_fix_priority_model.py`

特徴量データセットを使い、修正優先度分類プロトタイプを実行するスクリプトです。

主な処理：

* 特徴量CSV読み込み
* FixPriorityラベル確認
* 学習データ・テストデータ分割
* scikit-learnによる分類処理
* classification_report出力
* confusion_matrix出力
* predictions出力

入力：

```text
04_output_csv/bim_features_v001.csv
```

出力：

```text
04_output_csv/fix_priority_classification_report_v001.csv
04_output_csv/fix_priority_confusion_matrix_v001.csv
04_output_csv/fix_priority_predictions_v001.csv
```

### `src/calculate_ai_readiness_score.py`

AI Readiness Scoreを算出するスクリプトです。

主な処理：

* 品質チェック結果CSV読み込み
* Rule Master v003読み込み
* RuleIdをキーにAIReadinessImpactとAIReadinessPenaltyを結合
* ElementIdごとのAIReadinessPenalty合計
* AIReadinessScore算出
* AIReadinessLevel分類
* BlockingRuleIds整理
* HumanReviewRequired判定
* ElementId表示整形

入力：

```text
04_output_csv/check_results_revit_v002.csv
02_rule_master/bim_rule_master_v003.csv
```

出力：

```text
04_output_csv/ai_readiness_scores_v001.csv
```

### `src/generate_ai_context.py`

RuleId、違反内容、重大度、品質スコア、修正優先度、AI Readiness Scoreをもとに、生成AI向け構造化コンテキストを生成するスクリプトです。

主な処理：

* 品質チェック結果読み込み
* 特徴量データセット読み込み
* AI Readiness Score読み込み
* ElementIdごとのコンテキスト作成
* Summary作成
* JSON / Markdown出力
* AI向け指示条件の整理

入力：

```text
04_output_csv/check_results_revit_v002.csv
04_output_csv/bim_features_v001.csv
04_output_csv/ai_readiness_scores_v001.csv
```

出力：

```text
04_output_csv/ai_context_v002.json
04_output_csv/ai_context_v002.md
```

### `src/generate_fix_guide.py`

品質チェック結果、Rule Master v003、AI Readiness Scoreをもとに、修正ガイドMarkdownを生成するスクリプトです。

主な処理：

* 品質チェック結果読み込み
* Rule Master v003読み込み
* AI Readiness Score読み込み
* RuleIdをキーにAIReadinessImpactとAIReadinessPenaltyを結合
* ElementIdをキーにAI Readiness情報を結合
* Summary作成
* Blocking Rule Summary作成
* ElementId別Fix Guide作成
* Markdown出力

入力：

```text
04_output_csv/check_results_revit_v002.csv
02_rule_master/bim_rule_master_v003.csv
04_output_csv/ai_readiness_scores_v001.csv
```

出力：

```text
04_output_csv/fix_guides_v001.md
```

### `src/utils.py`

共通処理をまとめる補助スクリプトです。

主な処理候補：

* ファイルパス管理
* CSV読み込み共通関数
* CSV出力共通関数
* 文字列整形
* 欠損値判定

現時点では、主要処理は各スクリプト内で完結しています。

---

## Streamlit App

Streamlitは、PoCを画面で説明しやすくするための簡易UIです。

対象ファイル：

```text
app/streamlit_app.py
```

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

## 可視化

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

## Revit列マッピング

現時点のRevit由来データ対応は初期試作です。

`door_schedule_converted_v002.csv` では、列マッピングが一部仮設定です。

特に重要な点は以下です。

* `ElementId` は、Revit内部ElementIdではなく、建具表上の建具番号を仮IDとして使用しています。
* `FamilyName` は、Revitファミリ名ではなく、建具表上の種別記号 `SD` を仮格納しています。
* `TypeName` は、Revitタイプ名ではなく、設置場所・室名に近い列を仮格納しています。
* `Level` は現時点では空欄です。
* `BIM_ClassificationCode`、`BIM_ModelRole`、`BIM_Zone` は現時点では空欄です。

この仮マッピングは、品質チェック結果、AI Readiness Score、AI Context v002、Fix Guide Markdownに影響します。

今回のAI Readiness Assessment拡張では、正式なRevit内部情報の取得ではなく、仮マッピングを明文化し、PoCとしての前提条件と将来改善方針を説明できる状態にすることを目的としています。

詳細は以下に整理しています。

```text
docs/data_dictionary.md
docs/revit_schedule_column_mapping.md
```

---

## 現時点の注意点

現時点の制約と注意点は以下です。

* このPoCは個人開発の検証用PoCです。
* Revit由来データ対応は初期試作です。
* `door_schedule_converted_v002.csv` の列マッピングは仮設定です。
* `ElementId` はRevit内部ElementIdではなく、建具表上の建具番号を仮IDとして使用しています。
* `FamilyName` はRevitファミリ名ではなく、建具表上の種別記号 `SD` を仮格納しています。
* `TypeName` はRevitタイプ名ではなく、設置場所・室名に近い列を仮格納しています。
* `BIM_ClassificationCode`、`BIM_ModelRole`、`BIM_Zone` は現時点では空欄であり、未入力チェック対象として使用しています。
* `check_results_revit_v002.csv` の100件の違反は、正確な品質評価ではなく、処理フロー確認のための結果です。
* `QualityScore` はPoC用の簡易指標であり、正式な実務品質評価基準ではありません。
* `FixPriority` は実務の正解ラベルではなく、仮ラベルです。
* `AIReadinessScore` はPoC用の簡易指標であり、正式なAI活用準備度基準ではありません。
* `AIReadinessPenalty` はPoC用の仮設定であり、今後調整する前提です。
* `AI Context v002` は生成AIやRAGへ渡す前段階の構造化コンテキストであり、生成AI APIの呼び出しは未実装です。
* `Fix Guide Markdown` は生成AI APIではなく、RuleIdベースのテンプレート方式で生成しています。
* Revit API / pyRevit連携は未実装です。
* BIMモデルの自動修正は対象外です。
* 最終的な設計判断・モデル修正判断は人間が行う前提です。

---

## テスト実行結果

RuleIdベース品質チェックの基本動作を確認するため、`tests/test_quality_rules.py` を作成し、pytestで最小テストを実行しました。

確認した内容は以下です。

* `R-001`：必須パラメータ未入力を検出できるか
* `R-002`：分類コード未入力を検出できるか
* `R-003`：ファミリ命名規則違反を検出できるか
* 正常なファミリ名の場合、違反なしとして扱えるか
* 1要素に複数の違反がある場合、想定どおり検出できるか

実行コマンド：

```powershell
python -m pytest tests/test_quality_rules.py -v
```

実行結果：

```text
collected 5 items
5 passed
```

現時点では、`tests/test_quality_rules.py` はRuleIdベース品質チェックの期待動作を固定するための最小テストとして位置づけます。

AI Readiness Score、AI Context v002、Fix Guide Markdown生成に関するテストは今後追加予定です。

---

## 今後の拡張方針

今後の主な拡張方針は以下です。

1. AI Readiness Score関連のテストを追加する
2. AI Readiness Level分類のテストを追加する
3. Rule Master v003必須列確認のテストを追加する
4. AI Context v002生成結果の基本確認テストを追加する
5. Fix Guide Markdown生成結果の基本確認テストを追加する
6. GitHub公開範囲を確認する
7. Streamlit画面スクリーンショットを保存する
8. 必要に応じてポートフォリオPDF v003へ反映する
9. 将来的にRevit内部ElementId、FamilyName、TypeName、Level、RoomNameなどの正式取得を検討する
10. 将来的にpyRevit / Revit API連携を検討する

---

## 現時点の到達点

現時点では、Revit/BIMデータをPythonで処理し、品質チェック、品質メトリクス作成、特徴量作成、修正優先度分類プロトタイプ、AI Readiness Score、AI Context v002、Fix Guide Markdown生成、Streamlit簡易表示へ接続できる状態です。

具体的には、以下を確認済みです。

* Revit由来TXTをPython/pandasで読み込む
* 品質チェック用CSVへ変換する
* クレンジング済みCSVを作成する
* RuleIdベース品質チェックを実行する
* 品質チェック結果CSVを出力する
* 品質メトリクスを作成する
* 特徴量データセットを作成する
* 修正優先度分類プロトタイプを実行する
* AI Readiness Scoreを算出する
* AI Context v002を生成する
* Fix Guide Markdownを生成する
* Streamlitで各出力を確認する
* Revit列マッピングの仮設定と将来方針をdocsに整理する

このPoCにより、BIMデータをAI・機械学習・データ分析で扱うための前処理、ルールベース判定、品質メトリクス作成、特徴量設計、AI活用準備度評価、構造化コンテキスト生成、修正ガイド生成、簡易可視化までの一連の流れを説明できる状態になっています。
