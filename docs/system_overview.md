# System Overview

## BIM Data Quality & AI Readiness Assessment PoC

## この資料の目的

この資料は、`BIM Data Quality & AI Readiness Assessment PoC`の現在のシステム構成、処理フロー、各Pythonファイルの役割を整理するためのものです。

各資料の位置づけは以下です。

* `README.md`：PoC全体の入口
* `docs/portfolio_summary.md`：ポートフォリオ説明用の要約
* `docs/system_overview.md`：現在のシステム構成と処理フロー
* `docs/data_dictionary.md`：主要な列・データ項目の定義
* `docs/revit_schedule_column_mapping.md`：初期試作時のRevit列マッピング
* `docs/limitations.md`：制約・未実装範囲

本資料では、過去の試作と現在の正式なGit管理対象コードを区別して説明します。

---

## PoC全体の目的

このPoCは、Revit/BIM由来データをPythonで処理し、以下へ接続するデータ処理パイプラインを検証するものです。

* データクレンジング
* RuleIdベース品質チェック
* 品質メトリクス作成
* 特徴量作成
* 修正優先度分類処理の試作
* AI Readiness Score算出
* Human Review判定
* 生成AI向け構造化コンテキスト生成
* Fix Guide Markdown生成
* Streamlit簡易可視化

単なるBIM品質チェックツールではなく、建築BIMデータをAI、機械学習、BI、生成AI、将来的なRAGで扱いやすい状態へ整えるためのPoCとして位置づけます。

---

## 第1段階と第2段階

### 第1段階

第1段階では、BIM品質チェックを中心に以下を作成しました。

* Revit由来データの読み込み試作
* 品質チェック用CSVへの変換試作
* データクレンジング
* RuleIdベース品質チェック
* QualityScore算出
* 品質メトリクス作成
* 特徴量データセット作成
* FixPriority仮ラベル作成
* scikit-learnによる分類処理経路の試作
* 生成AI向け構造化コンテキスト v001
* Streamlit簡易画面
* Power BI補助可視化

### 第2段階

第2段階では、PoCを以下へ拡張しました。

```text
BIM Data Quality & AI Readiness Assessment PoC
```

追加内容：

* Rule Master v003
* AI Readiness Score
* AI Readiness Level
* HumanReviewRequired
* AI Context JSON / Markdown v002
* Fix Guide Markdown
* Streamlit上のAI Readiness表示
* Revit列マッピングの制約整理
* AI Readiness関数のテスト
* 本番コードとテストコードの接続改善

---

## 過去の入力作成試作

初期試作では、以下の処理を行いました。

```text
Revit書き出しTXT
↓
08_python/convert_revit_schedule.py
↓
03_input_csv/door_schedule_converted_v002.csv
↓
src/clean_bim_data.py
↓
03_input_csv/cleaned_bim_data_v001.csv
```

`08_python/convert_revit_schedule.py`は、Revit書き出しTXTを品質チェック用CSVへ変換する試作コードです。

一方、`src/convert_revit_schedule.py`は正式実装として完成しておらず、0バイトの空ファイルだったため削除しました。

そのため、現在の`src`配下の正式なシステム構成には、Revit TXT変換スクリプトを含めていません。

---

## 現在の主要処理フロー

現在のGit管理対象パイプラインは、整形済みCSVを入力起点としています。

```text
03_input_csv/cleaned_bim_data_v001.csv
↓
1. src/check_bim_quality.py
   RuleIdベース品質チェック
↓
04_output_csv/check_results_revit_v002.csv
↓
2. src/calculate_quality_metrics.py
   品質メトリクス作成
↓
04_output_csv/quality_metrics_v001.csv
04_output_csv/rule_summary_v001.csv
04_output_csv/category_summary_v001.csv
04_output_csv/element_summary_v001.csv
↓
3. src/create_bim_features.py
   特徴量データセット作成
↓
04_output_csv/bim_features_v001.csv
↓
4. src/train_fix_priority_model.py
   修正優先度分類処理の試作
↓
04_output_csv/fix_priority_classification_report_v001.csv
04_output_csv/fix_priority_confusion_matrix_v001.csv
04_output_csv/fix_priority_predictions_v001.csv
↓
5. src/calculate_ai_readiness_score.py
   AI Readiness Score算出
↓
04_output_csv/ai_readiness_scores_v001.csv
↓
6. src/generate_ai_context.py
   生成AI向け構造化コンテキスト v002生成
↓
04_output_csv/ai_context_v002.json
04_output_csv/ai_context_v002.md
↓
7. src/generate_fix_guide.py
   Fix Guide Markdown生成
↓
04_output_csv/fix_guides_v001.md
↓
8. app/streamlit_app.py
   Streamlit簡易可視化
```

---

## 入力データ

### Revit書き出しTXT

```text
03_input_csv/door_schedule_SD_export_test_v001.txt
```

Revitのドア建具表をタブ区切りTXTとして書き出した検証用データです。

### 初期試作で変換したCSV

