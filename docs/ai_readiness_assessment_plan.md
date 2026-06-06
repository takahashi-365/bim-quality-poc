# AI Readiness Assessment Plan

## BIM Data Quality & AI Readiness Assessment PoC

## この資料の目的

この資料は、既存の **BIM Data Quality Engineering & AI Analysis PoC** を、第2段階として **BIM Data Quality & AI Readiness Assessment PoC** へ拡張するための計画と実装方針を整理するものです。

第2段階では、新しい別PoCを作るのではなく、第1段階で作成したBIMデータ品質チェックPoCを継続利用し、BIMデータがBI、機械学習、生成AI、将来的なRAGに活用できる状態かを評価する仕組みへ拡張します。

本資料では、AI Readiness Score、Rule Master v003、AI Context v002、Fix Guide Markdown、Streamlit画面拡張、Revit列マッピング整理の方針と実装結果をまとめます。

---

## 1. 第2段階の目的

第2段階の目的は、BIMデータがAIやデータ活用に使える状態かを評価することです。

ここでいうAI活用とは、以下を想定します。

* BIでの集計・可視化
* 機械学習用の特徴量作成
* 生成AIへの構造化コンテキスト提供
* 将来的なRAG連携
* 人間レビューを支援する修正ガイド生成

主目的は、本格的なRAGシステム構築や生成AI API接続ではありません。

本PoCでは、AIに自由判断させる前に、RuleId、品質チェック結果、QualityScore、FixPriority、AIReadinessScore、HumanReviewRequired、FixGuideなどを構造化し、AIへ渡す前段階のデータ品質と文脈を整理することを重視します。

---

## 2. 第1段階と第2段階の位置づけ

### 第1段階

第1段階のPoC名：

**BIM Data Quality Engineering & AI Analysis PoC**

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
* ポートフォリオPDF v002

### 第2段階

第2段階のPoC名：

**BIM Data Quality & AI Readiness Assessment PoC**

日本語名：

**BIMデータ品質・AI活用準備度評価PoC**

第2段階では、既存PoCを発展させ、BIMデータがAIやデータ活用に使える状態かを評価できる構成にします。

第2段階で重視する内容は以下です。

* AI活用前のBIMデータ品質評価
* AI Readiness Score
* RuleIdベースのAI活用影響整理
* AI Context JSON / Markdown v002
* Fix Guide Markdown生成
* StreamlitによるAI Readiness確認画面
* Revit列マッピングの前提整理

---

## 3. 全体の開発順序

今回のAI Readiness Assessment拡張では、以下の順序で開発を進めます。

1. `docs/ai_readiness_assessment_plan.md` を作成する
2. PoC名と目的を再定義する
3. AI Readiness Scoreを設計する
4. Rule Master v003を作成する
5. AI Readiness Scoreを実装する
6. AI Context JSON / Markdown v002を拡張する
7. Fix Guide Markdownを生成する
8. Streamlit画面を拡張する
9. Revit列マッピングを改善する
10. docsを更新する
11. testsを追加する
12. READMEを整理する
13. GitHub公開範囲を判断する
14. ポートフォリオPDF v003化を検討する

現時点では、1〜9までを完了扱いとし、10は更新作業中です。

---

## 4. AI Readiness Scoreの考え方

AI Readiness Scoreは、BIM要素ごとにAIやデータ活用に使いやすい状態かを評価する簡易スコアです。

AI Readiness Scoreでは、以下のような観点を評価します。

* 必須属性が入力されているか
* 分類コードが入力されているか
* 命名規則が一定のルールに沿っているか
* AIやBIで検索・分類・集計しやすい状態か
* 人間確認が必要な状態か

初期計算式は以下です。

```text
AIReadinessScore = 100 - AIReadinessPenalty合計
```

スコアが0未満になる場合は0とします。

初期レベル分類は以下です。

| AIReadinessScore | AIReadinessLevel |
| ---------------- | ---------------- |
| 80-100           | High             |
| 60-79            | Medium           |
| 0-59             | Low              |

---

## 5. Rule Master v003

AI Readiness Scoreを計算するため、既存のRule Master v002を拡張し、Rule Master v003を作成しました。

作成ファイル：

```text
02_rule_master/bim_rule_master_v003.csv
```

追加列：

* `AIReadinessImpact`
* `AIReadinessPenalty`

初期ペナルティ設定は以下です。

| RuleId | RuleName   | AIReadinessImpact | AIReadinessPenalty |
| ------ | ---------- | ----------------- | -----------------: |
| R-001  | 必須パラメータ未入力 | High              |                 15 |
| R-002  | 分類コード未入力   | High              |                 20 |
| R-003  | ファミリ命名規則違反 | Medium            |                 10 |

各ルールの位置づけは以下です。

