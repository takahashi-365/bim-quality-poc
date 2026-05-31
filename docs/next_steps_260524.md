# Next Steps_260524

## BIM Data Quality Engineering & AI Analysis PoC

## この資料の目的

この資料は、`BIM Data Quality Engineering & AI Analysis PoC` の次工程を管理するためのタスク整理資料です。

READMEにはPoCの概要と実行方法を記載し、`system_overview.md` にはシステム構成と処理フローを記載します。

この `next_steps_260524.md` では、今後対応するタスク、優先順位、完了条件、後回しにする内容を整理します。

---

## 次工程の基本方針

次工程では、5月に作成した試作成果物をもとに、PoCを本実装・ポートフォリオ向けに整理します。

5月時点では、以下を確認済みです。

- Revit集計表TXTを書き出せること
- Revit書き出しTXTをPython/pandasで読み込めること
- Revit書き出しTXTを品質チェック用CSVへ変換できること
- 変換後CSVを既存の品質チェックツールに入力できること
- RuleId付き品質チェック結果CSVを出力できること
- Power BIで補助的に可視化できること
- RuleId検索デモを作成できたこと
- RuleIdベース生成AI向け構造化コンテキスト生成の前段階となるプロンプト生成デモを作成できたこと

次工程の目的は、機能を急に増やすことではありません。

主目的は、以下です。

- Revit由来データの列マッピングを整理する
- 5月試作コードを `src` 配下へ段階的に整理する
- データ辞書、RuleId仕様、Limitationsを作成する
- Revit由来データを安定してPython処理できる土台を作る
- 7月以降の品質メトリクス作成、特徴量設計、Streamlit化、機械学習プロトタイプへつなげる

---

## 現時点の前提

現時点のRevit由来データ対応は初期試作です。

`door_schedule_converted_v001.csv` の列マッピングは仮設定です。

`check_results_revit_v001.csv` の104件の違反は、現時点では正確な品質評価ではなく、処理フロー確認を目的とした結果です。

特に、以下の列が空欄になっているため、未入力違反が多く検出されています。

- BIM_ClassificationCode
- BIM_ModelRole
- BIM_Zone

そのため、次工程ではまず、Revit由来CSVの列マッピングとデータ定義を整理します。

---

## 優先順位サマリー

| 優先度 | タスク | 目的 |
|---|---|---|
| A | Revit由来CSVの列マッピング整理 | 後続処理の前提を固める |
| A | `08_python` / `06_ai_demo` / `src` の役割整理 | どれが試作でどれが本実装か明確にする |
| A | `data_dictionary.md` 作成 | データ項目の意味を整理する |
| A | `rule_specification.md` 作成 | RuleIdルールマスタの仕様を整理する |
| A | `limitations.md` 作成 | PoCの限界を明記する |
| B | `convert_revit_schedule.py` v0.2化 | Revit TXT変換処理を安定化する |
| B | `check_bim_quality.py` v0.2化 | 品質チェック処理を整理する |
| B | `business_requirements_mapping.md` 作成 | 実務課題とPoCの対応を整理する |
| B | `evaluation_policy.md` 作成 | 機械学習プロトタイプの評価方針を整理する |
| B | `tests/test_quality_rules.py` 作成 | 最小テストを追加する |
| C | 品質メトリクス作成 | 7月以降の分析基盤を作る |
| C | 特徴量設計 | 機械学習用データセットへ接続する |
| C | Streamlit簡易UI化 | PoCを画面で説明しやすくする |
| C | 生成AI向け構造化コンテキスト生成 | RuleIdをAI活用へ接続する |

---

# 優先度A：最優先タスク

## A-1. Revit由来CSVの列マッピング整理

### 対象ファイル

- `03_input_csv/door_schedule_SD_export_test_v001.txt`
- `03_input_csv/door_schedule_converted_v001.csv`
- `04_output_csv/check_results_revit_v001.csv`
- `08_python/convert_revit_schedule.py`

### 確認する主な列

- ElementId
- Category
- FamilyName
- TypeName
- Level
- BIM_ClassificationCode
- BIM_ModelRole
- BIM_Zone
- SourceFile
- ModelName

### やること

- Revit書き出しTXTの元列を確認する
- `door_schedule_converted_v001.csv` の列対応を確認する
- どの元列が `ElementId` に相当するか確認する
- どの元列が `FamilyName` に相当するか確認する
- どの元列が `TypeName` に相当するか確認する
- `Level` に相当する情報があるか確認する
- 品質チェックに必要な列が足りているか確認する
- 必要に応じてRevit集計表側に列を追加する
- 仮マッピングと正式マッピングを分けて記録する

### 完了条件

