# Room Schedule Column Mapping

## 目的

このドキュメントは、Phase 3B：Roomカテゴリ追加で使用するRevit Room Schedule TXTの列構成を確認し、PoC側で使用する列名との対応を整理するためのメモである。

対象ファイル：

```text
03_input_csv/room_schedule_export_test_v001.txt
```

このTXTは、Revitモデル内の以下の集計表を書き出したものである。

```text
05 部屋 仕上表 作業用
```

Phase 3Bでは、このRoom Schedule TXTをもとに、Roomカテゴリ用の品質チェック、AI Readiness Score、AI Context、Fix Guide生成へ接続する。

---

## 元データの概要

Room Schedule TXTには、Roomカテゴリの検証に使える以下の情報が含まれている。

* レベル
* 仕上表 グループ名
* 仕上表 グループ番号
* 仕上表 整列番号
* 仕上表 別名(室名)
* 名前
* 面積
* 排煙
* 排煙告示
* 施工令
* 内装制限
* SL
* FL
* CH
* 床 下地 / 床 仕上
* 幅木
* 腰壁
* 壁 下地 / 壁 仕上
* 廻り縁
* 天井 下地 / 天井 仕上
* 備考

---

## 列マッピング案

初期MVPでは、以下の対応でPoC側の列名へ変換する。

| PoC側の列名               | Revit TXT列    | 使用方針                     |
| --------------------- | ------------- | ------------------------ |
| `Category`            | なし            | Python側で固定値 `Room` を付与する |
| `Level`               | `レベル`         | 使用する                     |
| `RoomName`            | `名前`          | 使用する                     |
| `RoomAlias`           | `仕上表 別名(室名)`  | 取得できる場合に使用する             |
| `RoomGroupName`       | `仕上表 グループ名`   | 補助情報として使用する              |
| `RoomGroupNumber`     | `仕上表 グループ番号*` | 補助情報として使用する              |
| `RoomNumber`          | `仕上表 整列番号`    | RoomNumber相当として使用する候補    |
| `Area`                | `面積`          | 数値部分を抽出して使用する            |
| `SmokeControl`        | `排煙`          | 初期MVPでは補助情報              |
| `SmokeControlNotice`  | `排煙告示`        | 初期MVPでは補助情報              |
| `BuildingCode`        | `施工令`         | 初期MVPでは補助情報              |
| `InteriorRestriction` | `内装制限`        | 初期MVPでは補助情報              |
| `SL`                  | `SL`          | 補助情報として使用する              |
| `FL`                  | `FL`          | 補助情報として使用する              |
| `CH`                  | `CH`          | 補助情報として使用する              |
| `FloorBase`           | `床 下地`        | 仕上情報として使用する              |
| `FloorFinish`         | `床 仕上`        | 仕上情報として使用する              |
| `BaseboardHeight`     | `幅木 H`        | 初期MVPでは補助情報              |
| `BaseboardMaterial`   | `幅木 材料`       | 初期MVPでは補助情報              |
| `WainscotBase`        | `腰壁 下地`       | 初期MVPでは補助情報              |
| `WainscotFinish`      | `腰壁 仕上`       | 初期MVPでは補助情報              |
| `WallBase`            | `壁 下地`        | 仕上情報として使用する              |
| `WallFinish`          | `壁 仕上`        | 仕上情報として使用する              |
| `CeilingBase`         | `天井 下地`       | 仕上情報として使用する              |
| `CeilingFinish`       | `天井 仕上`       | 仕上情報として使用する              |
| `Notes`               | `備考`          | 補助情報として使用する              |

---

## 初期MVPで優先する列

Phase 3Bの初期MVPでは、まず以下の列を優先して扱う。

```text
Category
ElementId
Level
RoomName
RoomNumber
Area
FloorFinish
WallFinish
CeilingFinish
```

`Category` はRevit TXTには存在しないため、Python側で固定値として付与する。

```text
Category = Room
```

`ElementId` はRevit内部ElementIdではなく、初期MVPではPoC用の仮IDとして生成する。

---

## ElementIdの扱い

Room Schedule TXTには、Revit内部ElementIdは含まれていない。

そのため、Phase 3Bの初期MVPでは、PoC上の仮ElementIdを生成する。

候補：

```text
Level + "-" + RoomNumber
```

例：

```text
1FL-100
1FL-101
2FL-200
```

ただし、`仕上表 整列番号` が空欄の行もあるため、次の優先順位で仮ElementIdを生成する。

```text
1. Level + "-" + RoomNumber
2. Level + "-" + RoomName
3. Room-連番
```

Revit内部ElementId / UniqueIdの取得は、Phase 3C：pyRevitでElementId / UniqueId取得PoCで扱う。

---

## Areaの扱い

