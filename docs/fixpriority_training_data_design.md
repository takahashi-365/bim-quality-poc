# 第3段階E：FixPriority教師データ設計

## 目的

第3段階Eでは、既存の `BIM Data Quality & AI Readiness Assessment PoC` で扱っている `FixPriority` を、将来的に教師データとして扱えるようにするための設計を行う。

この段階では、機械学習モデルを本格的に作成しない。
目的は、BIMデータ品質チェック結果、RuleId、Severity、AI Readiness Score、HumanReviewRequired、Fix Guideなどをもとに、どのような情報を教師データとして蓄積すべきかを整理することである。

第3段階Eで作成するサンプル教師データは、**モデル学習用データではなく、列設計とラベル付け方針を確認するための小規模サンプル**とする。

---

## 位置づけ

第3段階Eは、新規PoCではなく、既存PoCの第3段階拡張である。

第2段階まで：

```text
Revit Schedule TXT
↓
CSV変換
↓
品質チェック
↓
QualityScore
↓
FixPriority prototype
↓
AI Readiness Score
↓
AI Context
↓
Fix Guide
```

第3段階A〜D：

```text
A：Local LLM Explanation Demo
B：Roomカテゴリ追加
C：pyRevitでElementId / UniqueId取得PoC
D：RAG / Azure AI Search構成検討
```

第3段階E：

```text
RuleId
Severity
QualityScore
AI Readiness Score
HumanReviewRequired
Fix Guide
ElementId / UniqueId
Door / Roomカテゴリ
↓
FixPriority教師データ設計
```

---

## 第3段階Eでやること

* 既存のFixPriorityの考え方を整理する
* 「教師データ設計」と「自動判定」を明確に分ける
* 教師データ1行の単位を定義する
* FixPriorityを教師ラベルとして扱う場合の候補値を定義する
* `CurrentFixPriority` と `ProposedFixPriorityLabel` の違いを明確にする
* `Review` ラベルの意味を定義する
* 教師データに含める特徴量候補を整理する
* Door / Roomカテゴリの違いを教師データにどう含めるか検討する
* RuleId、Severity、AI Readiness Score、HumanReviewRequiredとの関係を整理する
* BIM担当者による判断が必要な項目を整理する
* 教師データCSVの列設計を作成する
* サンプル教師データを少量作成する
* ラベル付けルールをdocsに記録する
* pytestで検証するCSV品質項目を整理する
* GitHub公開範囲と非公開範囲を整理する
* 将来的に機械学習や分析へ接続する場合の制約を整理する
* 既存PoCの出力と接続できるか確認する

---

## 第3段階Eでやらないこと

```text
本格的な機械学習モデル作成
モデル学習
モデル精度評価
ファインチューニング
深層学習
自動ラベル付けの本格実装
FixPriorityの完全自動判定
設計判断・施工判断の自動化
Revitモデル自動修正
実案件データを使った教師データ作成
大量データ収集
本番運用設計
```

この段階では、**教師データとして何を蓄積すべきかを設計すること**に限定する。

---

## 教師データと自動判定の違い

第3段階Eでは、教師データ設計とFixPriorityの自動判定を明確に分ける。

```text
教師データ設計：
将来的に学習・分析・レビューに使えるよう、入力情報、ラベル、判断理由を整理すること。

自動判定：
入力データから機械的にFixPriorityを決定すること。
```

第3段階Eでは、自動判定の本格実装は行わない。
初期MVPでは、ルールベースの初期案と人による確認を前提に、教師データの列構成とラベル付け方針を整理する。

---

## 教師データ1行の単位

教師データの1行は、原則として以下の単位とする。

```text
1要素 × 1 RuleId
```

方針：

```text
1つの要素に1つのRuleId違反がある場合は、1行として記録する
1つの要素に複数のRuleId違反がある場合は、RuleIdごとに複数行として記録する
要素全体の総合優先度を扱う場合は、将来拡張とする
```

理由：

* RuleIdごとの品質問題とFix Guideを対応させやすい
* LabelReasonをRuleId単位で記録しやすい
* Door / Roomカテゴリごとの優先度傾向を分析しやすい
* 将来的にRuleId別の傾向分析につなげやすい

---

## FixPriorityの位置づけ

FixPriorityは、BIMデータ品質上の問題に対して、どの修正を優先すべきかを示すためのPoC用指標である。

ただし、FixPriorityは最終判断ではない。
最終的な対応順序は、BIM担当者がプロジェクト状況、設計意図、納品要件、データ利用目的を踏まえて判断する。

