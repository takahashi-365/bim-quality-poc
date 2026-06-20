# FixPriorityラベル例

## 目的

このドキュメントでは、第3段階E：FixPriority教師データ設計で作成したサンプル教師データについて、ラベル付けの考え方を例として整理する。

対象CSVは以下とする。

```text id="qmt357"
07_fixpriority_training/fixpriority_training_samples_v001.csv
```

このサンプルは、モデル学習用データではない。
列設計、ラベル候補、LabelReason、Reviewラベルの扱いを確認するための小規模サンプルである。

---

## 前提

第3段階Eでは、教師データ1行の単位を以下とする。

```text id="2ewbwb"
1要素 × 1 RuleId
```

`ProposedFixPriorityLabel` の許可値は以下とする。

```text id="e8saem"
High
Medium
Low
Review
```

`Review` は低優先度ではなく、人による判断が必要な状態を示す。

---

## サンプル一覧

| TrainingSampleId | Category | RuleId | RuleName                  | CurrentFixPriority | ProposedFixPriorityLabel | ReviewStatus |
| ---------------- | -------- | ------ | ------------------------- | ------------------ | ------------------------ | ------------ |
| TS-001           | Door     | D-002  | ClassificationCodeMissing | High               | High                     | Draft        |
| TS-002           | Door     | D-003  | DoorNumberMissing         | Medium             | Medium                   | Draft        |
| TS-003           | Door     | D-005  | FamilyNameMissing         | Low                | Low                      | Draft        |
| TS-004           | Room     | R-101  | RoomNameMissing           | High               | High                     | Draft        |
| TS-005           | Room     | R-102  | RoomNumberMissing         | High               | High                     | Draft        |
| TS-006           | Room     | R-103  | AreaMissingOrZero         | Medium             | Medium                   | Draft        |
| TS-007           | Room     | R-105  | ZoneMissing               | Low                | Review                   | Draft        |
| TS-008           | Door     | D-004  | LevelNameMissing          | Medium             | Review                   | Draft        |

---

## TS-001：Door / ClassificationCodeMissing

### 入力情報

| 項目                       | 値                         |
| ------------------------ | ------------------------- |
| TrainingSampleId         | TS-001                    |
| Category                 | Door                      |
| RuleId                   | D-002                     |
| RuleName                 | ClassificationCodeMissing |
| Severity                 | High                      |
| HumanReviewRequired      | True                      |
| CurrentFixPriority       | High                      |
| ProposedFixPriorityLabel | High                      |

### ラベル理由

分類コード未入力は、検索、集計、AI活用に影響が大きいため、`High` とする。

### BIM担当者確認が必要な点

```text id="by8gsv"
分類コードの入力ルールがプロジェクト内で定義されているか
対象建具にどの分類コードを付与すべきか
外部連携やCOBie等の用途で分類コードが必要か
```

### 注意点

`High` はAIが自動修正してよいという意味ではない。
BIM担当者が優先的に確認した方がよいという意味である。

---

## TS-002：Door / DoorNumberMissing

### 入力情報

| 項目                       | 値                 |
| ------------------------ | ----------------- |
| TrainingSampleId         | TS-002            |
| Category                 | Door              |
| RuleId                   | D-003             |
| RuleName                 | DoorNumberMissing |
| Severity                 | Medium            |
| HumanReviewRequired      | False             |
| CurrentFixPriority       | Medium            |
| ProposedFixPriorityLabel | Medium            |

### ラベル理由

建具番号は、建具の識別や集計に影響するため、`Medium` とする。

### BIM担当者確認が必要な点

```text id="kuydo2"
建具番号の採番ルールがあるか
建具表とモデル内パラメータが一致しているか
番号未入力が意図的なものか
```

### 注意点

建具番号の不足は重要だが、分類コード未入力ほどAI活用全体への影響が大きいとは限らないため、初期MVPでは `Medium` とする。

---

## TS-003：Door / FamilyNameMissing

### 入力情報

| 項目                       | 値                 |
| ------------------------ | ----------------- |
| TrainingSampleId         | TS-003            |
| Category                 | Door              |
| RuleId                   | D-005             |
| RuleName                 | FamilyNameMissing |
| Severity                 | Low               |
| HumanReviewRequired      | False             |
| CurrentFixPriority       | Low               |
| ProposedFixPriorityLabel | Low               |

### ラベル理由

初期MVPでは主要判定への影響が限定的だが、将来的な整理対象となるため、`Low` とする。

### BIM担当者確認が必要な点

```text id="9qlnnq"
ファミリ名が本当に取得できないのか
出力条件やカテゴリ設定に起因する欠損か
将来的なRAGや検索でファミリ名を使う必要があるか
```

### 注意点

`Low` は不要という意味ではない。
初期MVPでは相対的に優先度が低いという意味である。

---

## TS-004：Room / RoomNameMissing

### 入力情報

| 項目                       | 値               |
| ------------------------ | --------------- |
| TrainingSampleId         | TS-004          |
| Category                 | Room            |
| RuleId                   | R-101           |
| RuleName                 | RoomNameMissing |
| Severity                 | High            |
| HumanReviewRequired      | True            |
| CurrentFixPriority       | High            |
| ProposedFixPriorityLabel | High            |

### ラベル理由

