# Portfolio Summary

## BIM Data Quality & AI Readiness Assessment PoC

## 概要

このPoCは、Revit/BIM由来のデータをPythonで処理し、BIM品質ルールに基づく品質チェック、品質メトリクス作成、特徴量データセット作成、修正優先度分類の試作、AI Readiness Score算出、生成AI向け構造化コンテキスト生成、Fix Guide Markdown生成、Streamlitによる簡易可視化までを検証する個人開発PoCです。

本PoCは、AIモデルそのものの精度を追求することを主目的としていません。

建築BIMデータを、BI、機械学習、生成AI、将来的なRAGなどで扱える状態へ整えるために、以下を一連のデータ処理パイプラインとして整理することを目的としています。

* BIMデータの入力前提整理
* データクレンジング
* RuleIdベースの品質チェック
* 品質メトリクス作成
* 特徴量設計
* AI活用準備度のルールベース評価
* Human Reviewの明示
* 生成AIへ渡す前段階の構造化
* 修正方針の説明可能な出力
* 簡易UIによる可視化

---

## 背景

BIM導入支援やRevit運用支援の実務では、モデル内のパラメータ未入力、分類コード未入力、命名規則違反、属性情報のばらつきにより、次のような問題が発生します。

* 集計結果が安定しない
* 必要な要素を正しく検索できない
* 後工程での確認作業が増える
* BIや分析用データとして扱いにくい
* 機械学習用の特徴量を安定して作れない
* 生成AIへ渡す情報の信頼性が下がる
* RAGで正しい情報を検索しにくくなる
* 自動化前に人間による確認が必要な範囲が曖昧になる

このPoCでは、BIMデータ品質上の問題をRuleIdとして整理し、Pythonで処理可能な品質チェック結果、品質メトリクス、AI Readiness Score、HumanReviewRequired、AI Context、Fix Guideへ接続しています。

---

## PoCの位置づけ

### 第1段階

第1段階では、BIMデータ品質チェックを中心に、以下を作成しました。

* Revit由来データの読み込み試作
* データクレンジング
* RuleIdベース品質チェック
* QualityScore算出
* 品質メトリクス作成
* 特徴量データセット作成
* FixPriority仮ラベル作成
* scikit-learnによる修正優先度分類処理の試作
* 生成AI向け構造化コンテキスト v001
* Streamlit簡易画面
* Power BIによる補助可視化

### 第2段階

第2段階では、既存PoCを以下の名称へ再定義しました。

```text
BIM Data Quality & AI Readiness Assessment PoC
```

日本語名：

```text
BIMデータ品質・AI活用準備度評価PoC
```

第2段階では、次の内容を追加しました。

* Rule Master v003
* AI Readiness Score
* AI Readiness Level
* HumanReviewRequired
* AI Context JSON / Markdown v002
* Fix Guide Markdown
* Streamlit上でのAI Readiness表示
* Revit列マッピングの前提・制約整理
* pytestによるAI Readiness関数の検証
* 本番コードとテストコードの接続改善

---

## 現在の入力起点

初期試作では、Revit書き出しTXTをGit管理対象外の試作コードで変換しました。

初期試作時の流れ：

```text
Revit書き出しTXT
↓
08_python/convert_revit_schedule.py
↓
door_schedule_converted_v002.csv
↓
src/clean_bim_data.py
↓
cleaned_bim_data_v001.csv
```

ただし、`src/convert_revit_schedule.py`は正式な実装として完成しておらず、0バイトの空ファイルだったため削除しました。

現在のGit管理対象となる主要パイプラインは、次の整形済みCSVを入力起点としています。

```text
03_input_csv/cleaned_bim_data_v001.csv
```

したがって、現在の正式な処理フローは以下です。

```text
cleaned_bim_data_v001.csv
↓
src/check_bim_quality.py
↓
check_results_revit_v002.csv
↓
src/calculate_quality_metrics.py
↓
品質メトリクス・各種集計CSV
↓
src/create_bim_features.py
↓
bim_features_v001.csv
↓
src/train_fix_priority_model.py
↓
修正優先度分類の試作出力
↓
src/calculate_ai_readiness_score.py
↓
ai_readiness_scores_v001.csv
↓
src/generate_ai_context.py
↓
ai_context_v002.json
ai_context_v002.md
↓
src/generate_fix_guide.py
↓
fix_guides_v001.md
↓
app/streamlit_app.py
```

