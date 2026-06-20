# FixPriority教師データ列設計

## 目的

このドキュメントでは、第3段階E：FixPriority教師データ設計で使用する教師データCSVの列構成を定義する。

本設計は、将来的に `FixPriority` を分析・学習・レビューに活用できるようにするための列設計である。

ただし、本段階では機械学習モデルの作成、モデル学習、精度評価、自動優先度判定は行わない。

作成するサンプル教師データは、モデル学習用データではなく、列設計とラベル付け方針を確認するための小規模サンプルである。

---

## 前提

第3段階Eでは、教師データ1行の単位を以下とする。

```text
1要素 × 1 RuleId
```

方針：

```text
1つの要素に1つのRuleId違反がある場合は1行として記録する
1つの要素に複数のRuleId違反がある場合はRuleIdごとに複数行として記録する
要素全体の総合優先度は将来拡張とする
```

理由：

```text
RuleIdごとの品質問題とFix Guideを対応させやすい
LabelReasonをRuleId単位で記録しやすい
Door / Roomカテゴリごとの優先度傾向を分析しやすい
将来的にRuleId別の傾向分析につなげやすい
```

---

## 対象CSV

第3段階Eで作成するサンプル教師データCSVは以下とする。

```text
07_fixpriority_training/fixpriority_training_samples_v001.csv
```

---

## 列一覧

初期MVPでは、以下の列を使用する。

```text
TrainingSampleId
ElementId
UniqueId
Category
RuleId
RuleName
Severity
QualityScore
AIReadinessScore
HumanReviewRequired
FixGuideAvailable
FixGuideSummary
IssueSummary
CurrentFixPriority
ProposedFixPriorityLabel
LabelReason
ReviewedBy
ReviewStatus
SourceFile
CreatedDate
Notes
```

---

## 必須列

初期MVPの必須列は以下とする。

```text
TrainingSampleId
ElementId
Category
RuleId
RuleName
Severity
HumanReviewRequired
IssueSummary
CurrentFixPriority
ProposedFixPriorityLabel
LabelReason
ReviewStatus
SourceFile
CreatedDate
```

必須列は、CSV品質検証の対象とする。

---

## 任意列

初期MVPの任意列は以下とする。

```text
UniqueId
QualityScore
AIReadinessScore
FixGuideAvailable
FixGuideSummary
ReviewedBy
Notes
```

任意列であっても、値がある場合は可能な範囲で記録する。

`ReviewedBy` は、GitHub公開用サンプルでは空欄または匿名値とする。

---

## 許可値

### ProposedFixPriorityLabel

`ProposedFixPriorityLabel` の許可値は以下とする。

```text
High
Medium
Low
Review
```

空欄やその他の値は、初期MVPでは許可しない。

---

### ReviewStatus

`ReviewStatus` の許可値は以下とする。

```text
Draft
Reviewed
Approved
```

意味：

| ReviewStatus | 意味                |
| ------------ | ----------------- |
| Draft        | 仮作成したラベル          |
| Reviewed     | BIM担当者または作成者が確認済み |
| Approved     | 教師データとして採用可能と判断   |

初期MVPでは、多くのサンプルを `Draft` として扱ってよい。

---

### Category

`Category` の初期許可値は以下とする。

```text
Door
Room
Other
```

初期サンプルでは、主に `Door` と `Room` を使用する。

---

### Severity

`Severity` の初期許可値は以下とする。

```text
High
Medium
Low
None
Unknown
```

既存PoCの出力に合わせて使用する。

---

## 列定義

