# System Overview

## BIM Data Quality Engineering & AI Analysis PoC

## この資料の目的

この資料は、`BIM Data Quality Engineering & AI Analysis PoC` の全体構成、処理フロー、各Pythonファイルの役割を整理するためのものです。

READMEはPoC全体の説明、`portfolio_summary.md` はポートフォリオ用の要約、`system_overview.md` はシステム構成と処理の流れを説明する資料として位置づけます。

## PoC全体の目的

このPoCは、Revit/BIMデータをPythonで処理し、品質チェック、品質メトリクス作成、特徴量化、簡易機械学習、生成AI向け構造化コンテキスト生成へつなげるデータ処理パイプラインを検証するものです。

単なるBIM品質チェックツールではなく、建築BIMデータをAI・機械学習・データ分析で扱える状態に整えるための、BIMデータ品質エンジニアリングPoCとして位置づけます。

## 全体処理フロー

```text
Revit集計表TXT / CSV
↓
1. Revit/BIMデータ取り込み
↓
2. データクレンジング・列名標準化
↓
3. RuleIdベース品質チェック
↓
4. 品質チェック結果CSV出力
↓
5. 品質メトリクス作成
↓
6. 特徴量データセット作成
↓
7. 修正優先度分類モデル
↓
8. 生成AI向け構造化コンテキスト生成
↓
9. Power BI / Streamlitによる可視化
```

## 現時点で確認済みの処理フロー

現時点では、以下の最小ルートを確認済みです。

```text
Revit書き出しTXT
↓
convert_revit_schedule.py で品質チェック用CSVへ変換
↓
door_schedule_converted_v001.csv
↓
check_bim_quality.py で品質チェック
↓
check_results_revit_v001.csv を出力
```

確認済みの内容は以下です。

- Revit書き出しTXTをPython/pandasで読み込めること
- タブ区切りTXTを表データとして扱えること
- Revit書き出しTXTを品質チェック用CSVへ変換できること
- 変換後CSVを既存の品質チェックツールに入力できること
- RuleId付き品質チェック結果CSVを出力できること

## 入力データ

### Revit書き出しTXT

Revitから書き出した集計表データです。

現時点で確認済みのファイル：

- `03_input_csv/door_schedule_SD_export_test_v001.txt`
- `03_input_csv/material_schedule_export_test_v001.txt`
- `03_input_csv/room_finish_schedule_export_test_v001.txt`

### 品質チェック用サンプルCSV

Python品質チェックロジックの初期検証用として作成したCSVです。

- `03_input_csv/sample_bim_data_v001.csv`

### Revit由来変換CSV

Revit書き出しTXTを品質チェック用に変換したCSVです。

- `03_input_csv/door_schedule_converted_v001.csv`

現時点では、列マッピングは仮設定です。

## ルール定義

### RuleIdルールマスタ

BIM品質チェックルールをRuleIdで管理するためのCSVです。

- `02_rule_master/bim_rule_master_v001.csv`

主な役割：

- 品質チェックルールを外部CSVとして管理する
- Python品質チェックで参照する
- Power BI可視化でRuleIdを使う
- RuleId検索デモで参照する
- 生成AI向けプロンプト生成デモで参照する

初期ルール：

- R-001：必須パラメータ未入力
- R-002：分類コード未入力
- R-003：ファミリ命名規則違反

## 出力データ

### 品質チェック結果CSV

Python品質チェックによって出力されるCSVです。

- `04_output_csv/check_results_v001.csv`
- `04_output_csv/check_results_revit_v001.csv`

主な出力項目：

- CheckId
- ElementId
- Category
- FamilyName
- TypeName
- ParameterName
- CurrentValue
- RuleId
- RuleName
- Severity
- Status
- FixGuide
- DetectedAt
- SourceFile
- ModelName

### 今後追加予定の出力データ

今後、以下の出力を追加する予定です。

- `quality_metrics.csv`
- `bim_features.csv`
- `model_evaluation.txt`
- `confusion_matrix.csv`
- `feature_importance.csv`
- `fix_priority_predictions.csv`
- `ai_context.json`
- `ai_context.md`

