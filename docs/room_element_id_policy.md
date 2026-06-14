# Room ElementId Policy

## 目的

このドキュメントは、Phase 3B：Roomカテゴリ追加におけるRoom要素の `ElementId` の扱いを整理するためのメモである。

Phase 3Bでは、Revit Room Schedule TXTを入力としてRoomカテゴリの品質チェック、AI Readiness Score、AI Context、Fix Guide生成を行う。

ただし、現時点のRoom Schedule TXTには、Revit内部ElementIdまたはUniqueIdは含まれていない。

そのため、Phase 3B初期MVPでは、PoC用の仮ElementIdを生成して使用する。

---

## 前提

対象ファイル：

```text
03_input_csv/room_schedule_export_test_v001.txt
```

対象集計表：

```text
05 部屋 仕上表 作業用
```

このTXTには、Roomカテゴリの識別に使えそうな列として、以下が含まれている。

```text
レベル
仕上表 グループ番号*
仕上表 整列番号
仕上表 別名(室名)
名前
面積
```

一方で、以下は含まれていない。

```text
Revit内部ElementId
Revit UniqueId
```

Revit内部ElementId / UniqueIdの取得は、Phase 3C：pyRevitでElementId / UniqueId取得PoCで扱う。

---

## 基本方針

Phase 3B初期MVPでは、Revit内部ElementIdではなく、Room Schedule上で識別可能な情報からPoC用の仮ElementIdを生成する。

仮ElementIdは、品質チェック結果、AI Readiness Score、AI Context、Fix GuideをElement単位で紐づけるために使用する。

この仮ElementIdは、Revit内部ElementIdとは別物であり、実務上の永続IDとしては扱わない。

---

## 仮ElementIdの生成優先順位

仮ElementIdは、以下の優先順位で生成する。

```text
1. Level + "-" + RoomNumber
2. Level + "-" + RoomName
3. Room-連番
```

ここで使用する列は以下とする。

| PoC側の列名    | Revit TXT列 |
| ---------- | ---------- |
| Level      | `レベル`      |
| RoomNumber | `仕上表 整列番号` |
| RoomName   | `名前`       |

---

## 第1候補：Level + RoomNumber

`仕上表 整列番号` が存在する場合は、以下の形式で仮ElementIdを生成する。

```text
Level + "-" + RoomNumber
```

例：

```text
1FL-100
1FL-101
2FL-200
3FL-202
```

理由：

* RoomNumber単体では階をまたいで重複する可能性がある
* Levelを含めることで、階別の識別性が上がる
* 人間が見てもRoomの位置を推測しやすい
* AI ContextやFix Guideで参照しやすい

---

## 第2候補：Level + RoomName

`仕上表 整列番号` が空欄の場合は、RoomNameを使用する。

```text
Level + "-" + RoomName
```

例：

```text
1FL-ピロティ
2FL-設備バルコニー
ピット-消火水槽
```

理由：

* RoomNumberが空欄でも、RoomNameがあればRoomの意味を識別しやすい
* RoomNameはAI ContextやFix Guide上でも説明に使いやすい
* ただし、同一階に同名Roomがある場合は重複する可能性がある

---

## 第3候補：Room-連番

LevelまたはRoomNameが不足しており、上記の方法で仮ElementIdを生成できない場合は、連番を使用する。

```text
Room-001
Room-002
Room-003
```

理由：

* どの行にも一意のIDを付与するため
* 品質チェック結果、AI Readiness Score、AI Context、Fix Guideを行単位で紐づけるため
* 入力データに識別情報が不足している場合のフォールバックとして使う

---

## 重複時の扱い

仮ElementIdが重複する場合は、末尾に連番を付与する。

例：

```text
2FL-設備バルコニー
2FL-設備バルコニー-002
2FL-設備バルコニー-003
```

または、RoomNumberが使える場合はRoomNumberを優先する。

重複が発生した場合は、Room Schedule上の識別情報が不足している可能性があるため、制約として記録する。

---

## グループ見出し行の扱い

Room Schedule TXTには、以下のようなグループ見出し行が含まれる可能性がある。

```text
1階
基準階
共通
```

これらはRoom要素本体ではないため、仮ElementId生成対象から除外する。

除外候補の特徴：

```text
RoomNameが空欄
Areaが空欄
仕上情報が空欄
Level列だけに見出し文字列が入っている
```

---

## 仮ElementIdの用途

Phase 3B初期MVPでは、仮ElementIdを以下に使用する。

* Room用品質チェック結果のElementId
* Room用QualityScoreの集計単位
* Room用AI Readiness Scoreの集計単位
* Room用AI Contextの対象ElementId
* Room用Fix Guideの対象ElementId
* pytestでの期待値確認

---

## 仮ElementIdの制約

仮ElementIdには以下の制約がある。

* Revit内部ElementIdではない
* Revit UniqueIdではない
* Revitモデル内で永続的に保証されるIDではない
* RoomNameやRoomNumberが変更されるとIDも変わる可能性がある
* 同名RoomやRoomNumber空欄が多い場合、重複対応が必要になる
* 実務利用時にはRevit内部ElementIdまたはUniqueIdの取得が望ましい

---

## Phase 3Cとの関係

Phase 3Bでは、Room Schedule TXTのみを入力として扱う。

そのため、Revit内部ElementId / UniqueIdが必要な場合は、Phase 3CでpyRevitまたはRevit APIを使って取得する。

Phase 3Cでは、以下のような情報を取得することを検討する。

```text
ElementId
UniqueId
Category
FamilyName
TypeName
Level
RoomName
RoomNumber
```

Phase 3Bで仮ElementIdを使うことは、Phase 3Cで正式なElementId / UniqueId取得へ進む前のMVP上の暫定対応である。

---

## 初期MVPでの採用方針

Phase 3B初期MVPでは、以下の方針を採用する。

```text
ElementId = Level + "-" + RoomNumber
```

ただし、RoomNumberが空欄の場合は以下を使用する。

```text
ElementId = Level + "-" + RoomName
```

それでも生成できない場合は、連番を使用する。

```text
ElementId = Room-連番
```

この方針により、Revit内部ElementIdがない状態でも、Roomカテゴリの品質チェック、AI Readiness Score、AI Context、Fix GuideをElement単位で接続できるようにする。

---

## Step 3の判断

Phase 3Bでは、Room Schedule TXTにRevit内部ElementIdが含まれていないため、初期MVPではPoC用の仮ElementIdを生成して使用する。

正式なRevit内部ElementId / UniqueIdの取得は、Phase 3Cで扱う。

この方針で、次のStepでは `Category = Room` の付与方針と、Room Schedule TXTのクレンジング方針を整理する。