- Revit書き出しTXTのどの列を品質チェック用CSVのどの列に対応させるか整理できている
- `ElementId`、`Category`、`FamilyName`、`TypeName`、`Level` の扱い方が説明できる
- `BIM_ClassificationCode`、`BIM_ModelRole`、`BIM_Zone` が現時点で空欄である理由を説明できる
- `data_dictionary.md` に反映できる状態になっている

---

## A-2. `08_python` / `06_ai_demo` / `src` の役割整理

### 現状

現時点では、以下のようにフォルダが分かれています。

- `08_python/`
- `06_ai_demo/`
- `src/`

### 整理方針

| フォルダ | 役割 |
|---|---|
| `08_python/` | 5月時点のPython試作コード |
| `06_ai_demo/` | 5月時点のRuleId検索・生成AI向け説明生成デモ |
| `src/` | 今後の本実装用コード |
| `docs/` | 設計資料・ポートフォリオ説明資料 |
| `00_docs/` | 5月時点の設計メモ・コード説明メモ |

### やること

- READMEにフォルダ役割を明記する
- `system_overview.md` にフォルダ役割を明記する
- `08_python` は試作コードであると明記する
- `06_ai_demo` は5月時点のAI連携前処理デモであると明記する
- `src` は今後の本実装用であると明記する
- 既存コードをすぐに削除せず、段階的に `src` へ移行する方針にする

### 完了条件

- READMEを見れば、どのフォルダが何の役割か分かる
- `system_overview.md` を見れば、試作コードと本実装コードの関係が分かる
- 面接で「なぜ08_pythonとsrcが両方あるのか」を説明できる

---

## A-3. `data_dictionary.md` の作成

### 作成予定ファイル

- `docs/data_dictionary.md`

### 目的

Revit由来CSV、品質チェック用CSV、チェック結果CSVで使用する列の意味を整理する。

PoCが単なるCSV処理ではなく、BIMデータをAI・機械学習で扱うためのデータ設計を行っていることを示す。

### 定義する主な項目

- ElementId
- Category
- FamilyName
- TypeName
- Level
- BIM_ClassificationCode
- BIM_ModelRole
- BIM_Zone
- SourceFile
- ModelName
- CheckId
- ParameterName
- CurrentValue
- RuleId
- RuleName
- Severity
- Status
- FixGuide
- DetectedAt

### やること

- 各列の意味を定義する
- どのCSVに含まれる列か整理する
- データ型を整理する
- 必須項目か任意項目かを整理する
- 現時点で仮設定の項目を明記する
- Revit由来TXTの元列との対応が分かる場合は追記する

### 完了条件

- 品質チェック用CSVの各列の意味を説明できる
- チェック結果CSVの各列の意味を説明できる
- Revit由来CSVの列マッピングの現状が説明できる

---

## A-4. `rule_specification.md` の作成

### 作成予定ファイル

- `docs/rule_specification.md`

### 目的

RuleIdルールマスタの仕様を整理する。

RuleIdを中心に、品質チェック、補助的可視化、RuleId検索、生成AI向け構造化コンテキスト生成を接続する設計を明確にする。

### 整理する項目

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

### やること

- RuleId命名規則を整理する
- 初期ルール R-001、R-002、R-003 を説明する
- Severityの意味を整理する
- TargetFieldの意味を整理する
- CheckLogicの考え方を整理する
- BusinessImpactの使い方を整理する
- AIUseImpactの使い方を整理する
- FixGuideの書き方を整理する
- 今後追加するルールの方針を整理する

### 完了条件

- RuleIdルールマスタの各列の意味を説明できる
- R-001、R-002、R-003の違いを説明できる
- RuleIdをAI向け構造化コンテキストに使う理由を説明できる

---

## A-5. `limitations.md` の作成

### 作成予定ファイル

- `docs/limitations.md`

### 目的

5月時点のPoCの限界と注意点を明記する。

限界を明記することで、PoCの信頼性を上げる。

### 記載する内容

- Revit由来データ対応は初期試作である
- `door_schedule_converted_v001.csv` の列マッピングは仮設定である
- `check_results_revit_v001.csv` の104件の違反は正確な品質評価ではない
- 104件の違反は処理フロー確認のための結果である
- `BIM_ClassificationCode`、`BIM_ModelRole`、`BIM_Zone` が空欄のため、未入力違反が多く出ている
- 機械学習プロトタイプは未実装である
- 品質スコアは未実装である
- 修正優先度 High / Medium / Low は今後仮ラベルとして設計する
- 実務適用には、修正履歴、手戻り時間、担当者判断、プロジェクト条件、修正工数などの教師データが必要である
- 現時点ではOpenAI APIなどは直接呼び出していない
- Revit APIによる直接操作や自動修正は行っていない
- 設計判断、施工判断、モデル修正の最終判断は人間が行う前提である