---

## 実装済みの内容

現時点で実装済みの内容は以下です。

* Revit集計表TXTの書き出し確認
* Revit書き出しTXTのPython/pandas読み込み試作
* 初期試作コードによるRevit書き出しTXTからCSVへの変換検証
* Revit由来CSVのクレンジング
* RuleId付きBIM品質ルールマスタの作成
* Rule Master v002の作成
* Rule Master v003の作成
* Python/pandasによるBIM品質チェック
* 必須パラメータ未入力の検出
* 分類コード未入力の検出
* ファミリ命名規則違反の検出
* RuleId、重大度、修正ガイド付きチェック結果CSVの出力
* 品質メトリクスCSVの作成
* RuleId別集計CSVの作成
* Category別集計CSVの作成
* ElementId別集計CSVの作成
* SeverityScoreの算出
* QualityScoreの算出
* 特徴量データセットの作成
* FixPriority仮ラベルの作成
* scikit-learnによる分類処理経路の試作
* AI Readiness Scoreの算出
* AI Readiness Levelの分類
* HumanReviewRequiredの判定
* AI Context JSON / Markdown v002の生成
* Fix Guide Markdownの生成
* StreamlitによるAI Readiness対応画面の作成
* Power BIによる補助的な初期ダッシュボード作成
* Revit列マッピングの仮設定整理
* pyRevitによるメタデータCSV出力の試作
* pytestによる品質ルール、AI Readiness、FixPriority学習データ、pyRevitメタデータCSV、Roomパイプラインの検証
* README、system_overview、data_dictionary、rule_specification、limitationsなどの説明資料作成

---

## 主な成果物

### ルールマスタ

* `02_rule_master/bim_rule_master_v002.csv`
* `02_rule_master/bim_rule_master_v003.csv`

### 入力データ

* `03_input_csv/door_schedule_SD_export_test_v001.txt`
* `03_input_csv/door_schedule_converted_v002.csv`
* `03_input_csv/cleaned_bim_data_v001.csv`

### 品質チェック・分析出力

* `04_output_csv/check_results_revit_v002.csv`
* `04_output_csv/quality_metrics_v001.csv`
* `04_output_csv/rule_summary_v001.csv`
* `04_output_csv/category_summary_v001.csv`
* `04_output_csv/element_summary_v001.csv`
* `04_output_csv/bim_features_v001.csv`

### 修正優先度分類の試作出力

* `04_output_csv/fix_priority_classification_report_v001.csv`
* `04_output_csv/fix_priority_confusion_matrix_v001.csv`
* `04_output_csv/fix_priority_predictions_v001.csv`

### AI Readiness・生成AI前処理出力

* `04_output_csv/ai_readiness_scores_v001.csv`
* `04_output_csv/ai_context_v002.json`
* `04_output_csv/ai_context_v002.md`
* `04_output_csv/fix_guides_v001.md`

### 主要Pythonコード

* `src/clean_bim_data.py`
* `src/check_bim_quality.py`
* `src/calculate_quality_metrics.py`
* `src/create_bim_features.py`
* `src/train_fix_priority_model.py`
* `src/calculate_ai_readiness_score.py`
* `src/generate_ai_context.py`
* `src/generate_fix_guide.py`
* `app/streamlit_app.py`

### テスト

* `tests/test_quality_rules.py`
* `tests/test_ai_readiness_score.py`
* `tests/test_fixpriority_training_data.py`
* `tests/test_pyrevit_metadata_csv.py`
* `tests/test_room_pipeline.py`

### 主な説明資料

* `README.md`
* `docs/system_overview.md`
* `docs/data_dictionary.md`
* `docs/revit_schedule_column_mapping.md`
* `docs/rule_specification.md`
* `docs/limitations.md`
* `docs/evaluation_policy.md`
* `docs/portfolio_summary.md`
* `docs/ai_readiness_assessment_plan.md`

`.rvt`ファイル本体および`.pbix`ファイル本体は、容量・配布条件を考慮し、GitHub公開対象外としています。