第3段階Eでは、FixPriorityを以下のように位置づける。

```text
品質チェック結果を整理するための優先度ラベル
将来の教師データ候補
BIM担当者の判断を補助するための参考情報
AI Readiness ScoreやHumanReviewRequiredと組み合わせて使う補助指標
```

---

## CurrentFixPriority と ProposedFixPriorityLabel の違い

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
両者が一致しない場合は、LabelReason または Notes に理由を記録する
ProposedFixPriorityLabel を将来的な教師ラベル候補とする
```

これにより、既存PoCの自動出力と、人が確認した教師データ用ラベルを混同しないようにする。

---

## FixPriorityラベル案

初期MVPでは、ラベルを増やしすぎない。

`ProposedFixPriorityLabel` の許可値は以下とする。

```text
High
Medium
Low
Review
```

空欄やその他の値は、初期MVPでは許可しない。

---

## ラベル定義

### High

優先的に確認・修正した方がよい問題。

例：

```text
High SeverityのRuleIdに該当する
AI Readiness Scoreへの影響が大きい
分類コードや部屋名など、AI活用・検索・集計に重要な情報が欠けている
HumanReviewRequired=True かつ影響が大きい
```

---

### Medium

確認した方がよいが、Highほど緊急性が高くない問題。

例：

```text
Medium SeverityのRuleIdに該当する
BIや集計には影響するが、要素識別そのものは可能
AreaやLevelなどの一部情報が不足している
```

---

### Low

将来的には整備した方がよいが、初期MVPでは優先度が低い問題。

例：

```text
Low SeverityのRuleIdに該当する
Zoneなど、プロジェクトによっては存在しない情報
AI活用上の補助的な文脈情報が不足している
```

---

### Review

`Review` は、High / Medium / Low のいずれかに機械的に分類できない場合に使う。

重要な点：

```text
Review は優先度が低いという意味ではない
Review は人による判断が必要という意味である
Review の行では、LabelReason に判断保留の理由を必ず記録する
```

例：

```text
ルール違反ではあるが、プロジェクト条件によって判断が変わる
入力情報だけでは優先度を判断できない
HumanReviewRequired=Trueだが、Severityだけでは優先度を決められない
Zone管理の有無など、運用条件に依存する
```

---

## LabelReasonの扱い

`LabelReason` は必須列とする。

方針：

```text
なぜそのラベルにしたかを記録する
後からBIM担当者が判断根拠を確認できるようにする
CurrentFixPriority と ProposedFixPriorityLabel が異なる場合は、その理由を記録する
Review ラベルの場合は、判断保留の理由を必ず記録する
```

LabelReasonが空欄の教師データは、初期MVPでは不完全なデータとして扱う。

---

## ReviewStatusの扱い

`ReviewStatus` の許可値は、初期MVPでは以下とする。

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

## 教師データに含める列案

初期MVPでは、以下の列を候補とする。

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

## 列の意味

| 列名                       | 意味                          |
| ------------------------ | --------------------------- |
| TrainingSampleId         | 教師データ上の一意ID                 |
| ElementId                | 既存PoC上の要素識別子                |
| UniqueId                 | Revit由来の安定識別子候補             |
| Category                 | Door / Roomなどのカテゴリ          |
| RuleId                   | 該当した品質チェックルール               |
| RuleName                 | ルール名                        |
| Severity                 | ルールの重要度                     |
| QualityScore             | 品質スコア                       |
| AIReadinessScore         | AI活用準備度                     |
| HumanReviewRequired      | 人による確認が必要か                  |
| FixGuideAvailable        | Fix Guideが存在するか             |
| FixGuideSummary          | 修正方針の要約                     |
| IssueSummary             | 問題内容の要約                     |
| CurrentFixPriority       | 既存PoC上のFixPriority          |
| ProposedFixPriorityLabel | 教師データとしての優先度ラベル             |
| LabelReason              | ラベル付け理由。必須                  |
| ReviewedBy               | レビュー者。公開用では匿名または空欄          |
| ReviewStatus             | Draft / Reviewed / Approved |
| SourceFile               | 元データファイル                    |
| CreatedDate              | 作成日                         |
| Notes                    | 補足                          |

---

## 必須列と任意列

初期MVPの必須列：

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

任意列：

```text
UniqueId
QualityScore
AIReadinessScore
FixGuideAvailable
FixGuideSummary
ReviewedBy
Notes
```

ただし、`ReviewedBy` はGitHub公開用では空欄または匿名とする。

---

## ラベル付け方針

初期MVPでは、完全自動ラベルではなく、ルールベースの初期案 + 人による確認を前提とする。

基本方針：

```text
SeverityがHighの場合はHigh候補
SeverityがMediumの場合はMedium候補
SeverityがLowの場合はLow候補
HumanReviewRequired=Trueの場合はReviewまたはHigh候補
AIReadinessScoreが低い場合は優先度を上げる候補
FixGuideがある場合は対応案を提示しやすい
入力情報だけで判断できない場合はReviewにする
LabelReasonを必ず記録する
```

---

## 初期ラベル付けルール案

| 条件                                            | ProposedFixPriorityLabel |
| --------------------------------------------- | ------------------------ |
| Severity = High かつ HumanReviewRequired = True | High または Review          |
| Severity = High かつ AIReadinessScoreが低い        | High                     |
| Severity = Medium                             | Medium                   |
| Severity = Low                                | Low                      |
| ZoneMissingなどプロジェクト依存の項目                      | Low または Review           |
| 入力情報だけで判断できない                                 | Review                   |

注意：

```text
このルールはPoC用の初期案であり、正式な優先度判定基準ではない。
最終的なラベルはBIM担当者が確認する。
```

---

## HumanReviewRequiredとの関係

`HumanReviewRequired` は、FixPriority設計で重要な列とする。

方針：

```text
HumanReviewRequired=Trueの場合、FixPriorityを完全自動決定しない
Reviewラベルの候補とする
SeverityがHighの場合はHigh候補にもなり得る
ラベル理由に、人による確認が必要な理由を記録する
```

例：

```text
HumanReviewRequired=True
Severity=High
AIReadinessScore=Low
→ ProposedFixPriorityLabel=High
→ LabelReason=分類コード未入力でAI活用・検索・外部連携に影響が大きいため
```

または、

```text
HumanReviewRequired=True
Severity=Low
ZoneMissing
→ ProposedFixPriorityLabel=Review
→ LabelReason=Zone管理の有無はプロジェクト条件によるため
```

---

## Door / Roomカテゴリの扱い

FixPriority教師データでは、Door / Roomカテゴリを区別する。

理由：

```text
DoorとRoomでは重要な欠損項目が異なる
Doorでは分類コード、建具番号、ファミリ名などが重要
Roomでは部屋名、部屋番号、面積、階、分類コードなどが重要
同じSeverityでもカテゴリによって対応優先度が異なる可能性がある
```

方針：

```text
Category列を必須とする
RuleIdとCategoryを組み合わせてラベル理由を整理する
Door用ルールとRoom用ルールを分けて確認できるようにする
```

---

## RuleIdとの関係

FixPriority教師データでは、RuleIdをラベル付けの中心キーとする。

方針：

```text
RuleIdごとに優先度傾向を整理する
RuleIdとFix Guideを関連付ける
RuleIdごとのLabelReasonを蓄積する
将来的にRuleId別の優先度傾向を分析できるようにする
```

例：

```text
D-002：分類コード未入力 → High候補
R-101：RoomName未入力 → High候補
R-103：Area未入力または0 → Medium候補
R-105：ZoneMissing → LowまたはReview候補
```

---

## AI Readiness Scoreとの関係

AI Readiness Scoreは、FixPriorityラベルを補助する指標として扱う。

方針：

```text
AIReadinessScoreが低い要素は優先度を上げる候補とする
ただし、AIReadinessScoreだけでFixPriorityを決定しない
RuleId、Severity、HumanReviewRequired、FixGuideと組み合わせて判断する
```

---

## Fix Guideとの関係

Fix Guideは、ラベル付け理由と対応案の根拠として扱う。

方針：

```text
Fix Guideが存在するRuleIdは、対応案を説明しやすい
FixGuideSummaryを教師データに含める
LabelReasonにはFix Guideに基づく理由を記録する
ただし、Fix Guideは修正提案であり、最終判断ではない
```

---

## セキュリティ・公開範囲

GitHubに含めてよいもの：

```text
公開可能なPoC用サンプル
匿名化したサンプル教師データ
ラベル付け方針
列設計
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

