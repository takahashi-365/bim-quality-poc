# Data Dictionary

## BIM Data Quality & AI Readiness Assessment PoC

## この資料の目的

この資料は、Revit由来TXT、品質チェック用CSV、品質チェック結果CSV、AI Readiness Score、AI Context、Fix Guideで使用する主な列の意味、現時点の扱い、注意点を整理するためのデータ辞書です。

現時点では、Revit由来データ対応は初期試作段階であり、一部の列は正式なRevit内部情報ではなく、建具表上の列をPoC用に仮対応させています。

この資料では、現時点の仮マッピングを明記し、今後の正式な列マッピング、データクレンジング、品質チェック、特徴量設計、AI Readiness Assessmentへつなげることを目的とします。

---

## 1. 対象データ

現時点で対象としているRevit由来データは以下です。

```text
03_input_csv/door_schedule_SD_export_test_v001.txt
```

このファイルは、Revitのドア建具表をタブ区切りTXTとして書き出したものです。

変換後CSVは以下です。

```text
03_input_csv/door_schedule_converted_v002.csv
```

クレンジング済みCSVは以下です。

```text
03_input_csv/cleaned_bim_data_v001.csv
```

現時点では、ドア建具表のみを対象にしています。

---

## 2. 品質チェック用CSVの主な列

| 列名                     | 意味           | 現時点の扱い                                       | 注意点                                  | 今後の対応                                                                                 |
| ---------------------- | ------------ | -------------------------------------------- | ------------------------------------ | ------------------------------------------------------------------------------------- |
| Category               | BIM要素カテゴリ    | 現時点では `Doors` を固定値として付与                      | ドア集計表のみを対象にした初期試作                    | 将来的には Walls、Rooms などにも対応                                                              |
| ElementId              | BIM要素を識別するID | 現時点ではRevit内部ElementIdではなく、建具表上の建具番号を仮IDとして使用 | `101`、`102` などの建具番号であり、Revit内部IDではない | Revit内部ElementIdを出力できるか検討。難しい場合は `ElementKey`、`DoorNumber`、`ScheduleMark` などへの名称変更を検討 |
| FamilyName             | Revitファミリ名   | 現時点ではRevitファミリ名ではなく、建具表上の種別記号 `SD` を仮格納      | 正式なFamilyNameではないため、命名規則チェック結果は参考扱い  | Revitファミリ名を出力できる集計表設定を検討                                                              |
| TypeName               | Revitタイプ名    | 現時点ではRevitタイプ名ではなく、設置場所・室名に近い列を仮格納           | `管理用出入口`、`PS`、`電気室 1F` などが入る         | `LocationName` または `RoomName` として扱うか、別列をTypeName候補として検討                               |
| Level                  | 階情報          | 現時点では空欄                                      | ドア集計表TXTからは階情報を取得していない               | Revit集計表側で階情報を追加するか検討                                                                 |
| BIM_ClassificationCode | 分類コード        | 現時点では空欄                                      | 未入力チェック対象として使用                       | 将来的に分類コードを持つ列を追加                                                                      |
| BIM_ModelRole          | モデル上の役割      | 現時点では空欄                                      | 未入力チェック対象として使用                       | Revit側またはCSV側で値を追加するか検討                                                               |
| BIM_Zone               | ゾーン情報        | 現時点では空欄                                      | 未入力チェック対象として使用                       | Revit側またはCSV側で値を追加するか検討                                                               |
| SourceFile             | 元データファイル名    | 入力TXTファイル名を付与                                | 変換元ファイルを追跡するために使用                    | 継続使用                                                                                  |
| ModelName              | モデル名         | 固定値としてサンプルモデル名を付与                            | 現時点では固定文字列                           | 将来的には設定値化を検討                                                                          |

---

## 3. 元TXT列との対応

現時点の `convert_revit_schedule.py` では、Revit書き出しTXTの一部列をPoC用の標準列へ仮マッピングしています。

| 変換後CSVの列               | 元TXT列番号 | 元TXTの値の例                                  | 推定される意味      | 現時点の判定               |
| ---------------------- | ------: | ----------------------------------------- | ------------ | -------------------- |
| Category               |     固定値 | Doors                                     | カテゴリ         | 問題なし                 |
| ElementId              |       1 | 101, 102, 201                             | 建具番号・建具符号    | Revit内部ElementIdではない |
| FamilyName             |       0 | SD                                        | 建具種別・建具表種別   | Revitファミリ名ではない       |
| TypeName               |       3 | 管理用出入口, PS, 電気室 1F                        | 設置場所・室名・用途名称 | Revitタイプ名ではない        |
| Level                  |      なし | 空欄                                        | 階情報          | 未対応                  |
| BIM_ClassificationCode |      なし | 空欄                                        | 分類コード        | 未対応                  |
| BIM_ModelRole          |      なし | 空欄                                        | モデル上の役割      | 未対応                  |
| BIM_Zone               |      なし | 空欄                                        | ゾーン情報        | 未対応                  |
| SourceFile             | 入力ファイル名 | door_schedule_SD_export_test_v001.txt     | 元ファイル名       | 問題なし                 |
| ModelName              |     固定値 | BIM_Quality_Check_Sample_Model_R2024_v001 | モデル名         | 問題なし                 |

