# Portfolio Summary

## BIM Data Quality Engineering & AI Analysis PoC

## 概要

このPoCは、Revit/BIMデータをPythonで処理し、BIM品質ルールに基づく品質チェック、品質メトリクス作成、特徴量データセット作成、Streamlitによる簡易可視化までを実装した個人開発PoCです。

目的は、建築BIMデータをAI・機械学習・データ分析で扱うために必要となる、データ整形、ルールベース判定、品質評価、品質スコア算出、特徴量設計、修正優先度分類プロトタイプ、生成AI連携前処理までの一連の流れを検証することです。

本PoCは、AIモデルそのものの精度を追求するものではなく、建築BIMデータをAI・機械学習・生成AIで扱える状態に整えるためのデータ処理パイプラインを構築することを目的としています。

---

## 背景

BIM導入支援やRevit運用支援の実務では、モデル内のパラメータ未入力、分類コード未入力、命名規則違反などにより、集計、検索、品質管理、後工程確認、AI活用の精度が下がる課題があります。

BIMデータに未入力項目、分類コード不足、命名規則違反、属性情報のばらつきがある場合、そのままではBI、機械学習、生成AI、RAGなどに活用しにくくなります。

このPoCでは、そうしたBIMデータ品質の課題を、Pythonによるデータ処理、RuleIdベースの品質チェック、品質メトリクス作成、特徴量データセット作成、Streamlit簡易可視化へ接続する形で検証しています。

---

## 7月応募可能MVP時点で実装済みの内容

- Revit集計表TXTの書き出し確認
- Revit書き出しTXTのPython/pandas読み込み
- Revit書き出しTXTから品質チェック用CSVへの変換
- Revit由来CSVのクレンジング
- RuleId付きBIM品質ルールマスタの作成・整理
- Python/pandasによるBIM品質チェック
- 必須パラメータ未入力、分類コード未入力、ファミリ命名規則違反の検出
- RuleId、重大度、修正ガイド付きチェック結果CSVの出力
- 品質メトリクスCSVの作成
- RuleId別、Category別、ElementId別集計CSVの作成
- SeverityScore、QualityScoreの算出
- 特徴量データセットの作成
- FixPriority仮ラベルの作成
- Streamlitによる簡易UI作成
- pytestによる最小テスト
- Power BIによる補助的な初期ダッシュボード作成
- RuleId検索デモの作成
- RuleIdベース生成AI向け構造化コンテキスト生成の前段階となるプロンプト生成デモの作成
- data_dictionary.md、rule_specification.md、limitations.md、evaluation_policy.md などの説明資料作成

---

## 主な成果物

- `README.md`
- `requirements.txt`
- `02_rule_master/bim_rule_master_v002.csv`
- `03_input_csv/door_schedule_SD_export_test_v001.txt`
- `03_input_csv/door_schedule_converted_v002.csv`
- `03_input_csv/cleaned_bim_data_v001.csv`
- `04_output_csv/check_results_revit_v002.csv`
- `04_output_csv/quality_metrics_v001.csv`
- `04_output_csv/rule_summary_v001.csv`
- `04_output_csv/category_summary_v001.csv`
- `04_output_csv/element_summary_v001.csv`
- `04_output_csv/bim_features_v001.csv`
- `05_powerbi/bim_quality_dashboard_v001.pbix`
- `06_ai_demo/ruleid_lookup_demo.py`
- `06_ai_demo/ruleid_prompt_generator_demo.py`
- `08_python/convert_revit_schedule.py`
- `08_python/check_bim_quality.py`
- `src/clean_bim_data.py`
- `src/calculate_quality_metrics.py`
- `src/create_bim_features.py`
- `app/streamlit_app.py`
- `tests/test_quality_rules.py`
- `docs/system_overview.md`
- `docs/data_dictionary.md`
- `docs/rule_specification.md`
- `docs/limitations.md`
- `docs/business_requirements_mapping.md`
- `docs/evaluation_policy.md`
- `docs/streamlit_app_design.md`
- `docs/portfolio_summary.md`

---

## 処理フロー

```text
Revit書き出しTXT
↓
Python/pandasで読み込み
↓
品質チェック用CSVへ変換
↓
Revit由来CSVをクレンジング
↓
RuleIdベース品質チェック
↓
品質チェック結果CSV出力
↓
品質メトリクス作成
↓
RuleId別・Category別・ElementId別集計
↓
QualityScore算出
↓
特徴量データセット作成
↓
FixPriority仮ラベル作成
↓
Streamlitによる簡易UI化
↓
Power BIによる補助的可視化
↓
今後、修正優先度分類プロトタイプと生成AI向け構造化コンテキスト生成へ拡張
```