方針：

```text
ReviewedByはGitHub公開用では空欄または匿名にする
実案件データは使わない
公開可能なPoC用サンプルのみ使う
```

---

## 想定成果物

### docs

```text
docs/fixpriority_training_data_design.md
docs/fixpriority_labeling_policy.md
docs/fixpriority_training_columns.md
docs/fixpriority_limitations.md
```

### sample data

```text
07_fixpriority_training/fixpriority_training_samples_v001.csv
07_fixpriority_training/fixpriority_label_examples_v001.md
```

第3段階Eでは、`07_fixpriority_training/` を新規フォルダとして作成してもよい。

---

## サンプル教師データ案

このサンプル教師データは、モデル学習用データではなく、列設計とラベル付け方針を確認するための小規模サンプルである。

CSV例：

```csv
TrainingSampleId,ElementId,UniqueId,Category,RuleId,RuleName,Severity,QualityScore,AIReadinessScore,HumanReviewRequired,FixGuideAvailable,FixGuideSummary,IssueSummary,CurrentFixPriority,ProposedFixPriorityLabel,LabelReason,ReviewedBy,ReviewStatus,SourceFile,CreatedDate,Notes
TS-001,12345,sample-unique-id,Door,D-002,ClassificationCodeMissing,High,60,45,True,True,分類コード確認を提案,分類コードが未入力,High,High,分類コード未入力は検索・集計・AI活用に影響が大きいため,,Draft,check_results_revit_v002.csv,2026-06-14,PoC用サンプル
TS-002,R-ROOM-001,,Room,R-103,AreaMissingOrZero,Medium,75,65,False,True,面積入力確認を提案,面積が未入力または0,Medium,Medium,面積分析やBI利用に影響するため,,Draft,check_results_room_v001.csv,2026-06-14,PoC用サンプル
TS-003,R-ROOM-002,,Room,R-105,ZoneMissing,Low,85,80,True,True,Zone管理有無の確認を提案,Zoneが未入力,Low,Review,Zone管理の有無はプロジェクト条件によるため,,Draft,check_results_room_v001.csv,2026-06-14,PoC用サンプル
```