---

## 現在の主要処理フロー

```text
03_input_csv/cleaned_bim_data_v001.csv
↓
src/check_bim_quality.py
↓
04_output_csv/check_results_revit_v002.csv
↓
src/calculate_quality_metrics.py
↓
04_output_csv/quality_metrics_v001.csv
04_output_csv/rule_summary_v001.csv
04_output_csv/category_summary_v001.csv
04_output_csv/element_summary_v001.csv
↓
src/create_bim_features.py
↓
04_output_csv/bim_features_v001.csv
↓
src/train_fix_priority_model.py
↓
04_output_csv/fix_priority_classification_report_v001.csv
04_output_csv/fix_priority_confusion_matrix_v001.csv
04_output_csv/fix_priority_predictions_v001.csv
↓
src/calculate_ai_readiness_score.py
↓
04_output_csv/ai_readiness_scores_v001.csv
↓
src/generate_ai_context.py
↓
04_output_csv/ai_context_v002.json
04_output_csv/ai_context_v002.md
↓
src/generate_fix_guide.py
↓
04_output_csv/fix_guides_v001.md
↓
app/streamlit_app.py
```

---

## 使用技術

* Python 3.12.10
* pandas
* pytest
* Streamlit
* scikit-learn
* CSV / TXTデータ処理
* JSON
* Markdown
* Revit集計表TXT
* pyRevit試作
* Power BI
* RuleIdベース品質チェック
* 生成AI向け構造化コンテキスト設計

---

## テスト

現在、以下をpytestで検証しています。

* 品質ルール関数
* AI Readiness Score計算
* AI Readiness Level分類
* HumanReviewRequired判定
* Rule Master v003必須列確認
* ElementId表示整形
* FixPriority学習データの構造
* 必須列・必須値
* ラベルの許容値
* pyRevitメタデータCSV
* Roomパイプライン

実行コマンド：

```powershell
python -m pytest -v
```

現在の実行結果：

```text
37 passed
```

品質ルールとAI Readinessのテストは、テスト内に複製したロジックではなく、`src`配下の本番関数を直接importして検証する構成へ改善しています。

---

## Streamlit簡易画面で確認できる内容

* 品質メトリクス概要
* RuleId別違反件数
* Category別違反件数
* ElementId別品質スコア
* 特徴量データセット
* FixPriority件数
* 品質チェック結果一覧
* RuleId / Severity / Categoryによるフィルタ
* 修正優先度分類の試作結果
* AI Readiness Assessment
* AI Readiness Score概要
* AI Readiness Level別件数
* ElementId別AI Readiness Score
* AI活用を阻害しているRuleIdランキング
* Element Detail
* 生成AI向け構造化コンテキスト v002
* AI Context JSON / Markdown Preview
* Fix Guide Markdown Preview
* CSV / JSON / Markdownダウンロード
* 現時点の注意点

この画面は本格的な業務アプリではなく、面接・ポートフォリオ説明用のMVPとして位置づけています。

---

## QualityScoreの考え方

本PoCでは、BIM品質チェック結果をもとに、要素ごとの簡易品質スコアである`QualityScore`を作成しています。

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

このスコアは、統計的に妥当性が検証された正式な品質指標ではありません。

品質チェック結果を数値化し、集計、特徴量作成、Streamlit表示へ接続するための説明可能なルールベース指標です。

---

## FixPriorityの考え方

本PoCでは、特徴量データセットに`FixPriority`を付与しています。

ただし、現時点の`FixPriority`は実務の正解ラベルではありません。

`QualityScore`と`HighViolationCount`をもとにした仮ラベルであり、修正優先度分類の処理経路を試作するための初期設計です。

現行サンプルでは、全要素のラベルが`High`となっています。

そのため、scikit-learnによる処理を実装していても、現時点の出力は分類性能を示すものではありません。

実務で修正優先度分類を評価するためには、次のような複数クラスの教師データが必要です。

* 実際の修正履歴
* 修正工数
* 修正時間
* 手戻り発生有無
* 担当者の判断結果
* 設計・施工上の影響度
* 後工程への影響
* 発注者要件
* BIM実行計画上の重要度
* プロジェクト条件

---