部屋名未入力は、検索、集計、AI文脈生成に影響が大きく、人による確認も必要なため、`High` とする。

### BIM担当者確認が必要な点

```text id="ztp8vt"
正しい部屋名が設計上定義されているか
建築モデルと設備モデルで部屋名の扱いが一致しているか
部屋名が未入力なのか、別の列に記録されているのか
```

### 注意点

Roomカテゴリでは、部屋名はAI ContextやRAGの文脈にも影響するため、重要度が高い。

---

## TS-005：Room / RoomNumberMissing

### 入力情報

| 項目                       | 値                 |
| ------------------------ | ----------------- |
| TrainingSampleId         | TS-005            |
| Category                 | Room              |
| RuleId                   | R-102             |
| RuleName                 | RoomNumberMissing |
| Severity                 | High              |
| HumanReviewRequired      | True              |
| CurrentFixPriority       | High              |
| ProposedFixPriorityLabel | High              |

### ラベル理由

部屋番号未入力は、部屋の識別と後続データ連携に影響するため、`High` とする。

### BIM担当者確認が必要な点

```text id="g7y9vo"
部屋番号の採番ルールがあるか
RoomNameとの対応関係が正しいか
部屋番号が不要な運用かどうか
```

### 注意点

RoomNumberはRoomを安定して参照するための重要な識別情報である。

---

## TS-006：Room / AreaMissingOrZero

### 入力情報

| 項目                       | 値                 |
| ------------------------ | ----------------- |
| TrainingSampleId         | TS-006            |
| Category                 | Room              |
| RuleId                   | R-103             |
| RuleName                 | AreaMissingOrZero |
| Severity                 | Medium            |
| HumanReviewRequired      | False             |
| CurrentFixPriority       | Medium            |
| ProposedFixPriorityLabel | Medium            |

### ラベル理由

面積は、面積分析やBI利用に影響するため、`Medium` とする。

### BIM担当者確認が必要な点

```text id="lcgfgl"
面積が0になっている理由
Room境界や計算設定が正しいか
面積が別の列または別の単位で記録されていないか
```

### 注意点

Areaは重要な分析項目だが、部屋名や部屋番号ほど要素識別に直結しない場合があるため、初期MVPでは `Medium` とする。

---

## TS-007：Room / ZoneMissing

### 入力情報

| 項目                       | 値           |
| ------------------------ | ----------- |
| TrainingSampleId         | TS-007      |
| Category                 | Room        |
| RuleId                   | R-105       |
| RuleName                 | ZoneMissing |
| Severity                 | Low         |
| HumanReviewRequired      | True        |
| CurrentFixPriority       | Low         |
| ProposedFixPriorityLabel | Review      |

### ラベル理由

Zone管理の有無はプロジェクト条件によるため、入力情報だけでは優先度を確定できない。
そのため、`Review` とする。

### BIM担当者確認が必要な点

```text id="nzvnls"
このプロジェクトでZone管理を行うか
Zoneが設計上必要な情報か
Zone欠損がAI ContextやRAG検索に影響するか
```

### 注意点

`Review` は低優先度ではない。
人による判断が必要という意味である。

---

## TS-008：Door / LevelNameMissing

### 入力情報

| 項目                       | 値                |
| ------------------------ | ---------------- |
| TrainingSampleId         | TS-008           |
| Category                 | Door             |
| RuleId                   | D-004            |
| RuleName                 | LevelNameMissing |
| Severity                 | Medium           |
| HumanReviewRequired      | True             |
| CurrentFixPriority       | Medium           |
| ProposedFixPriorityLabel | Review           |

### ラベル理由

LevelName不足は影響し得るが、モデル構成や出力条件によって判断が変わるため、`Review` とする。

### BIM担当者確認が必要な点

```text id="ttyqy1"
対象建具がどのレベルに属するべきか
Revitのホストやレベル設定に問題があるか
出力時にLevelNameが取得できなかっただけか
```

### 注意点

LevelNameMissingは、単純に `Medium` として扱える場合もあるが、pyRevit Metadataやモデル構成の確認が必要な場合は `Review` とする。

---

## 全体メモ

このサンプルでは、High / Medium / Low / Review をすべて含めている。

```text id="4zj872"
High：TS-001, TS-004, TS-005
Medium：TS-002, TS-006
Low：TS-003
Review：TS-007, TS-008
```

Door / Roomカテゴリも両方含めている。

```text id="7fmva0"
Door：TS-001, TS-002, TS-003, TS-008
Room：TS-004, TS-005, TS-006, TS-007
```

---

## 制約

このラベル例には以下の制約がある。

```text id="8tptju"
PoC用の小規模サンプルである
モデル学習用データではない
実案件データではない
ラベルは正式な優先度基準ではない
最終判断はBIM担当者が行う
AIが設計判断・施工判断・法規判断を行うものではない
Revitモデル自動修正を前提としない
```

---

## 完了条件

このドキュメントは、以下を満たした時点で完了とする。

```text id="zmgfmv"
サンプルCSVの全行についてラベル理由を説明した
High / Medium / Low / Review の例を含めた
Reviewラベルの意味を明記した
Door / Roomカテゴリの両方を含めた
BIM担当者確認が必要な点を整理した
制約を明記した
```