---

## 4. 仮マッピングと正式マッピング方針

現時点では、PoCの処理フローを成立させるために、Revit書き出しTXTの列を以下のように仮対応させています。

| 現在の列名                  | 現時点の実データ    | 正式に期待する意味        | 現在の扱い     |
| ---------------------- | ----------- | ---------------- | --------- |
| ElementId              | 建具番号        | Revit内部ElementId | 仮ID       |
| FamilyName             | 建具種別記号 `SD` | Revitファミリ名       | 仮ファミリ名    |
| TypeName               | 設置場所・室名に近い値 | Revitタイプ名        | 仮タイプ名     |
| Level                  | 空欄          | 配置階              | 未対応       |
| BIM_ClassificationCode | 空欄          | 分類コード            | 未入力チェック対象 |
| BIM_ModelRole          | 空欄          | モデル上の役割          | 未入力チェック対象 |
| BIM_Zone               | 空欄          | ゾーン情報            | 未入力チェック対象 |

このため、現時点の品質チェック結果は、Revitモデルの正式な品質評価ではなく、PoCとして処理フロー、RuleId連携、品質メトリクス、AI Readiness Score、AI Context、Fix Guide生成を確認するための結果として扱います。

---

## 5. チェック結果CSVの主な列

対象ファイル：

```text
04_output_csv/check_results_revit_v002.csv
```

| 列名            | 意味          | 現時点の扱い                                                              |
| ------------- | ----------- | ------------------------------------------------------------------- |
| CheckId       | チェック結果のID   | 違反ごとに付与                                                             |
| ElementId     | チェック対象要素のID | 現時点では建具番号を仮IDとして使用                                                  |
| Category      | カテゴリ        | 現時点では Doors                                                         |
| FamilyName    | ファミリ名相当     | 現時点では建具種別記号                                                         |
| TypeName      | タイプ名相当      | 現時点では設置場所・室名に近い値                                                    |
| Level         | 階情報         | 現時点では空欄                                                             |
| ParameterName | 違反対象パラメータ   | `BIM_ClassificationCode`、`BIM_ModelRole`、`BIM_Zone`、`FamilyName` など |
| CurrentValue  | 現在値         | 空欄または命名規則違反の対象値                                                     |
| RuleId        | 適用されたルールID  | `R-001`、`R-002`、`R-003`                                             |
| RuleName      | ルール名        | ルールマスタから取得                                                          |
| Severity      | 重大度         | ルールマスタから取得                                                          |
| Status        | チェック結果      | 現時点では主に `NG`                                                        |
| FixGuide      | 修正ガイド       | ルールマスタから取得                                                          |
| DetectedAt    | 検出日時        | チェック実行時に付与                                                          |
| SourceFile    | 元ファイル名      | 変換元TXT名                                                             |
| ModelName     | モデル名        | サンプルモデル名                                                            |

現時点の出力件数は以下です。

```text
対象要素数: 25
品質チェック結果: 100件
```

RuleId別の内訳は以下です。

| RuleId | 内容         | 件数 |
| ------ | ---------- | -: |
| R-001  | 必須パラメータ未入力 | 50 |
| R-002  | 分類コード未入力   | 25 |
| R-003  | ファミリ命名規則違反 | 25 |

---

## 6. 品質メトリクス関連の主な列

対象ファイル：

```text
04_output_csv/quality_metrics_v001.csv
04_output_csv/rule_summary_v001.csv
04_output_csv/category_summary_v001.csv
04_output_csv/element_summary_v001.csv
```

| 列名             | 意味          | 現時点の扱い                      |
| -------------- | ----------- | --------------------------- |
| RuleId         | ルールID       | `R-001`、`R-002`、`R-003`     |
| RuleName       | ルール名        | ルールマスタから取得                  |
| Severity       | 重大度         | High / Medium               |
| ViolationCount | 違反件数        | RuleId別、Category別などで集計      |
| Category       | カテゴリ        | 現時点では Doors                 |
| ElementId      | 要素ID        | 建具番号を仮IDとして使用               |
| SeverityScore  | 重大度に応じた減点合計 | High = 10点、Medium = 5点として算出 |
| QualityScore   | BIM品質の簡易スコア | `100 - SeverityScore`       |