## Pythonファイル構成

## 08_python / 06_ai_demo / src の役割整理

本PoCでは、Pythonコードの役割を以下のように整理します。

### 08_python

`08_python` は、5月〜6月前半の試作・検証コードを置く場所です。

主な役割は、Revit書き出しTXTの読み込み確認、品質チェック用CSVへの変換、RuleIdベース品質チェックの初期実装です。

主なファイル：

- `test_read_revit_txt.py`
- `convert_revit_schedule_v001.py`
- `convert_revit_schedule.py`
- `check_bim_quality_v001.py`
- `check_bim_quality.py`

現時点では、Revit由来データ処理と品質チェックの流れを確認するための試作コードとして位置づけます。

### 06_ai_demo

`06_ai_demo` は、RuleId検索と生成AI活用に関するデモコードを置く場所です。

主な役割は、RuleIdを起点にルール情報を検索し、業務影響、AI活用時の影響、修正方針を確認できるようにすることです。

主なファイル：

- `ruleid_lookup_demo.py`
- `ruleid_prompt_generator_demo.py`
- `generated_prompts/`

現時点では、生成AI向け構造化コンテキスト生成へ発展させる前段階のデモとして位置づけます。

### src

`src` は、今後の本実装用コードを置く場所です。

主な役割は、試作コードを整理し、データクレンジング、品質メトリクス作成、特徴量作成、機械学習プロトタイプ、生成AI向け構造化コンテキスト生成へ発展させることです。

主なファイル：

- `clean_bim_data.py`
- `convert_revit_schedule.py`
- `check_bim_quality.py`
- `calculate_quality_metrics.py`
- `create_bim_features.py`
- `train_fix_priority_model.py`
- `generate_ai_context.py`
- `utils.py`

今後は、`08_python` で検証した処理を必要に応じて `src` に移行し、再利用しやすい本実装コードとして整理します。

## src配下の予定ファイル

`src` 配下は、今後の本実装用Pythonファイルを置く場所です。

### `src/convert_revit_schedule.py`

Revit集計表TXT/CSVを読み込み、品質チェック用CSVへ変換するスクリプト。

主な処理予定：

- TXT/CSV読み込み
- 文字コード対応
- 区切り文字対応
- 列名標準化
- 必要列抽出
- 欠損値処理
- 品質チェック用CSV出力

### `src/clean_bim_data.py`

BIMデータのクレンジング処理を行うスクリプト。

主な処理予定：

- 不要行削除
- 空欄処理
- 型変換
- カテゴリ名の標準化
- ファイル名・モデル名の付与
- 品質チェック前のデータ整形

### `src/check_bim_quality.py`

RuleIdベースでBIM品質チェックを行う中心スクリプト。

主な処理予定：

- BIMデータCSV読み込み
- ルールマスタCSV読み込み
- 必須パラメータ未入力チェック
- 分類コード未入力チェック
- 命名規則チェック
- RuleId付きチェック結果CSV出力

### `src/calculate_quality_metrics.py`

品質チェック結果から品質メトリクスを作成するスクリプト。

主な処理予定：

- 総要素数の集計
- 違反件数の集計
- カテゴリ別違反数
- RuleId別違反数
- 重大度別違反数
- 品質スコア算出用の集計

### `src/create_bim_features.py`

BIM品質チェック結果から、機械学習や分析に使う特徴量データセットを作成するスクリプト。

主な特徴量候補：

- MissingFieldCount
- RuleViolationCount
- CriticalViolationCount
- WarningViolationCount
- HasClassificationCode
- FamilyNameValid
- SeverityScore
- QualityScore
- CategoryEncoded

### `src/train_fix_priority_model.py`

BIM品質チェック結果から作成した特徴量を使い、修正優先度分類モデルを作成するスクリプト。

主な処理予定：

- 特徴量CSV読み込み
- FixPriorityラベル作成
- 学習データ・テストデータ分割
- DecisionTreeClassifier
- RandomForestClassifier
- classification_report出力
- confusion_matrix出力
- feature_importance出力

### `src/generate_ai_context.py`