注意：

```text
実案件データは使わない
公開可能なPoC用サンプルのみ使う
ReviewedByはGitHub公開時には空欄または匿名にする
このサンプルは学習用ではなく設計確認用である
```

---

## 作業手順

### Step 1：作業前状態を確認する

```powershell
git status
```

作業ブランチを分ける場合：

```powershell
git checkout -b phase3e-fixpriority-training-design
```

---

### Step 2：教師データ設計用フォルダを作成する

```text
07_fixpriority_training/
```

作成候補：

```powershell
mkdir 07_fixpriority_training
```

---

### Step 3：設計メインドキュメントを作成する

作成ファイル：

```text
docs/fixpriority_training_data_design.md
```

記載内容：

```text
目的
対象範囲
やること
やらないこと
教師データと自動判定の違い
教師データ1行の単位
FixPriorityの位置づけ
CurrentFixPriority と ProposedFixPriorityLabel の違い
ラベル候補
Reviewラベルの定義
教師データ列設計
LabelReasonの扱い
ラベル付け方針
HumanReviewRequiredとの関係
Door / Roomカテゴリの扱い
RuleIdとの関係
AI Readiness Scoreとの関係
Fix Guideとの関係
セキュリティ・公開範囲
制約
完了条件
```

---

### Step 4：既存PoC出力を確認する

確認対象：

```text
check_results_revit_v002.csv
ai_readiness_scores_v001.csv
fix_guides_v001.md
bim_rule_master_v003.csv
Room用品質チェック結果
Room用AI Readiness Score
Room用Fix Guide
pyRevit Metadata
```

目的：

```text
教師データに使える列を確認する
不足している列を整理する
既存出力と教師データ列案を対応付ける
```

---

### Step 5：教師データ列設計を作成する

作成ファイル：

```text
docs/fixpriority_training_columns.md
```

整理内容：

```text
列名
意味
必須 / 任意
取得元
公開可否
備考
```

---

### Step 6：ラベル候補を定義する

初期ラベル候補：

```text
High
Medium
Low
Review
```

作成ファイル：

```text
docs/fixpriority_labeling_policy.md
```

---

### Step 7：ラベル付けルールを整理する

整理する観点：

```text
Severity
AIReadinessScore
HumanReviewRequired
RuleId
Category
FixGuideAvailable
```

注意：

```text
ルールベースの初期案であり、正式な自動判定ではない
BIM担当者による確認を前提にする
LabelReasonを必ず記録する
```

---

### Step 8：サンプル教師データを作成する

