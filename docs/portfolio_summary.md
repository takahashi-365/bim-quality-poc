# Portfolio Summary

## BIM Data Quality & AI Readiness Assessment PoC

## 概要

このPoCは、Revit/BIMデータをPythonで処理し、BIM品質ルールに基づく品質チェック、品質メトリクス作成、特徴量データセット作成、修正優先度分類プロトタイプ、AI Readiness Score算出、生成AI向け構造化コンテキスト生成、Fix Guide Markdown生成、Streamlitによる簡易可視化までを実装した個人開発PoCです。

第1段階では、Revit由来データをPython/pandasで読み込み、RuleIdベース品質チェック、QualityScore算出、特徴量設計、修正優先度分類プロトタイプ、生成AI向け構造化コンテキスト生成 v001 までを実装しました。

第2段階では、既存PoCを **BIM Data Quality & AI Readiness Assessment PoC** として再定義し、BIMデータがBI、機械学習、生成AI、将来的なRAGに活用できる状態かを評価する仕組みへ拡張しました。

本PoCは、AIモデルそのものの精度を追求するものではなく、建築BIMデータをAI・機械学習・生成AI・データ分析で扱える状態に整えるためのデータ品質評価パイプラインを構築することを目的としています。

---

## 背景

BIM導入支援やRevit運用支援の実務では、モデル内のパラメータ未入力、分類コード未入力、命名規則違反、属性情報のばらつきにより、集計、検索、品質管理、後工程確認、AI活用の精度が下がる課題があります。

BIMデータに未入力項目、分類コード不足、命名規則違反、属性情報のばらつきがある場合、そのままではBI、機械学習、生成AI、RAGなどに活用しにくくなります。

このPoCでは、そうしたBIMデータ品質の課題を、Pythonによるデータ処理、RuleIdベースの品質チェック、品質メトリクス作成、特徴量データセット作成、AI Readiness Score、AI Context v002、Fix Guide Markdown、Streamlit簡易可視化へ接続する形で検証しています。

---

## 実装済みの内容

現時点で実装済みの内容は以下です。

* Revit集計表TXTの書き出し確認
* Revit書き出しTXTのPython/pandas読み込み
* Revit書き出しTXTから品質チェック用CSVへの変換
* Revit由来CSVのクレンジング
* RuleId付きBIM品質ルールマスタの作成・整理
* Rule Master v003の作成
* Python/pandasによるBIM品質チェック
* 必須パラメータ未入力、分類コード未入力、ファミリ命名規則違反の検出
* RuleId、重大度、修正ガイド付きチェック結果CSVの出力
* 品質メトリクスCSVの作成
* RuleId別、Category別、ElementId別集計CSVの作成
* SeverityScore、QualityScoreの算出
* 特徴量データセットの作成
* FixPriority仮ラベルの作成
* scikit-learnによる修正優先度分類プロトタイプ
* AI Readiness Scoreの算出
* AI Readiness Levelの分類
* HumanReviewRequiredの判定
* AI Context JSON / Markdown v002の生成
* Fix Guide Markdownの生成
* StreamlitによるAI Readiness対応画面の作成
* pytestによる最小テスト
* Power BIによる補助的な初期ダッシュボード作成
* Revit列マッピングの仮設定整理
* data_dictionary.md、rule_specification.md、limitations.md、system_overview.md などの説明資料作成

---

## 主な成果物

主な成果物は以下です。