### 完了条件

- READMEから詳細なLimitationsを切り出せる
- PoCの限界を面接で説明できる
- 104件の違反について誤解なく説明できる

---

# 優先度B：次に対応するタスク

## B-1. `convert_revit_schedule.py` v0.2化

### 対象ファイル

- `08_python/convert_revit_schedule.py`
- 将来的に `src/convert_revit_schedule.py`

### 目的

Revit書き出しTXTを品質チェック用CSVへ安定して変換できるようにする。

### やること

- 入力ファイルパスを指定できるようにする
- 出力ファイルパスを指定できるようにする
- 区切り文字を明示する
- 文字コード対応を整理する
- 列名変換ルールを整理する
- 必要列だけ抽出する
- 欠損値の扱いを整理する
- `SourceFile` を付与する
- `ModelName` を付与する
- 処理結果をPowerShell上に表示する
- エラー時に分かりやすいメッセージを出す

### 完了条件

- Revit書き出しTXTを安定してCSV変換できる
- 入力ファイルと出力ファイルを変更しやすい
- 変換後CSVの列構成を説明できる

---

## B-2. `check_bim_quality.py` v0.2化

### 対象ファイル

- `08_python/check_bim_quality.py`
- 将来的に `src/check_bim_quality.py`

### 目的

BIM品質チェック処理を整理し、入力CSV、ルールマスタ、出力CSVを扱いやすくする。

### やること

- 入力CSVを指定しやすくする
- ルールマスタCSVを指定しやすくする
- 出力CSVを指定しやすくする
- 関数分割する
- 必須項目チェック処理を整理する
- 分類コード未入力チェック処理を整理する
- 命名規則チェック処理を整理する
- RuleId付与処理を整理する
- `DetectedAt` の出力を整理する
- エラー処理を追加する
- 処理結果件数を表示する

### 完了条件

- サンプルCSVとRevit由来CSVの両方で品質チェックを実行できる
- RuleId付きチェック結果CSVを安定して出力できる
- 処理内容を関数単位で説明できる

---

## B-3. `business_requirements_mapping.md` の作成

### 作成予定ファイル

- `docs/business_requirements_mapping.md`

### 目的

実務課題とPoCでの対応関係を整理する。

単なるコードではなく、BIM実務課題を技術に落とし込めることを示す。

### 記載例

| 実務課題 | PoCでの対応 | 使用技術 |
|---|---|---|
| BIM属性未入力が多い | 必須項目チェック | pandas, rules CSV |
| 命名規則が守られない | 正規表現チェック | Python |
| BIMデータをAIに使えない | データクレンジング | pandas |
| 修正優先度が属人的 | 修正優先度分類プロトタイプ | scikit-learn |
| AI回答の根拠が曖昧 | RuleId付き構造化コンテキスト | JSON / Markdown |
| 開発部門に要件を伝えにくい | ルール定義・設計ドキュメント化 | docs |

### 完了条件

- 実務課題と技術対応を表で説明できる
- 面接で「なぜこのPoCを作ったか」を説明できる
- BIM導入支援経験とPython実装の接続が説明できる

---

## B-4. `evaluation_policy.md` の作成

### 作成予定ファイル

- `docs/evaluation_policy.md`

### 目的

今後作成する修正優先度分類プロトタイプの評価方針を整理する。

機械学習を過大に見せず、実務適用条件を理解していることを示す。

### 記載する内容

- 本PoCの評価対象
- モデル精度を主目的にしない理由
- 仮ラベルの限界
- 実務適用に必要な教師データ
- 今後取得すべきデータ
- classification_report の位置づけ
- confusion_matrix の位置づけ
- feature_importance の位置づけ
- 実務適用時に必要な追加検証

### 完了条件

- 修正優先度分類プロトタイプの目的を説明できる
- 仮ラベルの限界を説明できる
- 実務データが必要な理由を説明できる
- モデル精度を過大に見せない説明ができる

---

## B-5. `tests/test_quality_rules.py` の作成

### 作成予定ファイル

- `tests/test_quality_rules.py`

### 目的

RuleIdベース品質チェックの基本動作を確認するための最小テストを作成する。

PoCを単なる学習メモではなく、開発成果物として見せやすくする。

### テスト内容

- 必須項目未入力を検出できるか
- 分類コード未入力を検出できるか
- ファミリ命名規則違反を検出できるか
- Severityが想定どおりに扱われるか
- RuleIdが正しく付与されるか

### 完了条件

- 最小テストが実行できる
- 主要ルールの検出結果を確認できる
- 品質チェックロジックの基本動作を説明できる

---