QualityScoreはPoC用の簡易指標であり、正式な実務評価基準ではありません。

---

## 7. 特徴量データセットの主な列

対象ファイル：

```text
04_output_csv/bim_features_v001.csv
```

| 列名                    | 意味                | 現時点の扱い               |
| --------------------- | ----------------- | -------------------- |
| ElementId             | 要素ID              | 建具番号を仮IDとして使用        |
| Category              | カテゴリ              | Doors                |
| RuleViolationCount    | ルール違反件数           | 各ElementIdの違反数       |
| MissingFieldCount     | 未入力項目数            | 必須パラメータや分類コード未入力数    |
| HighViolationCount    | High違反件数          | 各ElementIdのHigh違反数   |
| MediumViolationCount  | Medium違反件数        | 各ElementIdのMedium違反数 |
| LowViolationCount     | Low違反件数           | 現時点では0               |
| HasClassificationCode | 分類コード有無           | 現時点では0相当             |
| FamilyNameValid       | FamilyNameの命名規則判定 | 現時点ではSDが命名規則違反扱い     |
| SeverityScore         | 重大度スコア            | QualityScore算出に使用    |
| QualityScore          | 品質スコア             | 現時点では全要素65           |
| FixPriority           | 修正優先度仮ラベル         | 現時点では全要素High         |

FixPriorityは実務上の正解ラベルではなく、QualityScoreとHigh違反件数をもとにした仮ラベルです。

---

## 8. AI Readiness Score関連の主な列

対象ファイル：

```text
04_output_csv/ai_readiness_scores_v001.csv
```

| 列名                      | 意味                           | 現時点の扱い                          |
| ----------------------- | ---------------------------- | ------------------------------- |
| ElementId               | 要素ID                         | 建具番号を仮IDとして使用                   |
| Category                | カテゴリ                         | Doors                           |
| RuleViolationCount      | ルール違反件数                      | 各ElementIdの違反数                  |
| AIReadinessPenaltyTotal | AI活用準備度の減点合計                 | RuleIdごとのAIReadinessPenaltyを合計  |
| AIReadinessScore        | AI活用準備度スコア                   | `100 - AIReadinessPenaltyTotal` |
| AIReadinessLevel        | AI活用準備度レベル                   | High / Medium / Low             |
| BlockingRuleIds         | AI活用を阻害しているRuleId            | `R-001, R-002, R-003`           |
| HighImpactRuleCount     | AIReadinessImpactがHighの違反数   | 現時点では3                          |
| MediumImpactRuleCount   | AIReadinessImpactがMediumの違反数 | 現時点では1                          |
| HumanReviewRequired     | 人間確認要否                       | LowまたはHigh影響ありの場合True           |

現時点の初期データでは、全25要素が以下の結果となっています。

```text
AIReadinessScore = 40
AIReadinessLevel = Low
HumanReviewRequired = True
```

AIReadinessScoreはPoC用の簡易指標であり、正式なAI活用準備度基準ではありません。

---

## 9. AI Context v002関連の主な構造

対象ファイル：

```text
04_output_csv/ai_context_v002.json
04_output_csv/ai_context_v002.md
```

AI Context v002では、BIM品質チェック結果、特徴量データセット、AI Readiness Scoreをもとに、生成AIや将来的なRAGに渡す前段階の構造化コンテキストを生成しています。

主な構造は以下です。

| 構造              | 内容                                         |
| --------------- | ------------------------------------------ |
| project         | PoC名、前段階PoC名、目的、注意点                        |
| input_files     | 入力ファイルパス                                   |
| summary         | 総違反数、対象要素数、RuleId別集計、AI Readiness集計        |
| limitations     | PoC上の制約                                    |
| elements        | ElementIdごとの詳細コンテキスト                       |
| element         | 要素情報                                       |
| quality_summary | QualityScoreやFixPriorityなどの品質概要            |
| ai_readiness    | AIReadinessScore、AIReadinessLevel、人間確認要否など |
| violations      | RuleId別の違反詳細                               |
| ai_instruction  | 生成AIに渡す場合の前提条件・制約                          |

`ai_context_v002.json` の `ai_readiness` には、主に以下が含まれます。

* `ai_readiness_penalty_total`
* `ai_readiness_score`
* `ai_readiness_level`
* `blocking_rule_ids`
* `high_impact_rule_count`
* `medium_impact_rule_count`
* `human_review_required`