* R-001 必須パラメータ未入力
  AIに渡す属性情報が不足し、回答や分類の信頼性が下がるため、AIReadinessImpactはHighとします。

* R-002 分類コード未入力
  分類、検索、集計、将来的なRAG利用時の前提が弱くなるため、AIReadinessImpactはHighとします。

* R-003 ファミリ命名規則違反
  名称ベースの分類や検索の信頼性が下がるため、AIReadinessImpactはMediumとします。

Rule Master v003は、AI Readiness ScoreとAI Context v002、Fix Guide Markdown生成を支えるためのマスタ拡張として位置づけます。

---

## 6. AI Readiness Score実装

AI Readiness Scoreを算出するため、以下のスクリプトを作成しました。

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

処理内容：

* 品質チェック結果CSVを読み込む
* Rule Master v003を読み込む
* RuleIdをキーに、品質チェック結果へ `AIReadinessImpact` と `AIReadinessPenalty` を結合する
* ElementIdごとに違反件数を集計する
* ElementIdごとにAIReadinessPenaltyを合計する
* AIReadinessScoreを算出する
* AIReadinessLevelをHigh / Medium / Lowに分類する
* AI活用を阻害しているRuleIdをBlockingRuleIdsとして整理する
* AIReadinessImpactがHigh / Mediumの違反数を集計する
* HumanReviewRequiredを判定する
* ElementIdを `101.0` ではなく `101` 形式で出力する
* `ai_readiness_scores_v001.csv` を出力する

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

実行結果：

* 品質チェック結果100件を読み込み
* Rule Master v003の3ルールを読み込み
* 25要素分のAI Readiness Scoreを出力
* 全25要素が `AIReadinessScore = 40`
* 全25要素が `AIReadinessLevel = Low`
* 全25要素が `HumanReviewRequired = True`
* ElementIdは `101.0` ではなく `101` 形式で出力

全件Lowになったのは不具合ではありません。

初期データでは、各要素に以下の違反が含まれているためです。

* 必須パラメータ未入力
* 分類コード未入力
* ファミリ命名規則違反

この結果は、BIMデータをAIやBIに活用する前に、属性情報、分類コード、命名規則の整備が必要であることを示すPoC結果として扱います。

---

## 7. AI Context JSON / Markdown v002

既存の生成AI向け構造化コンテキストを拡張し、AI Readiness Scoreの情報を含めるようにしました。

対象スクリプト：

```text
src/generate_ai_context.py
```

入力ファイル：

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

追加した主な項目：

* `AIReadinessScore`
* `AIReadinessLevel`
* `AIReadinessPenaltyTotal`
* `BlockingRuleIds`
* `HighImpactRuleCount`
* `MediumImpactRuleCount`
* `HumanReviewRequired`

Markdown出力では、以下を追加しました。

* Project名を第2段階の名称に更新
* Previous Nameとして第1段階のPoC名を追加
* Input Filesに `ai_readiness_scores_v001.csv` を追加
* Average AI Readiness Scoreを追加
* Human Review Required Countを追加
* AI Readiness Level Summaryを追加
* Sample Element ContextにAI Readiness情報を追加
* LimitationsにAIReadinessScoreと生成AI API未接続の注意点を追加

JSON出力では、以下を追加しました。

* `project` に第2段階のPoC名を設定
* `input_files` に `ai_readiness_csv` を追加
* `summary` に `ai_readiness_level_summary` を追加
* `summary` に `average_ai_readiness_score` を追加
* `summary` に `human_review_required_count` を追加
* 各 `elements` に `ai_readiness` ブロックを追加
* `ai_instruction` を BIM data quality and AI readiness assistant 向けに更新

これにより、BIM品質チェック結果、QualityScore、FixPriority、AI Readiness Scoreを生成AI向けコンテキストに接続できました。

---

## 8. Fix Guide Markdown生成

品質チェック結果、Rule Master v003、AI Readiness Scoreをもとに、BIMデータの修正方針をMarkdown形式で出力する処理を追加しました。

作成スクリプト：

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

この処理では、生成AI APIは使わず、RuleIdベースのテンプレート方式で人間確認向けの修正ガイドを生成します。

出力Markdownの主な内容：

* Summary
* Input Files
* AI Readiness Level Summary
* Blocking Rule Summary
* Element Fix Guide
* Limitations

Element Fix Guideに出力した内容：

* ElementId
* Category
* FamilyName
* TypeName
* AI Readiness Score
* AI Readiness Level
* AI Readiness Penalty Total
* Blocking RuleIds
* Human Review Required
* Recommended fix approach
* RuleId別のFixGuide

実行結果：

* 品質チェック結果100件を読み込み
* Rule Master v003の3ルールを読み込み
* AI Readiness Score 25要素を読み込み
* 修正ガイド用データ100件を生成
* `04_output_csv/fix_guides_v001.md` を出力