# 優先度C：後続タスク

## C-1. 品質メトリクス作成

### 対象予定ファイル

- `src/calculate_quality_metrics.py`
- `data/output/quality_metrics.csv`

### 目的

品質チェック結果CSVを、分析・可視化・特徴量設計に利用しやすいメトリクスへ変換する。

### 作成するメトリクス候補

- 総要素数
- 総違反件数
- 違反要素数
- 違反率
- RuleId別違反数
- Category別違反数
- Severity別違反数
- ElementId別違反数
- 分類コード付与率
- 入力率
- 品質スコア

---

## C-2. 特徴量設計

### 対象予定ファイル

- `src/create_bim_features.py`
- `data/output/bim_features.csv`

### 目的

BIM品質チェック結果を、機械学習や分析に利用できる特徴量データセットへ変換する。

### 特徴量候補

- MissingFieldCount
- RuleViolationCount
- CriticalViolationCount
- WarningViolationCount
- HasClassificationCode
- FamilyNameValid
- ParameterCompletenessRate
- CategoryEncoded
- SeverityScore
- QualityScore
- FixPriority

---

## C-3. Streamlit簡易UI化

### 対象予定ファイル

- `app/streamlit_app.py`

### 目的

PoCを画面で説明しやすくする。

### 想定機能

- CSVアップロード
- データプレビュー
- 品質チェック実行
- 違反一覧表示
- 品質スコア表示
- RuleId別違反グラフ
- Category別違反グラフ
- Severity別違反グラフ
- 修正優先度分類プロトタイプの結果表示
- 生成AI向け構造化コンテキスト表示
- CSV / JSON ダウンロード

---

## C-4. 生成AI向け構造化コンテキスト生成

### 対象予定ファイル

- `src/generate_ai_context.py`
- `data/output/ai_context.json`
- `data/output/ai_context.md`

### 目的

RuleId、違反内容、重大度、品質スコア、修正優先度をもとに、生成AIへ渡す構造化コンテキストを作成する。

### 含める情報

- ElementId
- Category
- FamilyName
- TypeName
- QualityScore
- PredictedFixPriority
- RuleId
- RuleName
- Severity
- ViolationMessage
- FixGuide
- BusinessImpact
- AIUseImpact
- SourceFile
- ModelName

---

# 今は急がないこと

以下は重要だが、今すぐ優先しない。

- 本格RAG構成
- Azure AI連携
- OpenAI API連携
- ローカルLLM検証
- Revit APIによる直接操作
- pyRevit連携
- Dynamo Python連携
- Power BIダッシュボードの高度化
- 複雑なDAX作成
- 複数モデルの機械学習比較
- E資格学習
- AI-102学習

現時点では、Revit由来データをPythonで安定処理し、RuleIdベース品質チェック、品質メトリクス、特徴量設計へつなげることを優先する。

---

# READMEに残すNext Priorities

READMEには詳細タスクをすべて書かず、以下のように短く記載する。

```markdown
## Next Priorities

詳細な次工程は `docs/next_steps_260524.md` に整理しています。

主な優先事項は以下です。

1. Revit由来CSVの列マッピング整理
2. `08_python` / `06_ai_demo` の試作コードを `src` 配下へ整理
3. `data_dictionary.md` / `rule_specification.md` / `limitations.md` の作成
4. `convert_revit_schedule.py` と `check_bim_quality.py` のv0.2化
5. 品質メトリクス作成
6. 特徴量設計
7. Streamlit簡易UI化
8. 生成AI向け構造化コンテキスト生成
```

---

# 6月末に言える状態

6月末には、以下を説明できる状態を目指す。

> Revitから書き出した集計表TXTをPythonで読み込み、品質チェック用CSVへ変換し、データクレンジング、列名標準化、RuleIdベースの品質チェック、チェック結果CSV出力までを実装した。  
> また、Revit由来データの列マッピング、データ辞書、RuleId仕様、現時点の限界を整理し、7月以降の品質メトリクス作成・特徴量設計につなげる土台を作った。

---

# 最終方針

次工程では、機能追加を急ぎすぎない。

最優先は、5月の試作成果物を本実装・ポートフォリオ向けに整理することである。

特に重要なのは以下である。

1. Revit由来CSVの列マッピング整理
2. `08_python` / `06_ai_demo` / `src` の役割整理
3. `data_dictionary.md`
4. `rule_specification.md`
5. `limitations.md`
6. `convert_revit_schedule.py` v0.2化
7. `check_bim_quality.py` v0.2化

この土台ができれば、7月以降に品質メトリクス作成、特徴量設計、Streamlit、修正優先度分類プロトタイプ、生成AI向け構造化コンテキスト生成へ自然に進める。