```text
03_input_csv/door_schedule_converted_v002.csv
```

初期試作の`08_python/convert_revit_schedule.py`で、Revit書き出しTXTから変換した検証CSVです。

この変換処理は現在の`src`配下の正式実装には含まれていません。

### 現在の主要入力CSV

```text
03_input_csv/cleaned_bim_data_v001.csv
```

現在の品質チェック処理は、この整形済みCSVを入力起点としています。

---

## ルール定義

### Rule Master v002

```text
02_rule_master/bim_rule_master_v002.csv
```

第1段階で作成した品質チェック用ルールマスタです。

### Rule Master v003

```text
02_rule_master/bim_rule_master_v003.csv
```

現在の品質チェックおよびAI Readiness処理で使用するルールマスタです。

v003では、品質ルールに加えて以下を管理します。

* `AIReadinessImpact`
* `AIReadinessPenalty`
* `TargetCategory`

現在の`src/check_bim_quality.py`と`src/calculate_ai_readiness_score.py`は、Rule Master v003を参照します。

---

## 初期ルール

| RuleId | 内容         | Severity | AIReadinessImpact |
| ------ | ---------- | -------- | ----------------- |
| R-001  | 必須パラメータ未入力 | High     | High              |
| R-002  | 分類コード未入力   | High     | High              |
| R-003  | ファミリ命名規則違反 | Medium   | Medium            |

---

## 出力データ

### 品質チェック結果

```text
04_output_csv/check_results_revit_v002.csv
```

主な列：

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

現在の検証結果：

```text
対象要素数：25
品質チェック結果：100件
```

RuleId別内訳：

| RuleId | 件数 |
| ------ | -: |
| R-001  | 50 |
| R-002  | 25 |
| R-003  | 25 |

### 品質メトリクス

```text
04_output_csv/quality_metrics_v001.csv
04_output_csv/rule_summary_v001.csv
04_output_csv/category_summary_v001.csv
04_output_csv/element_summary_v001.csv
```

主な内容：

* 総違反件数
* RuleId別件数
* Severity別件数
* Category別件数
* ElementId別件数
* SeverityScore
* QualityScore

### 特徴量データセット

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

### 修正優先度分類の試作出力

```text
04_output_csv/fix_priority_classification_report_v001.csv
04_output_csv/fix_priority_confusion_matrix_v001.csv
04_output_csv/fix_priority_predictions_v001.csv
```

現時点のFixPriorityは実務の正解ラベルではなく、ルールで作成した仮ラベルです。

また、現行サンプルは単一クラスであるため、分類性能の評価結果としては扱いません。

### AI Readiness Score

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

現在の検証結果：

```text
AIReadinessScore = 40
AIReadinessLevel = Low
HumanReviewRequired = True
```

全25要素が同じ結果です。

### AI Context v002

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

```text
04_output_csv/fix_guides_v001.md
```

主な内容：

* Summary
* Input Files
* AI Readiness Level Summary
* Blocking Rule Summary
* ElementId別Fix Guide
* Limitations

---

## Pythonファイル構成

### `src/clean_bim_data.py`

品質チェック前のBIMデータクレンジングを行います。

主な処理：

* 必要列の確認
* 不足列の空列追加
* 列順の標準化
* NaNの空文字化
* 前後スペース除去
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
* Rule Master v003読み込み
* 必須パラメータ未入力チェック
* 分類コード未入力チェック
* 命名規則チェック
* RuleId付き結果CSV出力

入力：

```text
03_input_csv/cleaned_bim_data_v001.csv
02_rule_master/bim_rule_master_v003.csv
```

出力：

```text
04_output_csv/check_results_revit_v002.csv
```

### `src/calculate_quality_metrics.py`

品質チェック結果から品質メトリクスを作成します。

主な処理：

* 総違反件数集計
* RuleId別集計
* Severity別集計
* Category別集計
* ElementId別集計
* SeverityScore算出
* QualityScore算出

### `src/create_bim_features.py`

品質チェック結果から特徴量データセットを作成します。

主な処理：

* ElementIdごとの特徴量作成
* QualityScore付与
* FixPriority仮ラベル作成

### `src/train_fix_priority_model.py`

修正優先度分類処理の試作を行います。

主な処理：

* 特徴量CSV読み込み
* FixPriorityラベル確認
* 学習・テストデータ分割
* scikit-learnによる分類処理
* classification_report出力
* confusion_matrix出力
* predictions出力

注意点：

現行データは単一クラスであるため、分類精度を示す実験ではありません。

データ構造と処理経路を確認するための試作です。

### `src/calculate_ai_readiness_score.py`

AI Readiness Scoreを算出します。

主要関数：

* `classify_ai_readiness_level`
* `calculate_ai_readiness_score`
* `is_human_review_required`
* `validate_columns`
* `validate_rule_master_v003_columns`
* `format_element_id`
* `main`

主な処理：