* `README.md`
* `requirements.txt`
* `02_rule_master/bim_rule_master_v002.csv`
* `02_rule_master/bim_rule_master_v003.csv`
* `03_input_csv/door_schedule_SD_export_test_v001.txt`
* `03_input_csv/door_schedule_converted_v002.csv`
* `03_input_csv/cleaned_bim_data_v001.csv`
* `04_output_csv/check_results_revit_v002.csv`
* `04_output_csv/quality_metrics_v001.csv`
* `04_output_csv/rule_summary_v001.csv`
* `04_output_csv/category_summary_v001.csv`
* `04_output_csv/element_summary_v001.csv`
* `04_output_csv/bim_features_v001.csv`
* `04_output_csv/fix_priority_classification_report_v001.csv`
* `04_output_csv/fix_priority_confusion_matrix_v001.csv`
* `04_output_csv/fix_priority_predictions_v001.csv`
* `04_output_csv/ai_readiness_scores_v001.csv`
* `04_output_csv/ai_context_v002.json`
* `04_output_csv/ai_context_v002.md`
* `04_output_csv/fix_guides_v001.md`
* `src/convert_revit_schedule.py`
* `src/clean_bim_data.py`
* `src/check_bim_quality.py`
* `src/calculate_quality_metrics.py`
* `src/create_bim_features.py`
* `src/train_fix_priority_model.py`
* `src/calculate_ai_readiness_score.py`
* `src/generate_ai_context.py`
* `src/generate_fix_guide.py`
* `app/streamlit_app.py`
* `tests/test_quality_rules.py`
* `docs/ai_readiness_assessment_plan.md`
* `docs/system_overview.md`
* `docs/data_dictionary.md`
* `docs/revit_schedule_column_mapping.md`
* `docs/rule_specification.md`
* `docs/limitations.md`
* `docs/evaluation_policy.md`
* `docs/portfolio_summary.md`

`.rvt` ファイル本体および `.pbix` ファイル本体は、容量・配布条件を考慮し、GitHub公開対象外としています。

---

## 処理フロー

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

---

## 使用技術

* Python 3.12.10
* pandas 2.3.3
* pytest 9.0.3
* Streamlit 1.52.1
* scikit-learn 1.8.0
* CSV / TXTデータ処理
* Revit集計表TXT書き出し
* RuleIdベース品質チェック
* JSON / Markdown Context Generation
* Power BI
* Markdown
* 生成AI向け構造化コンテキスト設計

---

## Streamlit簡易画面で確認できる内容

Streamlit簡易画面では、以下を確認できるようにしています。

* 品質メトリクス概要
* RuleId別違反件数
* Category別違反件数
* ElementId別品質スコア
* 特徴量データセット
* FixPriority件数
* 品質チェック結果一覧
* RuleId / Severity / Category によるフィルタ
* 修正優先度分類プロトタイプ結果
* AI Readiness Assessment
* AI Readiness Score概要
* AI Readiness Level別件数
* ElementId別AI Readiness Score
* AI活用を阻害しているRuleIdランキング
* Element Detail
* 生成AI向け構造化コンテキスト v002
* AI Context JSON / Markdown Preview
* Fix Guide Markdown Preview
* CSV / JSON / Markdown ダウンロード
* 現時点の注意点

この画面は、本格的な業務アプリではなく、面接・ポートフォリオ説明用のMVPとして位置づけています。

---

## QualityScoreの考え方

本PoCでは、BIM品質チェック結果をもとに、要素ごとの簡易品質スコアである `QualityScore` を作成しています。

初期設計では、100点を初期値とし、検出された違反の重大度に応じて減点します。

| Severity |  減点 |
| -------- | --: |
| High     | 10点 |
| Medium   |  5点 |
| Low      |  1点 |

計算式は以下です。

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

## FixPriority仮ラベルの考え方

本PoCでは、特徴量データセットに `FixPriority` を付与しています。

ただし、現時点の `FixPriority` は実務の正解ラベルではありません。

`QualityScore` と `HighViolationCount` をもとにした仮ラベルであり、修正優先度分類プロトタイプへ接続するための初期設計です。

現時点の初期データでは、全25要素の `FixPriority` が `High` になっています。

実務で修正優先度分類を行うには、以下のような教師データが必要です。

* 実際の修正履歴
* 修正にかかった時間
* 修正工数
* 手戻り発生有無
* 担当者の判断結果
* 設計・施工上の影響度
* プロジェクト条件
* BIM実行計画上の重要度
* 発注者要件
* 後工程での利用有無

---

## AI Readiness Scoreの考え方

本PoCでは、BIMデータがAIやデータ活用に使いやすい状態かを評価する簡易スコアとして `AIReadinessScore` を追加しています。

AI Readiness Scoreは、以下の観点をRuleIdベースで評価します。

* 必須属性が入力されているか
* 分類コードが入力されているか
* 命名規則が一定のルールに沿っているか
* AIやBIで検索・分類・集計しやすい状態か
* 人間確認が必要な状態か