Room Schedule TXTの `面積` は、以下のような単位付き文字列として出力されている。

```text
16.3281 m²
410.8844 m²
22.7760 m²
```

Phase 3Bでは、Python側で数値部分を抽出して `Area` として扱う。

例：

```text
16.3281 m²
↓
16.3281
```

初期MVPでの判定方針：

```text
Areaが空欄の場合は未入力として扱う
Areaが0の場合はAreaMissingOrZeroとして扱う
Areaが数値として抽出できる場合は数値化して判定する
Areaを数値変換できない場合は、制約として記録する
```

---

## グループ見出し行の扱い

TXTには、Roomデータ本体ではなく、グループ見出しと思われる行が含まれている。

例：

```text
1階
基準階
共通
```

これらはRoom要素そのものではないため、クレンジング時に除外する。

除外候補の特徴：

```text
RoomNameが空欄
Areaが空欄
仕上情報が空欄
Level列だけに見出し文字列が入っている
```

---

## ヘッダー行の扱い

Revit書き出し設定で、列見出しとグループ化された列見出しを含めている。

そのため、TXTの先頭には以下が含まれる。

```text
1行目：主な列名
2行目：サブ列名
3行目以降：データ行
```

Python変換時には、基本的に1行目を主ヘッダーとして使用し、2行目は床・壁・天井などの下地/仕上の補助ヘッダーとして扱う。

必要に応じて、以下のような列名へ正規化する。

```text
床 + 下地 → FloorBase
床 + 仕上 → FloorFinish
壁 + 下地 → WallBase
壁 + 仕上 → WallFinish
天井 + 下地 → CeilingBase
天井 + 仕上 → CeilingFinish
```

---

## ClassificationCodeの扱い

現在のRoom Schedule TXTには、明確な `ClassificationCode` 相当の列は確認できていない。

そのため、初期MVPでは以下の扱いとする。

```text
ClassificationCode列が取得できない場合は、Roomカテゴリ初期MVPの制約として記録する。
```

ただし、将来的にはRoom分類コードを追加し、以下の品質チェックに接続する可能性がある。

```text
R-106 ClassificationCodeMissing
```

---

## Zoneの扱い

現在のRoom Schedule TXTには、明確な `Zone` 相当の列は確認できていない。

そのため、初期MVPでは `ZoneMissing` を無理に適用しない。

```text
R-105 ZoneMissing は、Zone列が取得できる場合のみチェック対象とする。
```

Zone列がない状態で全件違反にすると、Roomカテゴリ追加の初期MVPとして過剰判定になる可能性があるため、今回は制約として扱う。

---

## 初期MVPでのRoom用ルールとの関係

この列マッピングをもとに、初期MVPでは以下のRoom用ルールを優先する。

| RuleId | RuleName                  | 対象列                  | 初期MVPでの扱い           |
| ------ | ------------------------- | -------------------- | ------------------- |
| R-101  | RoomNameMissing           | `RoomName`           | 対象                  |
| R-102  | RoomNumberMissing         | `RoomNumber`         | 対象                  |
| R-103  | AreaMissingOrZero         | `Area`               | 対象                  |
| R-104  | LevelMissing              | `Level`              | 対象                  |
| R-105  | ZoneMissing               | `Zone`               | Zone列がある場合のみ対象      |
| R-106  | ClassificationCodeMissing | `ClassificationCode` | 初期MVPでは制約扱い、列追加時に対象 |

---

## 制約

現時点の制約は以下。

* Revit内部ElementIdはRoom Schedule TXTに含まれていない
* `ElementId` は初期MVPでは仮IDとして生成する
* `Area` は単位付き文字列で出力されるため、Python側で数値抽出が必要
* `ClassificationCode` 相当の列は現時点では確認できていない
* `Zone` 相当の列は現時点では確認できていない
* グループ見出し行が含まれるため、データ行と見出し行を分ける必要がある
* 床・壁・天井などの仕上列は、グループ化されたヘッダーを正規化する必要がある
* Room Scheduleは仕上表由来であり、純粋なRoom一覧表ではない

---

## Step 2の判断

Phase 3Bでは、以下の方針でRoom Schedule TXTを使用する。

```text
採用TXT:
03_input_csv/room_schedule_export_test_v001.txt

採用元集計表:
05 部屋 仕上表 作業用

初期MVPで優先する列:
Level
RoomName
RoomNumber
Area
FloorFinish
WallFinish
CeilingFinish

Python側で付与する列:
Category = Room
ElementId = 仮ID

初期MVPで制約扱いする列:
ClassificationCode
Zone
Revit内部ElementId
```

この方針で、次のStepではRoom Schedule TXTをCSVへ変換し、Roomカテゴリ用のクレンジング処理へ進む。
