# July MVP Summary 260731

## BIM Data Quality Engineering & AI Analysis PoC

## この資料の目的

この資料は、7月時点での応募可能MVPとして、`BIM Data Quality Engineering & AI Analysis PoC` で実装・整理した内容を1枚で説明できるようにまとめるための資料です。

READMEやportfolio_summary.mdよりも短く、面接・ポートフォリオ・職務経歴書で説明しやすい要約資料として位置づけます。

---

## 1. 7月時点の位置づけ

7月時点では、Revit/BIMデータを対象にしたPythonデータ処理PoCとして、以下の流れを実装済みです。

```text
Revit書き出しTXT
↓
品質チェック用CSVへ変換
↓
データクレンジング
↓
RuleIdベース品質チェック
↓
品質チェック結果CSV出力
↓
品質メトリクス作成
↓
特徴量データセット作成
↓
Streamlit簡易画面で可視化
```

この状態により、単なる「AI勉強中」ではなく、BIM/RevitデータをPythonで処理し、品質評価、分析、特徴量設計、簡易UIまで接続した応募可能MVPとして説明できます。

---

## 2. 作成したもの

7月応募可能MVPとして、以下を作成・更新しました。

### Python処理

- `08_python/convert_revit_schedule.py`
- `src/clean_bim_data.py`
- `08_python/check_bim_quality.py`
- `src/calculate_quality_metrics.py`
- `src/create_bim_features.py`
- `app/streamlit_app.py`

### 入出力CSV

- `03_input_csv/door_schedule_converted_v002.csv`
- `03_input_csv/cleaned_bim_data_v001.csv`
- `04_output_csv/check_results_revit_v002.csv`
- `04_output_csv/quality_metrics_v001.csv`
- `04_output_csv/rule_summary_v001.csv`
- `04_output_csv/category_summary_v001.csv`
- `04_output_csv/element_summary_v001.csv`
- `04_output_csv/bim_features_v001.csv`

### ルール・テスト

- `02_rule_master/bim_rule_master_v002.csv`
- `tests/test_quality_rules.py`
- pytest実行結果：5 passed

### ドキュメント

- `README.md`
- `docs/portfolio_summary.md`
- `docs/system_overview.md`
- `docs/data_dictionary.md`
- `docs/rule_specification.md`
- `docs/limitations.md`
- `docs/business_requirements_mapping.md`
- `docs/evaluation_policy.md`
- `docs/streamlit_app_design.md`
- `docs/july_mvp_summary_260731.md`

---

## 3. 実装済みの主な機能

### Revit由来データ変換

Revitから書き出したドア建具表TXTをPython/pandasで読み込み、品質チェック用CSVへ変換しました。

現時点では列マッピングは仮設定ですが、Revit由来データをPython処理に接続する流れを確認済みです。

### データクレンジング

変換後CSVに対して、列順整理、空欄処理、前後スペース削除、ElementId空欄行除外、重複行除外を行う初期クレンジング処理を実装しました。

### RuleIdベース品質チェック

以下の品質ルールをRuleId付きで実装しました。

| RuleId | 内容 |
|---|---|
| R-001 | 必須パラメータ未入力 |
| R-002 | 分類コード未入力 |
| R-003 | ファミリ命名規則違反 |

品質チェック結果は、RuleId、RuleName、Severity、FixGuide付きのCSVとして出力しています。

### 品質メトリクス作成

品質チェック結果CSVから、以下の集計を作成しました。

- 総違反件数
- RuleId別違反件数
- Severity別違反件数
- Category別違反件数
- ElementId別違反件数
- SeverityScore
- QualityScore

### 特徴量データセット作成

品質チェック結果とElementId別集計から、機械学習や分析に使える特徴量データセットを作成しました。

主な特徴量は以下です。

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

### Streamlit簡易画面

Streamlitで、品質チェック結果、品質メトリクス、特徴量データセットを確認できる簡易画面を作成しました。

表示内容は以下です。

- 品質メトリクス概要
- RuleId別違反件数
- Category別違反件数
- ElementId別品質スコア
- 特徴量データセット
- FixPriority件数
- 品質チェック結果一覧
- RuleId / Severity / Category フィルタ
- CSVダウンロード

---

## 4. 7月MVPで示せること

このMVPでは、以下を示せます。