| 列名                       | 必須 | 意味                 | 主な取得元                                            | 公開可否  | 備考                           |
| ------------------------ | -- | ------------------ | ------------------------------------------------ | ----- | ---------------------------- |
| TrainingSampleId         | 必須 | 教師データ上の一意ID        | 新規作成                                             | 可     | `TS-001` のようなサンプルID          |
| ElementId                | 必須 | 既存PoC上の要素識別子       | 品質チェック結果 / AI Readiness Score / pyRevit Metadata | 可     | 既存PoCでは仮ElementIdの場合がある      |
| UniqueId                 | 任意 | Revit由来の安定識別子候補    | pyRevit Metadata                                 | 条件付き可 | GitHub公開用では匿名値のみ使用           |
| Category                 | 必須 | Door / Roomなどのカテゴリ | 品質チェック結果 / Rule Master / pyRevit Metadata        | 可     | 初期MVPではDoor / Room中心         |
| RuleId                   | 必須 | 該当した品質チェックルール      | 品質チェック結果 / Rule Master                           | 可     | ラベル付けの中心キー                   |
| RuleName                 | 必須 | ルール名               | Rule Master / 品質チェック結果                           | 可     | RuleIdの意味を説明する               |
| Severity                 | 必須 | ルールの重要度            | Rule Master / 品質チェック結果                           | 可     | High / Medium / Low等         |
| QualityScore             | 任意 | 品質スコア              | Quality Metrics / AI Readiness Score             | 可     | 参考指標                         |
| AIReadinessScore         | 任意 | AI活用準備度            | AI Readiness Score                               | 可     | FixPriorityの補助指標             |
| HumanReviewRequired      | 必須 | 人による確認が必要か         | 品質チェック結果 / AI Readiness Score                    | 可     | Trueの場合は完全自動判断しない            |
| FixGuideAvailable        | 任意 | Fix Guideが存在するか    | Fix Guide Markdown                               | 可     | True / False                 |
| FixGuideSummary          | 任意 | 修正方針の要約            | Fix Guide Markdown                               | 可     | 修正命令ではなく確認・対応案               |
| IssueSummary             | 必須 | 問題内容の要約            | 品質チェック結果 / AI Context                            | 可     | BIM担当者が内容を確認しやすくする           |
| CurrentFixPriority       | 必須 | 既存PoC上のFixPriority | 既存PoC出力                                          | 可     | 既存ロジックの出力                    |
| ProposedFixPriorityLabel | 必須 | 教師データとしての優先度ラベル    | 人による確認 / 初期ラベル案                                  | 可     | High / Medium / Low / Review |
| LabelReason              | 必須 | ラベル付け理由            | 人による記録                                           | 可     | 空欄不可                         |
| ReviewedBy               | 任意 | レビュー者              | 人による記録                                           | 条件付き可 | GitHub公開用では空欄または匿名           |
| ReviewStatus             | 必須 | レビュー状態             | 人による記録                                           | 可     | Draft / Reviewed / Approved  |
| SourceFile               | 必須 | 元データファイル           | 各PoC出力ファイル                                       | 可     | 根拠確認用                        |
| CreatedDate              | 必須 | 作成日                | 新規作成                                             | 可     | ISO形式またはYYYY-MM-DD           |
| Notes                    | 任意 | 補足                 | 人による記録                                           | 可     | 判断条件や注意点                     |

---

## CurrentFixPriority と ProposedFixPriorityLabel

教師データでは、既存PoCの出力と教師データ用ラベルを分けて扱う。

```text
CurrentFixPriority：
既存PoCで算出した現在のFixPriorityを記録する列。

ProposedFixPriorityLabel：
教師データとして、人が確認・付与する予定の優先度ラベル。
```

方針：

```text
CurrentFixPriority は既存ロジックの出力を記録する
ProposedFixPriorityLabel は教師データ用のラベルとして扱う
両者が一致しない場合は LabelReason または Notes に理由を記録する
ProposedFixPriorityLabel を将来的な教師ラベル候補とする
```

---

## LabelReason

`LabelReason` は必須列とする。

理由：

```text
なぜそのラベルにしたかを後から確認できるようにする
BIM担当者が判断根拠を確認できるようにする
CurrentFixPriority と ProposedFixPriorityLabel が異なる場合の理由を残す
Reviewラベルの判断保留理由を明確にする
```

方針：

```text
LabelReasonが空欄の教師データは初期MVPでは不完全なデータとして扱う
Reviewラベルの場合は判断保留の理由を必ず記録する
HumanReviewRequired=Trueの場合は人間確認が必要な理由を記録する
```

---

## Reviewラベル

`Review` は、High / Medium / Low のいずれかに機械的に分類できない場合に使う。

重要な点：

```text
Review は優先度が低いという意味ではない
Review は人による判断が必要という意味である
Review の行では LabelReason に判断保留の理由を必ず記録する
```

例：

```text
プロジェクト条件によって判断が変わる
入力情報だけでは優先度を判断できない
HumanReviewRequired=TrueだがSeverityだけでは優先度を決められない
Zone管理の有無など運用条件に依存する
```

---

## HumanReviewRequiredとの関係

`HumanReviewRequired` は、FixPriority教師データ設計で重要な列とする。

方針：

```text
HumanReviewRequired=Trueの場合、FixPriorityを完全自動決定しない
Reviewラベルの候補とする
SeverityがHighの場合はHigh候補にもなり得る
ラベル理由に、人による確認が必要な理由を記録する
```