---

## 使用技術

- Python 3.12.10
- pandas 2.3.3
- pytest 9.0.3
- Streamlit 1.52.1
- CSV / TXTデータ処理
- Revit集計表TXT書き出し
- RuleIdベース品質チェック
- Power BI
- Markdown
- 生成AI向けプロンプト設計
- 生成AI向け構造化コンテキスト生成の設計
- 将来的に scikit-learn
- 将来的に JSON / Markdown Context Generation

---

## Streamlit簡易画面で確認できる内容

7月応募可能MVPでは、Streamlit簡易画面を作成し、以下を確認できるようにしました。

- 品質メトリクス概要
- 総違反件数
- 違反要素数
- 要素あたり平均違反件数
- 平均QualityScore
- High / Medium / Low 違反件数
- RuleId別違反件数
- Category別違反件数
- ElementId別品質スコア
- 特徴量データセット
- FixPriority件数
- 品質チェック結果一覧
- RuleId / Severity / Category によるフィルタ
- CSVダウンロード
- 現時点の注意点

この画面は、本格的な業務アプリではなく、面接・ポートフォリオ説明用のMVPとして位置づけています。

---

## QualityScoreの考え方

本PoCでは、BIM品質チェック結果をもとに、要素ごとの簡易品質スコアである `QualityScore` を作成しています。

初期設計では、100点を初期値とし、検出された違反の重大度に応じて減点します。

| Severity | 減点 |
|---|---:|
| High | 10点 |
| Medium | 5点 |
| Low | 1点 |

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

実務で修正優先度分類を行うには、以下のような教師データが必要です。

- 実際の修正履歴
- 修正にかかった時間
- 修正工数
- 手戻り発生有無
- 担当者の判断結果
- 設計・施工上の影響度
- プロジェクト条件
- BIM実行計画上の重要度
- 発注者要件
- 後工程での利用有無

---

## 現時点の位置づけ

現時点では、Revit由来データ対応は初期試作段階です。

Revit書き出しTXTをPythonで読み込み、品質チェック用CSVへ変換し、クレンジングしたうえで、RuleId付き品質チェック結果CSVを出力できることを確認しました。

さらに、品質チェック結果から品質メトリクスを作成し、ElementId別品質スコア、特徴量データセット、FixPriority仮ラベルを作成しました。

Streamlit簡易画面により、これらの結果を画面で確認できる状態にしています。

ただし、現時点の列マッピングは仮設定であり、出力された違反件数は正確な品質評価ではなく、Revit由来データでも一連の処理フローが動くことを確認するための検証結果です。

また、修正優先度分類プロトタイプ、生成AI向け構造化コンテキスト生成、Revit API / pyRevit連携は今後の拡張予定です。

---

## 制約・注意点

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

---

## 今後の拡張予定

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

## ポートフォリオで伝えたいこと

このPoCでは、BIM/Revit導入支援の経験をもとに、建築BIMデータをPythonで処理し、品質評価、品質メトリクス作成、特徴量設計、Streamlit簡易可視化、機械学習プロトタイプ、生成AI活用へ接続するためのデータ処理パイプラインを構築しています。

単なるBIM品質チェックツールではなく、BIMデータをAI・機械学習で扱える状態に整えるための、BIMデータ品質エンジニアリングPoCとして位置づけています。

本PoCで重視しているのは、AIモデルそのものの精度ではなく、AI・機械学習・生成AIが扱える建築BIMデータをどのように整備するかという点です。

そのため、BIM導入支援で扱ってきた品質ルールや運用ルールをRuleIdとして整理し、Pythonで処理可能なデータとして扱えるようにしています。

---

## ポートフォリオでの説明文

本PoCは、BIM/Revit導入支援の実務経験をもとに、建築BIMデータをAI・機械学習・データ分析で扱うための前処理、品質評価、特徴量設計、生成AI連携前処理までを検証する個人開発PoCです。

単なるBIM品質チェックツールではなく、Revit/BIMデータをPythonで読み込み、データクレンジング、RuleIdベースの品質チェック、品質メトリクス作成、特徴量データセット作成、Streamlit簡易可視化、修正優先度分類プロトタイプ、生成AI向け構造化コンテキスト生成へ接続するためのデータ処理パイプラインとして設計しています。