RuleId、違反内容、重大度、修正優先度をもとに、生成AI向け構造化コンテキストを生成するスクリプト。

主な処理予定：

- 品質チェック結果読み込み
- 修正優先度予測結果読み込み
- RuleIdルール情報の付与
- AIに渡すJSON/Markdown生成
- 参照情報を制御した生成AI活用前処理

### `src/utils.py`

共通処理をまとめる補助スクリプト。

主な処理予定：

- ファイルパス管理
- CSV読み込み共通関数
- CSV出力共通関数
- ログ出力
- 文字列整形
- 欠損値判定

## 既存実装ファイル

現時点では、既存の初期実装は以下にあります。

- `08_python/check_bim_quality.py`
- `08_python/convert_revit_schedule.py`
- `08_python/test_read_revit_txt.py`
- `06_ai_demo/ruleid_lookup_demo.py`
- `06_ai_demo/ruleid_prompt_generator_demo.py`

`src` 配下のファイルは、今後これらの既存実装を整理・発展させるための本実装予定ファイルとして作成しています。

## 可視化

### Power BI

現時点では、初期版としてPower BIダッシュボードを作成済みです。

- `05_powerbi/bim_quality_dashboard_v001.pbix`

主な可視化内容：

- 総違反件数
- RuleId別違反件数
- Severity別違反件数
- Category別違反件数
- 違反一覧

### Streamlit

今後、PoCを画面で説明しやすくするために、Streamlit簡易UIを作成する予定です。

想定機能：

- CSVアップロード
- 品質チェック実行
- 品質メトリクス表示
- 特徴量表示
- 修正優先度予測表示
- 生成AI向け構造化コンテキスト表示
- CSV/JSONダウンロード

## 現時点の注意点

現時点のRevit由来データ対応は初期試作です。

`door_schedule_converted_v001.csv` では、列マッピングが仮設定です。

特に、以下は今後確認が必要です。

- 元TXTのどの列が `ElementId` に相当するか
- 元TXTのどの列が `FamilyName` に相当するか
- 元TXTのどの列が `TypeName` に相当するか
- Revit集計表側で必要な列を追加する必要があるか
- 品質チェック用CSVとして必要な列が揃っているか

また、現時点の `check_results_revit_v001.csv` は、正確な品質評価ではなく、Revit由来データでも一連の処理フローが動くことを確認するための検証です。

## テスト実行結果

RuleIdベース品質チェックの基本動作を確認するため、`tests/test_quality_rules.py` を作成し、pytestで最小テストを実行しました。

確認した内容は以下です。

- `R-001`：必須パラメータ未入力を検出できるか
- `R-002`：分類コード未入力を検出できるか
- `R-003`：ファミリ命名規則違反を検出できるか
- 正常なファミリ名の場合、違反なしとして扱えるか
- 1要素に複数の違反がある場合、想定どおり検出できるか

実行コマンド：

`python -m pytest tests/test_quality_rules.py -v`

実行結果：

- collected 5 items
- 5 passed

現時点では、`tests/test_quality_rules.py` は本実装関数を直接テストするものではなく、RuleIdベース品質チェックの期待動作を固定するための最小テストとして位置づけます。

今後、`src/check_bim_quality.py` へ本実装を移行した後、このテストを本実装関数に接続します。

## 今後の拡張方針

1. Revit集計表の列マッピングを整理する
2. `convert_revit_schedule.py` をv0.2化する
3. `check_bim_quality.py` をv0.2化する
4. 品質メトリクスを作成する
5. 特徴量データセットを作成する
6. 修正優先度分類モデルを作成する
7. 生成AI向け構造化コンテキストを生成する
8. Streamlitで簡易UI化する
9. ポートフォリオPDFや職務経歴書に反映する

## 5月時点の到達点

5月時点では、PoC名、README、ディレクトリ構成、サンプルデータ、RuleIdルールマスタ、初期Python実装、Revit由来データ対応の初期試作、ポートフォリオ要約、システム概要を作成しました。

Revit/BIMデータをPythonで処理し、品質チェック、特徴量作成、機械学習、生成AI向け構造化コンテキスト生成へ拡張できる土台を作成した状態です。