---

## 取得元ファイル

第3段階Eでは、以下の既存PoC出力を参照対象とする。

```text
04_output_csv/check_results_revit_v002.csv
04_output_csv/ai_readiness_scores_v001.csv
04_output_csv/fix_guides_v001.md
02_rule_master/bim_rule_master_v003.csv
04_output_csv/check_results_room_v001.csv
04_output_csv/room_ai_readiness_scores_v001.csv
04_output_csv/room_fix_guides_v001.md
03_input_csv/pyrevit_element_metadata_sample_v001.csv
```

---

## 既存PoC出力との対応

| 教師データ列                   | 主な対応元                                     | 備考                                    |
| ------------------------ | ----------------------------------------- | ------------------------------------- |
| ElementId                | 品質チェック結果 / AI Readiness Score             | Doorは建具表上の仮ID、RoomはPhase 3B用仮IDの場合がある |
| UniqueId                 | pyRevit Metadata                          | 実モデル由来UniqueIdはGitHub公開時に使用しない        |
| Category                 | 品質チェック結果 / Rule Master / pyRevit Metadata | Door / Room                           |
| RuleId                   | 品質チェック結果 / Rule Master                    | ラベル付けの中心キー                            |
| RuleName                 | Rule Master                               | ルール名                                  |
| Severity                 | Rule Master / 品質チェック結果                    | 優先度判断の補助                              |
| QualityScore             | Quality Metrics / AI Readiness Score      | 参考指標                                  |
| AIReadinessScore         | AI Readiness Score                        | 参考指標                                  |
| HumanReviewRequired      | 品質チェック結果 / AI Readiness Score             | Trueの場合は人間確認を明記                       |
| FixGuideAvailable        | Fix Guide Markdown                        | Fix Guideの有無                          |
| FixGuideSummary          | Fix Guide Markdown                        | 要約して記録                                |
| IssueSummary             | 品質チェック結果 / AI Context                     | 問題内容                                  |
| CurrentFixPriority       | 既存PoC出力                                   | 既存ロジックの結果                             |
| ProposedFixPriorityLabel | 人による確認                                    | 教師データ用ラベル                             |
| LabelReason              | 人による確認                                    | 必須                                    |
| SourceFile               | 各入力ファイル                                   | 根拠ファイル                                |

---

## GitHub公開方針

GitHubに含めてよいもの：

```text
公開可能なPoC用サンプル
匿名化したサンプル教師データ
列設計
ラベル付け方針
サンプルCSV
サンプルMarkdown
```

GitHubに含めないもの：

```text
実案件データ
社外秘モデル由来の情報
顧客名
プロジェクト名
個人名
担当者名
実際のレビュー者名
社内固有の分類コード
機密性の高い仕様情報
```

公開用サンプルでは、`ReviewedBy` は空欄または匿名値とする。

---

## CSV品質検証候補

第3段階Eでは、pytestで以下を検証する候補とする。

```text
CSVを読み込めること
必須列がすべて存在すること
TrainingSampleIdが空でないこと
TrainingSampleIdが重複していないこと
ProposedFixPriorityLabelが High / Medium / Low / Review のいずれかであること
LabelReasonが空でないこと
ReviewStatusが Draft / Reviewed / Approved のいずれかであること
Categoryが Door / Room / Other のいずれかであること
RuleIdが空でないこと
SourceFileが空でないこと
HumanReviewRequired=True の行で LabelReason が空でないこと
```

---

## 制約

この列設計には以下の制約がある。

```text
PoC用の初期設計であり、実務上の正式な優先度基準ではない
サンプル教師データはモデル学習用ではない
FixPriorityは最終判断ではない
Severityだけで優先度を決定しない
AIReadinessScoreだけで優先度を決定しない
HumanReviewRequired=Trueの場合は人間確認を前提とする
実案件データは使用しない
GitHub公開用データは匿名サンプルに限定する
```

---

## 完了条件

このドキュメントは、以下を満たした時点で完了とする。

```text
教師データCSVの列一覧を定義した
必須列と任意列を分けた
ProposedFixPriorityLabelの許可値を定義した
ReviewStatusの許可値を定義した
Categoryの許可値を定義した
列ごとの意味、取得元、公開可否、備考を整理した
CurrentFixPriority と ProposedFixPriorityLabel の違いを整理した
LabelReasonを必須列として定義した
既存PoC出力との対応を整理した
GitHub公開方針を整理した
pytestで検証する候補を整理した
```