初期計算式は以下です。

```text
AIReadinessScore = 100 - AIReadinessPenalty合計
```

初期レベル分類は以下です。

| AIReadinessScore | AIReadinessLevel |
| ---------------- | ---------------- |
| 80-100           | High             |
| 60-79            | Medium           |
| 0-59             | Low              |

今回の初期データでは、全25要素が以下の結果となっています。

```text
AIReadinessScore = 40
AIReadinessLevel = Low
HumanReviewRequired = True
```

これは、各要素に必須パラメータ未入力、分類コード未入力、ファミリ命名規則違反が含まれているためです。

この結果は、BIMデータをAIやBIに活用する前に、属性情報、分類コード、命名規則の整備が必要であることを示すPoC結果として扱います。

---

## AI Context v002の考え方

AI Context v002では、BIM品質チェック結果、特徴量データセット、AI Readiness Scoreをもとに、生成AIへ渡すための参照情報をJSON / Markdown形式で整理しています。

出力ファイルは以下です。

* `04_output_csv/ai_context_v002.json`
* `04_output_csv/ai_context_v002.md`

AI Context v002には、主に以下を含めています。

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

現時点では、OpenAI APIなどの生成AI APIは呼び出していません。

生成AIに自由回答させるのではなく、RuleId、品質チェック結果、QualityScore、FixPriority、AIReadinessScore、HumanReviewRequiredなどを明示的に渡す前処理として位置づけています。

---

## Fix Guide Markdownの考え方

Fix Guide Markdownでは、品質チェック結果、Rule Master v003、AI Readiness Scoreをもとに、RuleIdベースの修正方針をMarkdownとして出力しています。

出力ファイルは以下です。

* `04_output_csv/fix_guides_v001.md`

Fix Guide Markdownには、主に以下を含めています。

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

この処理では、生成AI APIは使用していません。

RuleIdベースのテンプレート方式で、人間確認向けの修正ガイドを生成しています。

---

## 現時点の位置づけ

現時点では、Revit由来データ対応は初期試作段階です。

Revit書き出しTXTをPythonで読み込み、品質チェック用CSVへ変換し、クレンジングしたうえで、RuleId付き品質チェック結果CSVを出力できることを確認しました。

さらに、品質チェック結果から品質メトリクスを作成し、ElementId別品質スコア、特徴量データセット、FixPriority仮ラベルを作成しました。

修正優先度分類プロトタイプ、AI Readiness Score、AI Context v002、Fix Guide Markdown、StreamlitでのAI Readiness表示も実装済みです。

ただし、現時点の列マッピングは仮設定であり、出力された違反件数やAI Readiness Scoreは、正確な実務品質評価ではなく、Revit由来データでも一連の処理フローが動くことを確認するための検証結果です。

生成AI APIの呼び出しは行っておらず、AIに渡す参照情報をJSON / Markdown形式で整理する前処理として位置づけています。

Revit API / pyRevit連携は未実装であり、今後の拡張候補として検討しています。

---

## 制約・注意点

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
* `AIReadinessPenalty` はPoC用の仮設定であり、今後調整する前提です。
* `AI Context v002` は生成AIやRAGへ渡す前段階の構造化コンテキストであり、生成AI APIの呼び出しは未実装です。
* `Fix Guide Markdown` は生成AI APIではなく、RuleIdベースのテンプレート方式で生成しています。
* Revit APIやpyRevitとの直接連携は未実装です。
* RevitモデルやBIMデータの自動修正は対象外です。
* 設計判断、施工判断、モデル修正の最終判断は人間が行う前提です。

---

## 今後の拡張予定

### Tests

* AI Readiness Score計算のテスト追加
* AI Readiness Level分類のテスト追加
* Rule Master v003必須列確認のテスト追加
* AI Context v002生成結果の基本確認テスト追加
* Fix Guide Markdown生成結果の基本確認テスト追加

### Revit / BIM Integration

* Revit集計表の列マッピング精度向上
* Revit内部ElementId、FamilyName、TypeName、Level、RoomNameの取得確認
* pyRevit連携の検討
* Revit API連携の検討