作成ファイル：

```text
07_fixpriority_training/fixpriority_training_samples_v001.csv
```

内容：

```text
5〜10件程度の小さなサンプル
DoorとRoomを両方含める
High / Medium / Low / Review を含める
列案とサンプルCSVの列を揃える
LabelReasonを必ず入れる
ReviewedByは空欄または匿名にする
実案件データは使わない
学習用ではなく設計確認用サンプルとして扱う
```

---

### Step 9：ラベル例をMarkdownで整理する

作成ファイル：

```text
07_fixpriority_training/fixpriority_label_examples_v001.md
```

記載内容：

```text
サンプルID
入力情報
CurrentFixPriority
ProposedFixPriorityLabel
ラベル理由
BIM担当者確認が必要な点
注意点
```

---

### Step 10：制約を整理する

作成ファイル：

```text
docs/fixpriority_limitations.md
```

制約例：

```text
教師データ件数が少ない
PoC用サンプルであり実案件データではない
サンプルCSVは学習用ではなく設計確認用である
FixPriorityは正式な優先度基準ではない
HumanReviewRequired=Trueの場合は自動判断しない
Severityだけでは優先度を決められない
プロジェクト条件により優先度が変わる
モデル学習は本段階では行わない
```

---

### Step 11：pytest対象を検討する

第3段階Eでは、モデル学習ではなくCSV設計の検証を行う。

候補：

```text
tests/test_fixpriority_training_data.py
```

確認対象：

```text
教師データCSVを読み込めるか
必須列がすべて存在するか
TrainingSampleIdが空でないか
TrainingSampleIdが重複していないか
ProposedFixPriorityLabelが High / Medium / Low / Review のいずれか
LabelReasonが空でないか
HumanReviewRequired=True の行で LabelReason が空でないか
ReviewStatusが Draft / Reviewed / Approved のいずれか
Categoryが Door / Room / Other のいずれか
RuleIdが空でないか
SourceFileが空でないか
```

---

### Step 12：README反映判断

第3段階E単体では、READMEを大きく更新しない。

READMEに反映する場合は、以下のように小さく記載する。

```text
FixPriorityを将来的な教師データとして扱うため、RuleId、Severity、AI Readiness Score、HumanReviewRequired、Fix Guideを用いたラベル設計を検討しています。
```

Portfolio PDFの更新は、第3段階A〜Eがまとまってから検討する。

---

## 完了条件

第3段階Eの完了条件は以下。

```text
FixPriorityの位置づけを整理した
教師データと自動判定の違いを整理した
教師データ1行の単位を「1要素 × 1 RuleId」として整理した
CurrentFixPriority と ProposedFixPriorityLabel の違いを整理した
FixPriorityラベル候補を定義した
Reviewラベルの意味を整理した
ProposedFixPriorityLabelの許可値を定義した
ReviewStatusの許可値を定義した
LabelReasonを必須列として整理した
教師データ列案を作成した
既存PoC出力との対応を整理した
Door / Roomカテゴリの扱いを整理した
RuleIdとの関係を整理した
Severityとの関係を整理した
AI Readiness Scoreとの関係を整理した
HumanReviewRequiredとの関係を整理した
Fix Guideとの関係を整理した
サンプル教師データCSVを作成した
サンプルCSVと列案の整合を取った
ラベル例Markdownを作成した
GitHub公開範囲と非公開範囲を整理した
制約をdocsに記録した
pytest対象を整理した
README反映要否を判断した
```

---

## 成功とみなす状態

以下の状態になれば、第3段階EのMVPとして成功とする。

```text
既存PoC出力
↓
FixPriority教師データ列設計
↓
1要素 × 1 RuleId の行単位定義
↓
CurrentFixPriority / ProposedFixPriorityLabel の整理
↓
ラベル候補定義
↓
ラベル付け方針
↓
サンプル教師データCSV
↓
LabelReasonの記録
↓
制約整理
```

この段階では、機械学習モデルを作らない。
重要なのは、将来的にFixPriorityを学習・分析に使う場合、どの情報をどの列として蓄積すべきかを明確にすることである。

---

## 次段階への接続

第3段階Eにより、将来的に以下へ接続しやすくなる。

```text
FixPriority傾向分析
RuleId別の優先度傾向確認
BIM担当者レビュー結果の蓄積
AI Readiness改善施策の分析
将来的な機械学習モデル検討
```

ただし、これらは第3段階Eの範囲外とする。
