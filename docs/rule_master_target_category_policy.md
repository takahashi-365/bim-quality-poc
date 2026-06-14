# Rule Master TargetCategory Policy

## 目的

第3段階B：Roomカテゴリ追加では、既存のDoorカテゴリに加えてRoomカテゴリの品質チェックを行う。

Door用ルールとRoom用ルールを同じRule Masterで管理するため、Rule Masterに対象カテゴリを示す列として `TargetCategory` を追加する。

## 確認結果

`02_rule_master/bim_rule_master_v003.csv` の既存列には、対象カテゴリを示す専用列は存在しなかった。

既存の `Category` 列は、以下のようなルール分類として使用されている。

```text
Parameter Completeness
Classification
Naming Rule
```

そのため、`Category` 列を `Door` / `Room` の対象カテゴリ判定には使用しない。

## 採用方針

Rule Masterに `TargetCategory` 列を追加する。

既存Door用ルールには以下を設定する。

```text
TargetCategory = Door
```

Room用ルールを追加する場合は以下を設定する。

```text
TargetCategory = Room
```

## 想定構成

```text
RuleId,RuleName,TargetCategory,Category,Severity,TargetField,...
R-001,必須パラメータ未入力,Door,Parameter Completeness,High,RequiredFields,...
R-002,分類コード未入力,Door,Classification,High,BIM_ClassificationCode,...
R-003,ファミリ命名規則違反,Door,Naming Rule,Medium,FamilyName,...
R-101,RoomNameMissing,Room,Parameter Completeness,High,RoomName,...
R-102,RoomNumberMissing,Room,Parameter Completeness,High,RoomNumber,...
R-103,AreaMissingOrZero,Room,Parameter Completeness,Medium,Area,...
R-104,LevelMissing,Room,Parameter Completeness,Medium,Level,...
```

## 判断理由

`TargetCategory` を追加することで、RoomデータにRoom用ルールだけを適用できる。

また、既存の `Category` 列をルール分類として残すことで、既存Doorルールの意味を壊さずにRoomカテゴリを追加できる。

## 注意点

* 既存の `Category` 列は削除しない
* 既存の `Category` 列の意味を変更しない
* Door用既存ルールには `TargetCategory = Door` を設定する
* Room用新規ルールには `TargetCategory = Room` を設定する
* 品質チェック処理では、入力データの `Category` とRule Masterの `TargetCategory` を照合する

## 今後の対応

次のStepでは、Room用RuleIdを整理し、必要に応じて `02_rule_master/bim_rule_master_v003.csv` にRoom用ルールを追加する。
