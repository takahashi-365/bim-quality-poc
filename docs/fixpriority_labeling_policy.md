# FixPriorityラベル付け方針

## 目的

このドキュメントでは、第3段階E：FixPriority教師データ設計における `ProposedFixPriorityLabel` のラベル候補、意味、付与方針を定義する。

本方針は、将来的に `FixPriority` を分析・学習・レビューに活用するためのラベル設計である。

ただし、本段階では機械学習モデルの作成、モデル学習、精度評価、自動優先度判定は行わない。

初期MVPでは、ルールベースの初期案と人による確認を前提に、ラベル候補と判断理由の記録方法を整理する。

---

## 前提

第3段階Eでは、以下を明確に分ける。

```text
教師データ設計：
将来的に学習・分析・レビューに使えるよう、入力情報、ラベル、判断理由を整理すること。

自動判定：
入力データから機械的にFixPriorityを決定すること。
```

第3段階Eでは、自動判定の本格実装は行わない。

また、FixPriorityは最終判断ではない。
最終的な対応順序は、BIM担当者がプロジェクト状況、設計意図、納品要件、データ利用目的を踏まえて判断する。

---

## ラベル対象

ラベルを付与する単位は以下とする。

```text
1要素 × 1 RuleId
```

方針：

```text
1つの要素に1つのRuleId違反がある場合は1行として記録する
1つの要素に複数のRuleId違反がある場合はRuleIdごとに複数行として記録する
要素全体の総合優先度は将来拡張とする
```

---

## ProposedFixPriorityLabel の許可値

初期MVPでは、`ProposedFixPriorityLabel` の許可値を以下に限定する。

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

代表例：

```text
Severity が High の RuleId に該当する
AI Readiness Score への影響が大きい
分類コードや部屋名など、AI活用・検索・集計に重要な情報が欠けている
HumanReviewRequired=True かつ影響が大きい
```

注意：

```text
High は「AIが自動で修正してよい」という意味ではない
High は「BIM担当者が優先的に確認した方がよい」という意味である
```

---

### Medium

確認した方がよいが、Highほど緊急性が高くない問題。

代表例：

```text
Severity が Medium の RuleId に該当する
BIや集計には影響するが、要素識別そのものは可能
AreaやLevelなどの一部情報が不足している
後工程やAI活用への影響はあるが、Highほど致命的ではない
```

---

### Low

将来的には整備した方がよいが、初期MVPでは優先度が低い問題。

代表例：

```text
Severity が Low の RuleId に該当する
Zoneなど、プロジェクトによっては存在しない情報
AI活用上の補助的な文脈情報が不足している
現時点のPoCでは主要な品質判定に直結しない
```

注意：

```text
Low は「不要」という意味ではない
Low は「初期MVPでは相対的に優先度が低い」という意味である
```

---

### Review

`Review` は、High / Medium / Low のいずれかに機械的に分類できない場合に使う。

重要な点：

```text
Review は優先度が低いという意味ではない
Review は人による判断が必要という意味である
Review の行では LabelReason に判断保留の理由を必ず記録する
```

代表例：

```text
ルール違反ではあるが、プロジェクト条件によって判断が変わる
入力情報だけでは優先度を判断できない
HumanReviewRequired=Trueだが、Severityだけでは優先度を決められない
Zone管理の有無など、運用条件に依存する
```

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

方針：

```text
なぜそのラベルにしたかを記録する
後からBIM担当者が判断根拠を確認できるようにする
CurrentFixPriority と ProposedFixPriorityLabel が異なる場合は、その理由を記録する
Review ラベルの場合は、判断保留の理由を必ず記録する
```

LabelReason が空欄の教師データは、初期MVPでは不完全なデータとして扱う。

---

## 初期ラベル付け方針

初期MVPでは、完全自動ラベルではなく、ルールベースの初期案と人による確認を前提とする。

基本方針：

```text
Severity が High の場合は High 候補
Severity が Medium の場合は Medium 候補
Severity が Low の場合は Low 候補
HumanReviewRequired=True の場合は Review または High 候補
AIReadinessScore が低い場合は優先度を上げる候補
FixGuide がある場合は対応案を提示しやすい
入力情報だけで判断できない場合は Review にする
LabelReason を必ず記録する
```

---

## 初期ラベル付けルール案

| 条件                                            | ProposedFixPriorityLabel |
| --------------------------------------------- | ------------------------ |
| Severity = High かつ HumanReviewRequired = True | High または Review          |
| Severity = High かつ AIReadinessScore が低い       | High                     |
| Severity = Medium                             | Medium                   |
| Severity = Low                                | Low                      |
| ZoneMissingなどプロジェクト依存の項目                      | Low または Review           |
| 入力情報だけで判断できない                                 | Review                   |

注意：

```text
このルールはPoC用の初期案であり、正式な優先度判定基準ではない
最終的なラベルはBIM担当者が確認する
```

---

## HumanReviewRequiredとの関係

`HumanReviewRequired` は、FixPriorityラベル設計で重要な判断材料とする。

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

## Severityとの関係

`Severity` は、FixPriorityラベル付けの重要な補助情報である。

方針：

```text
Severity は初期ラベル候補を決めるための出発点とする
Severity だけで ProposedFixPriorityLabel を決定しない
Category、AIReadinessScore、HumanReviewRequired、FixGuide、IssueSummaryと組み合わせて判断する
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

## Door / Roomカテゴリとの関係

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

## ラベル付け時の禁止事項

以下は禁止する。

```text
AIが設計判断を行う
AIが施工判断を行う
AIが法規適合性の最終判断を行う
AIがRevitモデルを自動修正する
Severityだけで正式な優先度を決める
AIReadinessScoreだけで正式な優先度を決める
HumanReviewRequired=Trueを無視する
Reviewラベルを低優先度として扱う
Fix Guideを修正命令として扱う
入力情報にない内容を断定する
```

---

## GitHub公開方針

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

公開用サンプルでは、`ReviewedBy` は空欄または匿名値とする。

---

## 完了条件

このドキュメントは、以下を満たした時点で完了とする。

```text
ProposedFixPriorityLabel の許可値を定義した
High / Medium / Low / Review の意味を定義した
Review が低優先度ではなく人による判断が必要な状態であることを明記した
CurrentFixPriority と ProposedFixPriorityLabel の違いを整理した
LabelReasonを必須とした
初期ラベル付けルール案を整理した
HumanReviewRequiredとの関係を整理した
Severityとの関係を整理した
AI Readiness Scoreとの関係を整理した
RuleIdとの関係を整理した
Door / Roomカテゴリとの関係を整理した
Fix Guideとの関係を整理した
禁止事項を整理した
GitHub公開方針を整理した
```