Fix Guide Markdownは、生成AI APIではなくRuleIdベースで修正方針を整理するための初期実装です。

---

## 9. Streamlit画面拡張

既存のStreamlit画面を拡張し、第2段階で作成したAI Readiness Assessment、AI Context v002、Fix Guide Markdownを画面上で確認できるようにしました。

対象ファイル：

```text
app/streamlit_app.py
```

追加で読み込むファイル：

```text
04_output_csv/ai_readiness_scores_v001.csv
04_output_csv/ai_context_v002.json
04_output_csv/ai_context_v002.md
04_output_csv/fix_guides_v001.md
```

追加した主な画面：

* `7. AI Readiness Assessment`
* `9. 生成AI向け構造化コンテキスト v002`
* `10. Fix Guide Markdown Preview`
* `11. 出力ファイルダウンロード`
* `12. 現時点の注意点`

AI Readiness Assessmentで表示した内容：

* Target Elements
* Average AI Readiness Score
* Low Level Count
* Human Review Required
* AI Readiness Level別件数
* ElementId別 AI Readiness Score
* AI活用を阻害しているRuleIdランキング
* Element Detail
* 選択したElementIdのAI Readiness Score
* 選択したElementIdの品質チェック結果

AI Context v002で表示した内容：

* Total Violations
* Total Elements
* Average AI Readiness Score
* Human Review Required Count
* Project名
* Previous Name
* Purpose
* AI Readiness Level Summary
* Element Context Preview
* 選択したElementIdのJSONコンテキスト
* `ai_context_v002.md` のMarkdownプレビュー
* `ai_context_v002.json` のダウンロード
* `ai_context_v002.md` のダウンロード

Fix Guide Markdown Previewで表示した内容：

* `fix_guides_v001.md` のプレビュー
* `fix_guides_v001.md` のダウンロード

実行コマンド：

```powershell
streamlit run .\app\streamlit_app.py
```

Streamlit画面により、第1段階の品質チェック結果と、第2段階のAI活用準備度評価を1つの画面で確認できるようになりました。

---

## 10. Revit列マッピング整理

Revit書き出しTXTから品質チェック用CSVへ変換する際の列マッピングについて、現時点の仮設定を明文化しました。

更新・作成したファイル：

```text
docs/data_dictionary.md
docs/revit_schedule_column_mapping.md
```

今回の目的は、正式なRevit内部情報の取得や `convert_revit_schedule.py` の再設計ではなく、現在のPoCで使っている仮マッピングを隠さず整理し、品質チェック、AI Readiness Score、AI Context v002、Fix Guideへの影響を説明できる状態にすることです。

現在の仮マッピング：

| 品質チェック用CSV列            | 現在の元データ     | 現在の扱い                     |
| ---------------------- | ----------- | ------------------------- |
| Category               | 固定値 `Doors` | ドア建具表対象の固定カテゴリ            |
| ElementId              | 建具番号        | Revit内部ElementIdではなく仮ID   |
| FamilyName             | 建具種別記号 `SD` | Revitファミリ名ではなく仮FamilyName |
| TypeName               | 設置場所・室名に近い値 | Revitタイプ名ではなく仮TypeName    |
| Level                  | 空欄          | 未対応                       |
| BIM_ClassificationCode | 空欄          | 分類コード未入力チェック対象            |
| BIM_ModelRole          | 空欄          | 必須パラメータ未入力チェック対象          |
| BIM_Zone               | 空欄          | 必須パラメータ未入力チェック対象          |
| SourceFile             | 入力TXTファイル名  | 元データ追跡用                   |
| ModelName              | 固定値         | サンプルモデル名                  |

重要な整理内容：

* `ElementId` は、現時点ではRevit内部ElementIdではなく、建具表上の建具番号を仮IDとして使用している
* `FamilyName` は、現時点ではRevitファミリ名ではなく、建具表上の種別記号 `SD` を仮格納している
* `TypeName` は、現時点ではRevitタイプ名ではなく、設置場所・室名に近い列を仮格納している
* `Level` は現時点では空欄
* `BIM_ClassificationCode`、`BIM_ModelRole`、`BIM_Zone` は現時点では空欄
* 現在の品質チェック結果は、正式なRevitモデル品質評価ではなく、PoCとして処理フローを確認するための結果として扱う
* AI Readiness Scoreも、現時点の仮マッピングと未入力項目を前提としたPoC用の簡易指標として扱う

今回のAI Readiness Assessment拡張の範囲では、Revit列マッピング改善は「仮マッピングの明文化・影響整理・将来方針の整理」までを完了扱いとします。

正式なRevit内部ElementId取得、FamilyName / TypeName / Level / RoomNameの本格取得、`convert_revit_schedule.py` の再設計はFuture Workとして扱います。