## AI Readiness Scoreの考え方

本PoCでは、BIMデータがAIやデータ活用に使いやすい状態かを簡易評価するため、`AIReadinessScore`を作成しています。

評価観点：

* 必須属性が入力されているか
* 分類コードが入力されているか
* 命名規則が一定のルールに沿っているか
* BI、検索、分類、集計に利用しやすい状態か
* 人間確認が必要な状態か

初期計算式：

```text
AIReadinessScore = 100 - AIReadinessPenalty合計
```

初期レベル分類：

| AIReadinessScore | AIReadinessLevel |
| ---------------- | ---------------- |
| 80-100           | High             |
| 60-79            | Medium           |
| 0-59             | Low              |

今回の初期データでは、全25要素が次の結果です。

```text
AIReadinessScore = 40
AIReadinessLevel = Low
HumanReviewRequired = True
```

AIReadinessScoreは、Rule Masterに設定した仮ペナルティを用いる説明可能なルールベース指標です。

統計的に妥当性が検証された標準指標や、実務上の正式なAI活用準備度基準ではありません。

---

## AI Context v002の考え方

AI Context v002では、以下をJSON / Markdown形式で整理しています。

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

現時点ではOpenAI APIなどの生成AI APIは呼び出していません。

RuleId、品質チェック結果、QualityScore、FixPriority、AIReadinessScore、HumanReviewRequiredなどを明示的に構造化し、生成AIやRAGへ渡す前段階のデータとして位置づけています。

---

## Fix Guide Markdownの考え方

Fix Guide Markdownでは、品質チェック結果、Rule Master v003、AI Readiness Scoreをもとに、RuleIdベースの修正方針をMarkdownとして出力します。

主な内容：

* Summary
* Input Files
* AI Readiness Level Summary
* Blocking Rule Summary
* ElementId別Fix Guide
* Limitations

この処理では生成AI APIを使用していません。

RuleIdベースのテンプレート方式で、人間確認向けの修正ガイドを生成しています。

---

## Revit由来データの扱い

初期試作では、Revit書き出しTXTを`08_python/convert_revit_schedule.py`で変換し、検証用CSVを作成しました。

ただし、この変換処理は現在の`src`配下の正式実装には含めていません。

現在の主要パイプラインは、整形済みの`cleaned_bim_data_v001.csv`を入力起点としています。

また、現在の列マッピングには以下の仮設定があります。

* `ElementId`はRevit内部ElementIdではなく、建具番号を仮IDとして使用
* `FamilyName`は正式なRevitファミリ名ではなく、種別記号`SD`を仮格納
* `TypeName`は正式なRevitタイプ名ではなく、設置場所・室名に近い列を仮格納
* `Level`は空欄
* `BIM_ClassificationCode`は空欄
* `BIM_ModelRole`は空欄
* `BIM_Zone`は空欄

このため、品質チェック結果やAI Readiness Scoreは、正式な実務評価ではなく、処理フローを確認するための検証結果として扱います。

---

## Revit API / pyRevit連携

pyRevitによるメタデータCSV出力の試作は実施済みです。

一方、以下は未実装または未完成です。

* Revit APIからの正式な全項目取得
* pyRevit出力と主要品質チェックパイプラインの完全自動連携
* Revitモデル内での自動修正
* Revitモデルへ結果を書き戻す処理

今後は、Revit内部ElementId、UniqueId、Category、FamilyName、TypeName、Level、RoomName、各種パラメータを取得し、既存の品質チェック処理へ接続する構成を検討します。

---

## 制約・注意点

* 個人開発の検証用PoCです。
* 現在の主要パイプラインは整形済みCSVを入力起点とします。
* Revit TXT変換処理は初期試作であり、現在の正式な`src`実装には含めていません。
* Revit由来データの列マッピングは仮設定です。
* `ElementId`は正式なRevit内部ElementIdではありません。
* `FamilyName`は正式なRevitファミリ名ではありません。
* `TypeName`は正式なRevitタイプ名ではありません。
* `check_results_revit_v002.csv`の100件は、処理フロー確認のための結果です。
* `QualityScore`はPoC用のルールベース指標です。
* `FixPriority`は仮ラベルです。
* 現行FixPriorityデータは単一クラスであり、分類性能評価はできません。
* `AIReadinessScore`はPoC用のルールベース指標です。
* `AIReadinessPenalty`は仮設定です。
* `AI Context v002`は生成AIやRAGへ渡す前段階の構造化コンテキストです。
* `Fix Guide Markdown`はテンプレート方式です。
* 生成AI APIは呼び出していません。
* BIMモデルの自動修正は対象外です。
* 最終的な設計・施工・モデル修正判断は人間が行う前提です。