### Streamlit / Visualization

* Streamlit画面スクリーンショットの保存
* 必要に応じたタブ分けやElementId別表示の改善
* AI Readiness表示の見せ方改善
* Fix Guide Previewの表示改善

### Portfolio

* GitHub公開範囲の確認
* ポートフォリオPDF v003の作成検討
* AI Readiness Assessment拡張内容の説明反映
* 面接用説明文の整理

---

## Revit API / pyRevit連携検討

現時点では、Revit API / pyRevit連携は未実装です。

現在は、Revit書き出しTXTを入力として、Python/pandasによる品質チェック、品質メトリクス作成、特徴量データセット作成、修正優先度分類プロトタイプ、AI Readiness Score、AI Context v002、Fix Guide Markdown生成までを検証しています。

今後の拡張候補として、Revit APIまたはpyRevitを用いて、Revitモデル内のElementId、Category、FamilyName、TypeName、Level、RoomName、各種パラメータ情報を直接取得し、既存のPython品質チェック処理へ接続する構成を検討しています。

ただし、初期段階ではBIMモデルの自動修正は対象外とし、情報取得、品質チェック、修正候補の提示、人間による確認を前提とします。

詳細は `docs/revit_api_pyrevit_integration_plan.md` に整理しています。

---

## ポートフォリオで伝えたいこと

このPoCでは、BIM/Revit導入支援の経験をもとに、建築BIMデータをPythonで処理し、品質評価、品質メトリクス作成、特徴量設計、AI Readiness Score、AI Context v002、Fix Guide Markdown、Streamlit簡易可視化、機械学習プロトタイプ、生成AI活用前処理へ接続するためのデータ処理パイプラインを構築しています。

単なるBIM品質チェックツールではなく、BIMデータをAI・機械学習・生成AI・データ分析で扱える状態に整えるための、BIMデータ品質・AI活用準備度評価PoCとして位置づけています。

本PoCで重視しているのは、AIモデルそのものの精度ではなく、AI・機械学習・生成AIが扱える建築BIMデータをどのように整備するかという点です。

そのため、BIM導入支援で扱ってきた品質ルールや運用ルールをRuleIdとして整理し、Pythonで処理可能なデータとして扱えるようにしています。

さらに、RuleId、品質チェック結果、QualityScore、FixPriority、AIReadinessScore、HumanReviewRequired、FixGuideを構造化し、AIに渡す前段階の参照情報として整理する設計にしています。

---

## ポートフォリオでの説明文

本PoCは、BIM/Revit導入支援の実務経験をもとに、建築BIMデータをAI・機械学習・データ分析・生成AI活用で扱うための前処理、品質評価、特徴量設計、AI Readiness Assessment、生成AI連携前処理までを検証する個人開発PoCです。

単なるBIM品質チェックツールではなく、Revit/BIMデータをPythonで読み込み、データクレンジング、RuleIdベースの品質チェック、品質メトリクス作成、特徴量データセット作成、AI Readiness Score算出、AI Context v002生成、Fix Guide Markdown生成、Streamlit簡易可視化へ接続するためのデータ処理パイプラインとして設計しています。

初期段階では、BIM品質チェック用の検証CSVを作成し、Python/pandasを用いて、必須パラメータ未入力、分類コード未入力、ファミリ命名規則違反をRuleId付きで検出する品質チェックツールを実装しました。

その後、Revitから書き出した集計表TXTをPython/pandasで読み込み、品質チェック用CSVへ変換し、クレンジングしたうえで、RuleId付き品質チェック結果CSVを出力するフローを実装しました。

さらに、品質チェック結果から品質メトリクス、ElementId別品質スコア、特徴量データセット、FixPriority仮ラベルを作成し、scikit-learnによる修正優先度分類プロトタイプへ接続しました。

第2段階では、Rule Master v003、AI Readiness Score、AI Context v002、Fix Guide Markdown、Streamlit上でのAI Readiness表示を追加しました。

AI Readiness Scoreでは、BIMデータがBI、機械学習、生成AI、将来的なRAGに活用できる状態かを、RuleIdベースで簡易評価しています。