現時点では生成AI APIは呼び出していません。

---

## 10. Fix Guide Markdown関連の主な項目

対象ファイル：

```text
04_output_csv/fix_guides_v001.md
```

Fix Guide Markdownでは、品質チェック結果、Rule Master v003、AI Readiness Scoreをもとに、RuleIdベースの修正方針をMarkdownとして出力しています。

主な構成は以下です。

| セクション                      | 内容                                    |
| -------------------------- | ------------------------------------- |
| Summary                    | 対象要素数、違反数、平均AI Readiness Score、人間確認件数 |
| Input Files                | 入力ファイル                                |
| AI Readiness Level Summary | AIReadinessLevel別件数                   |
| Blocking Rule Summary      | AI活用を阻害しているRuleId別集計                  |
| Element Fix Guide          | ElementId別の修正ガイド                      |
| Limitations                | Fix Guideの制約                          |

Element Fix Guideでは、各ElementIdについて以下を出力しています。

* Category
* FamilyName
* TypeName
* AI Readiness Score
* AI Readiness Level
* AI Readiness Penalty Total
* Blocking RuleIds
* Human Review Required
* RuleId別のFixGuide

このFix Guideは生成AI APIによる文章生成ではなく、RuleIdベースのテンプレート方式で生成しています。

---

## 11. 現時点の注意点

* `ElementId` は、現時点ではRevit内部ElementIdではなく、建具表上の建具番号を仮IDとして使用している。
* `FamilyName` は、現時点ではRevitファミリ名ではなく、建具表上の種別記号 `SD` を仮格納している。
* `TypeName` は、現時点ではRevitタイプ名ではなく、設置場所・室名に近い列を仮格納している。
* `Level` は現時点では空欄である。
* `BIM_ClassificationCode`、`BIM_ModelRole`、`BIM_Zone` は現時点では空欄であり、未入力チェック対象として使用している。
* `check_results_revit_v002.csv` の100件の違反は、正確な品質評価ではなく、処理フロー確認のための結果である。
* 100件の内訳は、25要素に対して、`BIM_ModelRole`、`BIM_Zone`、`BIM_ClassificationCode`、`FamilyName` の違反が発生しているためである。
* `QualityScore` はPoC用の簡易指標であり、正式な実務品質評価基準ではない。
* `FixPriority` はPoC用の仮ラベルであり、実務上の正解ラベルではない。
* `AIReadinessScore` はPoC用の簡易指標であり、正式なAI活用準備度基準ではない。
* `AIReadinessPenalty` はPoC用の仮設定であり、今後調整する前提である。
* `AI Context v002` は生成AIやRAGへ渡す前段階の構造化コンテキストであり、生成AI APIの呼び出しは未実装である。
* `Fix Guide Markdown` は生成AI APIではなく、RuleIdベースのテンプレート方式で生成している。

---

## 12. 今後の対応

* Revit集計表側で正式なRevit内部ElementIdを出力できるか確認する。
* Revitファミリ名、タイプ名を取得できる列を追加できるか確認する。
* `ElementId` という列名が不正確な場合は、`ElementKey`、`DoorNumber`、`ScheduleMark` などへの名称変更を検討する。
* `FamilyName`、`TypeName`、`LocationName`、`RoomName` の役割を整理する。
* `Level`、`BIM_ClassificationCode`、`BIM_ModelRole`、`BIM_Zone` の取得方法を検討する。
* 仮マッピングと正式マッピングの対応表を整理する。
* `docs/revit_schedule_column_mapping.md` を作成または更新する。
* 列マッピング確定後、`convert_revit_schedule.py` を更新する。
* 列マッピング改善後、品質チェック、特徴量作成、AI Readiness Score、AI Context、Fix Guideへの影響を確認する。

---

## 13. まとめ

現時点の `door_schedule_converted_v002.csv` は、Revit由来TXTをPython処理へ接続するための初期試作データです。

そのため、`ElementId`、`FamilyName`、`TypeName` などの列名は、PoCの標準列に合わせるために仮で対応させていますが、正式なRevit内部情報とは一致していません。

一方で、この仮マッピングを明記することで、PoCとしての前提条件、制約、今後の改善方針を説明できる状態にしています。

今後は、Revit集計表側の列構成を見直し、正式なElementId、FamilyName、TypeName、Level、分類コード、モデル上の役割、ゾーン情報などを取得できるか確認したうえで、品質チェック用CSVの列定義を更新します。

このデータ辞書は、Revit由来データの列定義、品質チェック、品質メトリクス作成、特徴量設計、AI Readiness Assessment、AI Context生成、Fix Guide生成へつなげるための基礎資料として使用します。
