# Room Category Policy

## 目的

このドキュメントは、Phase 3B：Roomカテゴリ追加における `Category = Room` の付与方針を整理するためのメモである。

Phase 3Bでは、Revit Room Schedule TXTを入力として、Roomカテゴリ用の品質チェック、AI Readiness Score、AI Context、Fix Guide生成を行う。

その際、Roomデータであることを明示するため、クレンジング後データに `Category = Room` を付与する。

---

## 対象ファイル

入力元ファイル：

```text
03_input_csv/room_schedule_export_test_v001.txt
```

今後作成する予定の変換後CSV：

```text
03_input_csv/room_schedule_converted_v001.csv
```

今後作成する予定のクレンジング後CSV：

```text
03_input_csv/cleaned_room_data_v001.csv
```

`Category = Room` は、原則としてクレンジング後CSVに付与する。

---

## 基本方針

Phase 3B初期MVPでは、Room Schedule TXTには `Category` 列が存在しない。

そのため、Python側のクレンジング処理で、固定値として以下を付与する。

```text
Category = Room
```

この値は、Roomカテゴリの品質チェック、AI Readiness Score、AI Context、Fix Guide生成で共通して使用する。

---

## Categoryを付与する理由

`Category = Room` を付与する理由は以下である。

* DoorデータとRoomデータを区別するため
* Rule Masterの対象カテゴリ列と照合するため
* Room用ルールだけを適用できるようにするため
* AI Readiness Scoreをカテゴリ別に集計できるようにするため
* AI Contextで要素カテゴリを明示するため
* Fix Guideで対象カテゴリを明示するため
* 将来的にWall、Space、Equipmentなど複数カテゴリへ拡張しやすくするため

---

## 付与タイミング

`Category = Room` は、Room Schedule TXTをCSV化し、必要な列名変換と行除外を行った後に付与する。

想定フロー：

```text
room_schedule_export_test_v001.txt
↓
room_schedule_converted_v001.csv
↓
列名正規化
↓
グループ見出し行の除外
↓
Area数値変換
↓
仮ElementId生成
↓
Category = Room を付与
↓
cleaned_room_data_v001.csv
```

初期MVPでは、`cleaned_room_data_v001.csv` に必ず `Category` 列を含める。

---

## 出力イメージ

Room用クレンジング後データでは、以下のような列構成を想定する。

```text
ElementId,Category,Level,RoomNumber,RoomName,Area,FloorFinish,WallFinish,CeilingFinish
```

例：

```text
1FL-100,Room,1FL,100,ピロティ,173.3000,,,
2FL-設備バルコニー,Room,2FL,,設備バルコニー,22.7760,,,
ピット-消火水槽,Room,ピット,,消火水槽,16.3281,,,
```

---

## Rule Masterとの関係

将来的にDoorカテゴリとRoomカテゴリを同じRule Masterで扱う場合、Rule Master側には対象カテゴリを示す列が必要になる。

候補列名：

```text
TargetCategory
Category
ApplicableCategory
Target
```

Phase 3Bでは、Rule Masterに対象カテゴリ列があるか確認する。

対象カテゴリ列が存在しない場合は、Room用ルール追加前に、`TargetCategory` などの列追加を検討する。

Roomデータ側の `Category = Room` と、Rule Master側の `TargetCategory = Room` を照合することで、Room用ルールのみを適用できる構造にする。

---

## 品質チェックでの使用方針

Roomカテゴリの品質チェックでは、以下のような考え方を採用する。

```text
データ側 Category = Room
Rule Master側 TargetCategory = Room
↓
Room用RuleIdのみ適用
```

これにより、Door用ルールがRoomデータに誤って適用されることを防ぐ。

例：

```text
Door用のFamilyName命名規則違反をRoomに適用しない
Room用のRoomNameMissingをDoorに適用しない
```

---

## AI Readiness Scoreでの使用方針

AI Readiness Scoreでは、`Category` を以下の用途で使用する。

* Roomカテゴリ単位でスコアを確認する
* DoorカテゴリとRoomカテゴリを分けて集計する
* BlockingRuleIdsの対象カテゴリを明確にする
* 将来的なカテゴリ別AI Readiness評価につなげる

---

## AI Contextでの使用方針

AI Contextでは、`Category` を必須情報として扱う。

Roomカテゴリでは、以下のように出力することを想定する。

```text
ElementId: 1FL-100
Category: Room
RoomName: ピロティ
Level: 1FL
AIReadinessScore: 70
HumanReviewRequired: True
```

これにより、Local LLMや将来的なRAGに渡す際に、対象がDoorなのかRoomなのかを明確にできる。

---

## Fix Guideでの使用方針

Fix Guideでは、`Category` を対象要素の説明に含める。

例：

```text
ElementId: 1FL-100
Category: Room
RuleId: R-101
FixGuide: RoomNameを入力する
```

これにより、BIM担当者が修正対象カテゴリを判断しやすくなる。

---

## 表記ゆれの扱い

初期MVPでは、Roomカテゴリの値は以下に統一する。

```text
Room
```

以下の表記は使用しない。

```text
Rooms
部屋
room
ROOM
```

理由：

* Rule Masterの `TargetCategory` と一致させるため
* 出力CSV、AI Context、Fix Guideで表記を統一するため
* 後続処理でカテゴリ照合しやすくするため

ただし、READMEやdocs上の説明文では、日本語として「Roomカテゴリ」「部屋」と表記してもよい。

---

## 制約

現時点の制約は以下である。

* Revit Room Schedule TXTには `Category` 列が存在しない
* `Category = Room` はPython側で付与する
* Rule Masterに対象カテゴリ列が存在しない場合は、別途拡張が必要になる
* Door用既存処理がCategory列を前提としていない可能性がある
* 初期MVPでは、既存Door処理を壊さないようにRoom専用処理側でCategoryを扱う

---

## Step 4の判断

Phase 3Bでは、Room用クレンジング後データに `Category = Room` を付与する。

`Category = Room` は、Room用品質チェック、AI Readiness Score、AI Context、Fix Guide生成で共通して使用する。

また、将来的にRule Master側の `TargetCategory` と照合し、Door用ルールとRoom用ルールを分けて適用できる構造にする。

この方針により、既存Door処理を壊さず、Roomカテゴリを追加するための前提を整理できた。