- Revit/BIMデータをPythonで読み込める
- Revit集計表TXTを品質チェック用CSVへ変換できる
- BIM品質ルールをRuleIdとして整理できる
- RuleIdベースで品質チェックを実装できる
- 品質チェック結果をCSVとして出力できる
- 品質メトリクスを作成できる
- 要素ごとのQualityScoreを作成できる
- 機械学習や分析に使える特徴量データセットを作成できる
- FixPriority仮ラベルを設計できる
- Streamlitで処理結果を簡易可視化できる
- BIMデータをAI・機械学習で扱うための前処理パイプラインを説明できる

---

## 5. 現時点の制約

現時点では、以下の制約があります。

- Revit由来データ対応は初期試作である
- `ElementId` はRevit内部ElementIdではなく、建具表上の建具番号を仮IDとして使用している
- `FamilyName` はRevitファミリ名ではなく、建具表上の種別記号を仮格納している
- `TypeName` はRevitタイプ名ではなく、設置場所・室名に近い列を仮格納している
- `BIM_ClassificationCode`、`BIM_ModelRole`、`BIM_Zone` は現時点では空欄であり、未入力チェック対象として使用している
- `QualityScore` はPoC用の簡易指標であり、実務上の正式な品質評価基準ではない
- `FixPriority` は実務の正解ラベルではなく、仮ラベルである
- 機械学習プロトタイプは未実装である
- 生成AI向け構造化コンテキスト生成は未実装である
- Revit APIやpyRevitとの直接連携は未実装である
- RevitモデルやBIMデータの自動修正は対象外である
- 設計判断、施工判断、モデル修正の最終判断は人間が行う前提である

---

## 6. 面接・ポートフォリオでの説明文

本PoCは、BIM/Revit導入支援の実務経験をもとに、建築BIMデータをAI・機械学習・データ分析で扱うための前処理、品質評価、特徴量設計、簡易可視化までを検証した個人開発PoCです。

Revitから書き出した集計表TXTをPython/pandasで読み込み、品質チェック用CSVへ変換したうえで、データクレンジング、RuleIdベース品質チェック、品質メトリクス作成、特徴量データセット作成、Streamlit簡易画面での可視化までを実装しました。

AIモデルの精度を高く見せることではなく、BIMデータをAI・機械学習・生成AIで扱える状態に整えるためのデータ処理パイプラインを構築することを目的としています。

今後は、scikit-learnによる修正優先度分類プロトタイプ、生成AI向け構造化コンテキスト生成、Revit API / pyRevit連携へ拡張する予定です。

---

## 7. 職務経歴書向け要約

個人開発として、Revit/BIMデータを対象にした `BIM Data Quality Engineering & AI Analysis PoC` を構築。

Python/pandasでRevit集計表TXTを読み込み、品質チェック用CSVへ変換し、データクレンジング、RuleIdベース品質チェック、品質メトリクス作成、特徴量データセット作成、Streamlit簡易可視化までを実装。

BIM導入支援の実務経験をもとに、建築BIMデータをAI・機械学習・データ分析で扱うための前処理パイプラインを個人PoCとして構築している。

---

## 8. 今後の拡張予定

7月応募可能MVPの次工程として、以下へ拡張します。

- scikit-learnによる修正優先度分類プロトタイプ
- classification_report、confusion_matrix、feature_importanceの出力
- 生成AI向け構造化コンテキスト生成
- RuleId、違反内容、重大度、品質スコア、修正優先度を含むJSON生成
- Streamlit画面の改善
- CSVアップロード機能
- Revit内部ElementId、FamilyName、TypeName、Levelの取得確認
- Revit API / pyRevit連携の検討
- GitHub公開用整理
- ポートフォリオPDF化
- 職務経歴書への反映

---

## 9. まとめ

7月時点では、Revit/BIMデータをPythonで処理し、品質チェック、品質メトリクス作成、特徴量データセット作成、Streamlit簡易可視化まで接続した応募可能MVPが完成しました。

このMVPにより、BIM導入支援の経験を、Python、データ処理、AI・機械学習活用前処理へ接続できることを示せます。

現時点では、実務適用可能な完成品ではなく、応募・面接で説明可能なPoC段階です。

ただし、単なる学習メモではなく、BIMデータをAI活用へ接続するための具体的な処理フロー、成果物、制約、今後の拡張方針を示せる状態になっています。