AI Context v002では、RuleId、違反内容、重大度、品質スコア、修正優先度、AI Readiness Score、人間確認要否を含むJSON / Markdownを生成し、生成AIやRAGへ渡す前段階の構造化コンテキストとして整理しています。

Fix Guide Markdownでは、品質チェック結果、Rule Master v003、AI Readiness Scoreをもとに、RuleIdベースの修正方針を人間確認向けに出力しています。

現時点では、Revit由来データの列マッピングは仮設定であり、出力された違反件数やAI Readiness Scoreは正確な実務評価ではなく、Revit由来データでも一連の処理フローが動くことを確認するための検証結果です。

本PoCで重視しているのは、AIモデルそのものの精度ではなく、AI・機械学習・生成AIが扱える建築BIMデータをどのように整備するかという点です。

BIMデータは、未入力項目、分類コード不足、命名規則違反、属性情報のばらつきがあると、集計、検索、BI、機械学習、生成AI、RAGなどに活用しにくくなります。

そのため、本PoCでは、BIM導入支援で扱ってきた品質ルールや運用ルールをRuleIdとして整理し、Pythonで処理可能なデータとして扱えるようにしました。

RuleIdは、品質チェック結果CSV、品質メトリクス、特徴量データセット、AI Readiness Score、AI Context v002、Fix Guide Markdown、Streamlit簡易画面を接続するための共通キーとして利用しています。

生成AI連携については、現時点ではOpenAI APIなどを直接呼び出さず、RuleId、違反内容、重大度、修正提案、品質スコア、修正優先度、AI Readiness Score、人間確認要否などをJSONまたはMarkdown形式で構造化し、生成AIに渡す情報を制御する前処理として実装しています。

本PoCを通じて示したいことは、AIモデルをゼロから研究開発する力ではなく、建築情報・BIMデータ構造・BIM品質課題を理解したうえで、AIや機械学習が扱えるデータへ整備し、開発部門やAI活用プロジェクトへ接続できる力です。

BIM/Revit導入支援の経験を活かし、建築BIMデータをPythonで処理し、品質評価、品質メトリクス作成、特徴量設計、AI活用準備度評価、Streamlit簡易可視化、機械学習プロトタイプ、生成AI向け構造化コンテキスト生成へ接続できる、建設業界特化型のAI・データ分析エンジニア候補としてのポートフォリオに位置づけています。

---

## 面接での説明用メモ

AIモデルそのものをゼロから研究開発する経験はまだありません。

ただし、BIM導入支援の実務経験をもとに、Revit/BIMデータをAI・機械学習で扱うための前処理、品質評価、品質メトリクス作成、特徴量設計、AI Readiness Score、Streamlit簡易可視化、修正優先度分類プロトタイプ、生成AI向け構造化コンテキスト生成、Fix Guide Markdown生成までを個人PoCとして設計・実装しています。

建築情報の構造やBIMデータ品質の課題を理解しているため、単にAIを使うだけでなく、AIが使える建築データをどう作るかという部分から貢献できます。

また、生成AIに自由判断させるのではなく、RuleId、品質チェック結果、QualityScore、AIReadinessScore、HumanReviewRequired、FixGuideなどを構造化し、AIへ渡す情報を制御する設計を重視しています。

---

## 職務経歴書向け要約

個人開発として、Revit/BIMデータを対象にした `BIM Data Quality & AI Readiness Assessment PoC` を構築中。

Python/pandasでRevit集計表データを読み込み、品質チェック用CSVへ変換し、データクレンジング、RuleIdベースの品質チェック、品質メトリクス作成、特徴量データセット作成、修正優先度分類プロトタイプ、AI Readiness Score算出、AI Context v002生成、Fix Guide Markdown生成、Streamlit簡易可視化までを実装。

現時点では、生成AI APIは呼び出さず、RuleId、違反内容、重大度、品質スコア、修正優先度、AI Readiness Score、人間確認要否を含むJSON / Markdownを生成し、生成AIやRAGへ渡す前段階の構造化コンテキストとして整理している。

BIM導入支援の実務経験をもとに、建築BIMデータをAI・機械学習・データ分析・生成AI活用で扱うためのデータ処理パイプラインを個人PoCとして構築している。