---

## 11. 第2段階でやらないこと

第2段階では、以下は対象外とします。

* 別PoC作成
* 本格RAG
* Azure AI Search
* 生成AI API接続
* Revit API / pyRevit本格実装
* Revitモデル自動修正
* 機械学習モデルの精度向上
* 深層学習
* 複雑なPower BIダッシュボード再設計
* PL-300学習
* 資格学習

理由は、範囲が広がりすぎるためです。

第2段階では、AI活用前のBIMデータ品質評価、構造化コンテキスト生成、修正ガイド生成、Streamlit簡易表示に集中します。

---

## 12. 予定成果物と実装状況

現時点での主な成果物は以下です。

| 成果物                                          | 状況               |
| -------------------------------------------- | ---------------- |
| `docs/ai_readiness_assessment_plan.md`       | 更新中              |
| `README.md`                                  | 8番までの成果を反映済み     |
| `02_rule_master/bim_rule_master_v003.csv`    | 作成済み             |
| `src/calculate_ai_readiness_score.py`        | 作成済み             |
| `04_output_csv/ai_readiness_scores_v001.csv` | 出力済み             |
| `src/generate_ai_context.py`                 | v002対応済み         |
| `04_output_csv/ai_context_v002.json`         | 出力済み             |
| `04_output_csv/ai_context_v002.md`           | 出力済み             |
| `src/generate_fix_guide.py`                  | 作成済み             |
| `04_output_csv/fix_guides_v001.md`           | 出力済み             |
| `app/streamlit_app.py`                       | AI Readiness対応済み |
| `docs/data_dictionary.md`                    | 更新済み             |
| `docs/revit_schedule_column_mapping.md`      | 新規作成済み           |

---

## 13. 現時点の制約

現時点の制約は以下です。

* Revit由来データ対応は初期試作です。
* `door_schedule_converted_v002.csv` の列マッピングは仮設定です。
* `ElementId` はRevit内部ElementIdではなく、建具表上の建具番号を仮IDとして使用しています。
* `FamilyName` はRevitファミリ名ではなく、建具表上の種別記号 `SD` を仮格納しています。
* `TypeName` はRevitタイプ名ではなく、設置場所・室名に近い列を仮格納しています。
* `BIM_ClassificationCode`、`BIM_ModelRole`、`BIM_Zone` は現時点では空欄であり、未入力チェック対象として使用しています。
* `QualityScore` はPoC用の簡易指標であり、正式な実務品質評価基準ではありません。
* `FixPriority` は実務の正解ラベルではなく、仮ラベルです。
* `AIReadinessScore` はPoC用の簡易指標であり、正式なAI活用準備度基準ではありません。
* `AIReadinessPenalty` はPoC用の仮設定であり、今後、社内BIM標準、分類体系、プロジェクト要件、AI利用目的に応じて調整する前提です。
* `AI Context v002` は生成AIやRAGへ渡す前段階の構造化コンテキストであり、生成AI APIの呼び出しは未実装です。
* `Fix Guide Markdown` は生成AI APIではなく、RuleIdベースのテンプレート方式で生成しています。
* Revit APIやpyRevitとの直接連携は未実装です。
* RevitモデルやBIMデータの自動修正は対象外です。
* 設計判断、施工判断、モデル修正の最終判断は人間が行う前提です。

---

## 14. 今後の対応

今後の主な対応は以下です。

* `docs/system_overview.md` の更新
* `docs/portfolio_summary.md` の更新
* `docs/limitations.md` の更新
* `docs/rule_specification.md` の更新
* AI Readiness Score関連のtests追加
* GitHub公開範囲の確認
* Streamlit画面スクリーンショットの保存
* 必要に応じたポートフォリオPDF v003化検討

Revit列マッピングについては、今回の範囲では初期整理まで完了とし、正式なRevit内部情報取得はFuture Workとして扱います。

---

## 15. 面接での説明方針

RevitやBIMデータをBI、機械学習、生成AI、RAGに活用するには、モデル内の属性情報、分類コード、命名規則、必須パラメータが一定の品質を満たしている必要があります。

本PoCでは、Revit由来データをPythonで読み込み、RuleIdベースで品質チェックを行い、QualityScoreとAI Readiness Scoreを算出します。

さらに、違反内容、重大度、業務影響、AI活用時の影響、修正ガイド、人間確認要否を含む構造化JSON / Markdownを生成し、将来的な生成AIやRAG連携の前処理として利用できる形にしています。

AIに自由判断させるのではなく、BIMルールと品質チェック結果をもとに、AIへ渡す情報を制御する設計を重視しています。

また、現時点のRevit列マッピングには仮設定が含まれているため、その前提を隠さず、PoCとしての制約と将来改善方針を明確に説明します。