* 品質チェック結果読み込み
* Rule Master v003読み込み
* RuleIdをキーにペナルティ情報を結合
* ElementIdごとのペナルティ集計
* AIReadinessScore算出
* AIReadinessLevel分類
* HumanReviewRequired判定
* ElementId表示整形

### `src/generate_ai_context.py`

生成AI向け構造化コンテキストを生成します。

主な処理：

* 品質チェック結果読み込み
* 特徴量データセット読み込み
* AI Readiness Score読み込み
* ElementId別コンテキスト作成
* Summary作成
* JSON / Markdown出力
* AI向け指示条件整理

### `src/generate_fix_guide.py`

RuleIdベースのFix Guide Markdownを生成します。

主な処理：

* 品質チェック結果読み込み
* Rule Master v003読み込み
* AI Readiness Score読み込み
* RuleId情報結合
* ElementId別Fix Guide作成
* Markdown出力

---

## 削除した空ファイル

以下の2ファイルは0バイトであり、現在の本番コードから利用されていなかったため削除しました。

```text
src/convert_revit_schedule.py
src/utils.py
```

### `src/convert_revit_schedule.py`

過去の試作コードは`08_python/convert_revit_schedule.py`に存在します。

ただし、現在の正式な`src`実装としては扱いません。

### `src/utils.py`

共通処理は各スクリプト内に配置されており、`src/utils.py`は未使用でした。

今後、複数モジュールで同じ処理を共有する必要が生じた場合に、用途別の共通モジュールとして新規実装します。

---

## Streamlit App

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
* RuleId / Severity / Categoryフィルタ
* AI Readiness Assessment
* ElementId別AI Readiness Score
* Blocking RuleIdランキング
* Element Detail
* 修正優先度分類の試作出力
* AI Context JSON / Markdown Preview
* Fix Guide Markdown Preview
* 各種ダウンロード
* 制約・注意点

---

## Revit列マッピング

現在のRevit由来データ対応は初期試作です。

主な仮設定：

* `ElementId`：建具番号を仮IDとして使用
* `FamilyName`：種別記号`SD`を仮格納
* `TypeName`：設置場所・室名に近い列を仮格納
* `Level`：空欄
* `BIM_ClassificationCode`：空欄
* `BIM_ModelRole`：空欄
* `BIM_Zone`：空欄

この仮マッピングは、品質チェック結果、QualityScore、AI Readiness Score、AI Context、Fix Guideへ影響します。

詳細：

```text
docs/data_dictionary.md
docs/revit_schedule_column_mapping.md
```

---

## テスト

実行コマンド：

```powershell
python -m pytest -v
```

現在の結果：

```text
37 passed
```

主なテスト対象：

### 品質ルール

* R-001：必須パラメータ未入力
* R-002：分類コード未入力
* R-003：ファミリ命名規則違反
* 正常なFamilyName
* 1要素に複数違反がある場合

### AI Readiness

* High / Medium / Low分類
* ペナルティ減算
* 下限0点
* Human Review判定
* Rule Master v003必須列
* ElementId整形

### その他

* FixPriority学習データ
* pyRevitメタデータCSV
* Roomパイプライン

品質ルールとAI Readinessのテストは、本番コードを直接importして検証します。

---

## 現時点の制約

* 個人開発の検証用PoCです。
* 正式なRevit TXT変換処理は現在の`src`配下にありません。
* 現在の主要入力は整形済みCSVです。
* Revit列マッピングは仮設定です。
* 品質チェック100件は正式なモデル品質評価ではありません。
* QualityScoreはルールベースの簡易指標です。
* FixPriorityは仮ラベルです。
* FixPriorityデータは単一クラスです。
* AIReadinessScoreはルールベースの簡易指標です。
* AIReadinessPenaltyは仮設定です。
* AI Contextは生成AI API実行結果ではありません。
* Fix Guideはテンプレート方式です。
* Revitモデルの自動修正は対象外です。
* 最終判断は人間が行います。

---

## 今後の拡張方針

1. 一括実行パイプラインの作成
2. GitHub Actionsによるpytest自動実行
3. AI Context生成テスト
4. Fix Guide生成テスト
5. 品質メトリクス生成テスト
6. 特徴量生成テスト
7. 正式なRevit入力変換処理
8. pyRevit出力と品質チェック処理の接続
9. Revit API連携
10. 複数クラスのFixPriority教師データ作成
11. AI Readiness Penaltyの妥当性検証
12. Streamlit画面の改善
13. One-Pager・Portfolio PDFへの反映

---

## 現在の到達点

現時点では、整形済みBIMデータを入力として、以下を一連の流れとして説明・実行できる状態です。

* RuleIdベース品質チェック
* 品質チェック結果CSV出力
* 品質メトリクス作成
* 特徴量データセット作成
* 修正優先度分類処理の試作
* AI Readiness Score算出
* Human Review判定
* AI Context v002生成
* Fix Guide Markdown生成
* Streamlit簡易表示
* pytestによる本番関数の検証

また、過去の入力変換試作、現在の正式実装、未実装範囲を区別して説明できる構成へ改善しています。
