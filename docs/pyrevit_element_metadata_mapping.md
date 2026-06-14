# pyRevit Element Metadata Mapping

## 目的

このドキュメントは、第3段階C「pyRevitでElementId / UniqueId取得PoC」で出力したCSVと、既存の `BIM Data Quality & AI Readiness Assessment PoC` の入力データ・AI Context・将来のRAG用メタデータとの接続方針を整理する。

第3段階Cでは、pyRevitを用いてRevit上の選択要素から基本メタデータを取得し、CSVとして出力した。

---

## pyRevit出力CSV

今回の出力CSVは以下である。

```text
03_input_csv/pyrevit_element_metadata_sample_v001.csv
```

初期MVPの列構成は以下である。

```text
ElementId
UniqueId
Category
FamilyName
TypeName
Name
LevelName
RoomName
RoomNumber
```

サンプル出力例は以下である。

```text
ElementId,UniqueId,Category,FamilyName,TypeName,Name,LevelName,RoomName,RoomNumber
100001,00000000-0000-0000-0000-000000000001-00000001,ドア,Sample Door Family,Sample Door Type 900x2100,Sample Door Type 900x2100,1FL,,
```

---

## 既存PoCとの関係

既存PoCでは、Revit集計表TXTをPythonへ渡して処理している。

既存の基本フローは以下である。

```text
Revit Schedule TXT
↓
CSV変換
↓
データクレンジング
↓
RuleIdベース品質チェック
↓
QualityScore
↓
AI Readiness Score
↓
AI Context
↓
Fix Guide
```

第3段階Cでは、この前段にpyRevit取得データを追加する入口を作る。

```text
Revitモデル上で要素選択
↓
pyRevitでメタデータ取得
↓
CSV出力
↓
既存PoCの入力CSVとの接続可能性を確認
```

初期MVPでは、既存Door / Roomパイプラインへ直接接続せず、接続可能性の整理に留める。

---

## ElementId列の違い

既存PoCでは、`ElementId` 列が必ずしもRevit内部ElementIdを意味していない。

Doorでは、建具表上の建具番号や既存入力データ上の識別子をPoC用のIDとして扱っている。

Roomでは、Room Schedule TXTにRevit内部ElementId / UniqueIdが含まれていないため、Phase 3BでPoC用の仮ElementIdを生成した。

Roomの仮ElementId方針は以下である。

```text
Level + "-" + RoomNumber + "-" + 連番
RoomNumberが空欄の場合: Level + "-" + RoomName + "-" + 連番
それも無理な場合: Room-連番
```

一方、pyRevit出力CSVの `ElementId` は、Revit APIから取得したRevit内部ElementIdである。

そのため、既存PoCの `ElementId` とpyRevit出力CSVの `ElementId` は、同じ名前でも意味が異なる可能性がある。

---

## ElementId / UniqueId の整理方針

今後は、以下のように区別する。

```text
ElementId
  Revit内部ElementId、または既存PoC上の識別子として使われてきた列名

RevitElementId
  pyRevit / Revit APIから取得したRevit内部ElementIdを明示する場合の候補列名

UniqueId
  Revit APIから取得したUniqueId。将来的な安定識別子候補
```

既存PoCの互換性を保つため、すぐに既存の `ElementId` 列名を変更しない。

ただし、AI ContextやRAG用メタデータでは、以下のように併記することを検討する。

```text
ElementId
RevitElementId
UniqueId
SourceIdType
```

`SourceIdType` の候補は以下である。

```text
RevitElementId
RevitUniqueId
ScheduleDerivedId
TemporaryPoCId
```

---

## pyRevit出力CSVと既存PoC列の対応

| pyRevit出力列 | 既存PoCでの扱い                     | 接続方針                                    |
| ---------- | ----------------------------- | --------------------------------------- |
| ElementId  | 既存PoCのElementIdと名前が重なる        | Revit内部ElementIdとして意味を明確化する             |
| UniqueId   | 既存PoCでは未使用                    | 将来の安定識別子候補としてAI Context / RAGメタデータへ追加検討 |
| Category   | Category / TargetCategory と関連 | `ドア` を Door と対応付ける変換が必要                 |
| FamilyName | 既存品質チェックでは必須ではない              | AI Contextの補助メタデータ候補                    |
| TypeName   | TypeName / TypeMark等と関連する可能性  | Door品質チェックやAI Context補助情報として利用候補        |
| Name       | Revit要素名またはタイプ名相当             | そのまま品質判定に使う前に意味確認が必要                    |
| LevelName  | RoomのLevelやDoorの階情報に関連        | 階別分析・RAGメタデータ候補                         |
| RoomName   | Roomカテゴリのみ取得候補                | Doorでは空欄。DoorからのRoom推定は初期MVP対象外         |
| RoomNumber | Roomカテゴリのみ取得候補                | Doorでは空欄。初期MVPでは必須にしない                  |

---

## Categoryの対応方針

pyRevit出力では、Revitのカテゴリ名が日本語で出力される場合がある。