初期段階では、BIM品質チェック用の検証CSVを作成し、Python/pandasを用いて、必須パラメータ未入力、分類コード未入力、ファミリ命名規則違反をRuleId付きで検出する品質チェックツールを実装しました。

その後、Revitから書き出した集計表TXTをPython/pandasで読み込み、品質チェック用CSVへ変換し、クレンジングしたうえで、RuleId付き品質チェック結果CSVを出力するフローを実装しました。

さらに、品質チェック結果から品質メトリクス、ElementId別品質スコア、特徴量データセット、FixPriority仮ラベルを作成し、Streamlit簡易画面で確認できるようにしました。

現時点では、Revit由来データの列マッピングは仮設定であり、出力された違反件数は正確な品質評価ではなく、Revit由来データでも一連の処理フローが動くことを確認するための検証結果です。

本PoCで重視しているのは、AIモデルそのものの精度ではなく、AI・機械学習・生成AIが扱える建築BIMデータをどのように整備するかという点です。

BIMデータは、未入力項目、分類コード不足、命名規則違反、属性情報のばらつきがあると、集計、検索、BI、機械学習、生成AI、RAGなどに活用しにくくなります。

そのため、本PoCでは、BIM導入支援で扱ってきた品質ルールや運用ルールをRuleIdとして整理し、Pythonで処理可能なデータとして扱えるようにしました。

RuleIdは、品質チェック結果CSV、品質メトリクス、特徴量データセット、Streamlit簡易画面、Power BIによる補助的可視化、RuleId検索デモ、生成AI向け構造化コンテキスト生成へ接続するための共通キーとして利用しています。

生成AI連携については、現時点ではOpenAI APIなどを直接呼び出さず、RuleIdをキーに該当ルールを取得し、生成AIに渡すためのプロンプトを生成する初期デモを作成しています。

このデモは、今後、RuleId、違反内容、重大度、修正提案、品質スコア、修正優先度などをJSONまたはMarkdown形式で構造化し、生成AIに渡す情報を制御する「生成AI向け構造化コンテキスト生成」へ発展させる前段階です。

今後は、修正優先度分類プロトタイプ、生成AI向け構造化コンテキスト生成、Revit API / pyRevit連携へ拡張していきます。

本PoCを通じて示したいことは、AIモデルをゼロから研究開発する力ではなく、建築情報・BIMデータ構造・BIM品質課題を理解したうえで、AIや機械学習が扱えるデータへ整備し、開発部門やAI活用プロジェクトへ接続できる力です。

BIM/Revit導入支援の経験を活かし、建築BIMデータをPythonで処理し、品質評価、品質メトリクス作成、特徴量設計、Streamlit簡易可視化、機械学習プロトタイプ、生成AI向け構造化コンテキスト生成へ接続できる、建設業界特化型のAI・データ分析エンジニア候補としてのポートフォリオに位置づけています。

---

## 面接での説明用メモ

AIモデルそのものをゼロから研究開発する経験はまだありません。

ただし、BIM導入支援の実務経験をもとに、Revit/BIMデータをAI・機械学習で扱うための前処理、品質評価、品質メトリクス作成、特徴量設計、Streamlit簡易可視化、修正優先度分類プロトタイプ、生成AI向け構造化コンテキスト生成までを個人PoCとして設計・実装しています。

建築情報の構造やBIMデータ品質の課題を理解しているため、単にAIを使うだけでなく、AIが使える建築データをどう作るかという部分から貢献できます。

---

## 職務経歴書向け要約

個人開発として、Revit/BIMデータを対象にした「BIM Data Quality Engineering & AI Analysis PoC」を構築中。

Python/pandasでRevit集計表データを読み込み、品質チェック用CSVへ変換し、データクレンジング、RuleIdベースの品質チェック、品質メトリクス作成、特徴量データセット作成、Streamlit簡易可視化までを実装。

現時点では、修正優先度分類プロトタイプに向けた `FixPriority` 仮ラベルを作成し、生成AI向け構造化コンテキスト生成の前段階として、RuleIdベースのプロンプト生成デモも作成している。

今後は、scikit-learnによる修正優先度分類プロトタイプ、生成AI向け構造化コンテキスト生成、Revit API / pyRevit連携へ拡張予定。

BIM導入支援の実務経験をもとに、建築BIMデータをAI・機械学習・データ分析で扱うためのデータ処理パイプラインを個人PoCとして構築している。