---

## 今後の拡張候補

### Data Pipeline

* Revit書き出しデータの正式な変換処理
* 入力ファイル・出力ファイル指定の整理
* 一括実行パイプライン
* 設定ファイル化
* エラーハンドリング強化

### Tests

* AI Context v002生成結果のテスト
* Fix Guide Markdown生成結果のテスト
* 品質メトリクス生成処理のテスト
* 特徴量生成処理のテスト
* 全体パイプラインの統合テスト
* GitHub Actionsによる自動テスト

### Revit / BIM Integration

* 正式なRevit内部ElementId取得
* UniqueId取得
* FamilyName取得
* TypeName取得
* Level取得
* RoomName取得
* pyRevit出力と品質チェックの自動接続
* Revit API連携

### Portfolio

* GitHub上の説明整合性確認
* One-Pager作成
* Portfolio PDF更新
* Streamlitスクリーンショット更新
* 面接用説明文の短縮・整理

---

## ポートフォリオで伝えたいこと

本PoCで示したいのは、AIモデルをゼロから研究開発する能力ではありません。

建築情報、BIMデータ構造、BIM品質上の問題を理解したうえで、AI、機械学習、BI、生成AI、RAGが扱いやすい形へデータを整理し、品質ルール、特徴量、Human Review、構造化コンテキストへ接続する能力です。

特に、以下を重視しています。

* BIM業務上の課題をデータ項目へ分解する
* 品質ルールをRuleIdとして外部管理する
* Pythonで再現可能なチェック処理を作る
* テストで期待動作を固定する
* AIへ渡す情報を構造化する
* 人間判断が必要な範囲を明示する
* PoCの制約や仮設定を隠さず説明する

---

## ポートフォリオ説明文

本PoCは、BIM/Revit導入支援の実務経験をもとに、建築BIMデータをAI・機械学習・データ分析・生成AI活用で扱うための前処理、品質評価、特徴量設計、AI Readiness Assessment、生成AI連携前処理までを検証する個人開発PoCです。

Python/pandasを用いて、整形済みBIMデータの読み込み、RuleIdベース品質チェック、品質メトリクス作成、特徴量データセット作成、AI Readiness Score算出、AI Context v002生成、Fix Guide Markdown生成、Streamlit簡易可視化へ接続しています。

AI Readiness Scoreは、Rule Masterに設定した仮ペナルティを用いる説明可能なルールベース指標であり、正式な標準指標ではありません。

また、FixPriority分類処理は実装していますが、現行サンプルは単一クラスであるため、分類精度を示す成果ではなく、データ設計と処理経路の試作として位置づけています。

本PoCで重視しているのは、AIモデルそのものの精度ではなく、AIや機械学習が扱える建築BIMデータをどのように整備し、品質ルール、Human Review、生成AI向け構造化コンテキストへ接続するかという点です。

---

## 職務経歴書向け要約

個人開発として、Revit/BIM由来データを対象とした`BIM Data Quality & AI Readiness Assessment PoC`を構築。

Python/pandasを用いて、整形済みBIMデータの読み込み、RuleIdベース品質チェック、品質メトリクス作成、特徴量データセット作成、修正優先度分類処理の試作、AI Readiness Score算出、AI Context JSON / Markdown生成、Fix Guide Markdown生成、Streamlit簡易可視化までを実装。

品質ルールおよびAI Readinessのテストを本番関数へ直接接続し、pytestで全37テストが成功する構成へ改善。

生成AI APIは直接呼び出さず、RuleId、違反内容、重大度、品質スコア、修正優先度、AI Readiness Score、人間確認要否をJSON / Markdownとして構造化し、生成AIやRAGへ渡す前段階のデータとして整理している。