今回のDoor検証では以下のように出力された。

```text
Category = ドア
```

既存PoCのカテゴリ表記は以下である。

```text
Door
Room
```

そのため、接続時にはカテゴリ名の正規化が必要である。

例：

```text
ドア → Door
Doors → Door
Room → Room
Rooms → Room
部屋 → Room
```

この正規化は、pyRevitスクリプト側で行う方法と、PoC側のPython処理で行う方法がある。

初期MVPでは、pyRevit側ではRevitから取得した値をそのまま出力し、PoC側で正規化する方針が安全である。

理由は以下である。

```text
Revitから取得した生データを保持できる
変換ロジックをPoC側でテストしやすい
pyRevit側を最小限の取得処理に保てる
```

---

## Doorカテゴリとの接続方針

Doorでは、今回の検証で以下を取得できた。

```text
ElementId
UniqueId
Category = ドア
FamilyName
TypeName
Name
LevelName
```

既存Doorパイプラインへの直接接続には、既存のDoor入力CSVで必要な列との対応確認が必要である。

ただし、今回のPhase 3C MVPでは、既存Door品質チェックへ直接流し込むことは目的にしない。

まずは、pyRevitから取得した内部IDを既存Doorデータへ付加できる可能性を整理する。

接続候補は以下である。

```text
既存Doorデータ
+ RevitElementId
+ UniqueId
+ FamilyName
+ TypeName
+ LevelName
```

これにより、将来的にAI Contextへ以下のような情報を追加できる。

```text
RevitElementId
UniqueId
RevitCategory
FamilyName
TypeName
LevelName
```

---

## Roomカテゴリとの接続方針

Phase 3Bでは、Room Schedule TXTにRevit内部ElementId / UniqueIdが含まれていなかったため、仮ElementIdを生成した。

第3段階Cでは、pyRevitでRoom要素を選択できれば、RoomのRevit内部ElementId / UniqueIdを取得できる可能性がある。

ただし、Roomカテゴリでは以下の制約がある。

```text
FamilyNameが空欄になる可能性がある
TypeNameが取得できない可能性がある
RoomName / RoomNumberはRoom要素の場合のみ取得候補
Room Schedule由来の仮ElementIdとの照合方法が必要
```

Roomとの接続候補は以下である。

```text
RoomName
RoomNumber
LevelName
RevitElementId
UniqueId
```

ただし、RoomName / RoomNumber / LevelName が一致しても、必ず同一Roomと断定できるとは限らない。

初期MVPでは、Roomとの自動照合は行わず、接続候補として整理する。

---

## AI Contextへの追加候補

将来的にAI Contextへ追加するメタデータ候補は以下である。

```text
RevitElementId
UniqueId
RevitCategory
FamilyName
TypeName
LevelName
SourceIdType
```

これにより、AI Contextの説明力が高まる可能性がある。

例：

```text
この品質チェック結果は、Revit内部ElementId 100001、UniqueId 00000000-0000-0000-0000-000000000001-00000001 の要素に紐づく。
```

ただし、AI ContextにRevit内部IDを含める場合は、公開用サンプルとして問題ないかを確認する必要がある。

実案件モデル由来の情報をそのまま公開しないこと。

---

## RAG / Azure AI Searchへの追加候補

将来的なRAG / Azure AI Search構成では、以下のメタデータとして利用できる可能性がある。

```text
element_id
revit_element_id
unique_id
category
family_name
type_name
level_name
room_name
room_number
source_file
source_id_type
```

特に `UniqueId` は、将来的な検索・照合用メタデータとして有力である。

一方、`ElementId` はモデル内識別には有用だが、長期的な安定識別子としては注意が必要である。

---

## 初期MVPでやらないこと

今回の初期MVPでは、以下は行わない。

```text
既存Door品質チェックへの直接投入
既存Room品質チェックへの直接投入
Room Schedule由来データとの自動照合
Doorから関連Roomを推定する処理
全モデルスキャン
全カテゴリ対応
Revitモデル自動修正
パラメータ自動書き換え
```

---

## 今回の接続判断

今回のPhase 3C MVPでは、以下の判断とする。

```text
pyRevitでRevit内部ElementId / UniqueIdを取得できた
DoorカテゴリではCategory / FamilyName / TypeName / LevelNameを取得できた
DoorではRoomName / RoomNumberを空欄にする方針が妥当
CSVはUTF-8 with BOMで出力し、日本語項目を確認できた
既存PoCへ直接接続する前に、ID列の意味を整理する必要がある
既存PoCのElementIdとRevit内部ElementIdは区別して扱うべき
UniqueIdは将来の安定識別子候補として有用
```

---

## 次の作業候補

次の作業候補は以下である。

```text
Room要素を選択した場合の出力確認
pyRevit出力CSVを読み込むpytestの追加
必要列存在チェックの追加
ElementId / UniqueId が空でないことのチェック
Category正規化方針の実装検討
AI ContextへRevitElementId / UniqueIdを追加する方針検討
```
