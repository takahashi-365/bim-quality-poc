# Room Rule Specification

## 目的

第3段階B：Roomカテゴリ追加では、Roomデータに対してRuleIdベースの品質チェックを行う。

本ドキュメントでは、初期MVPで使用するRoom用RuleId、判定対象、Severity、AI活用上の影響、初期MVPでの扱いを整理する。

## 前提

Roomカテゴリ用データには、クレンジング後に以下を付与する。

```text
Category = Room
```

Rule Master側では、対象カテゴリを示す列として以下を使用する。

```text
TargetCategory = Room
```

品質チェック処理では、入力データの `Category` とRule Masterの `TargetCategory` を照合し、RoomデータにはRoom用ルールのみを適用する。

## 初期MVPで対象とするRoom用RuleId

| RuleId | RuleName          | TargetCategory | Category               | Severity | TargetField | 内容                        | 初期MVPでの扱い |
| ------ | ----------------- | -------------- | ---------------------- | -------- | ----------- | ------------------------- | --------- |
| R-101  | RoomNameMissing   | Room           | Parameter Completeness | High     | RoomName    | RoomNameが空欄の場合に違反とする      | 対象        |
| R-102  | RoomNumberMissing | Room           | Parameter Completeness | High     | RoomNumber  | RoomNumberが空欄の場合に違反とする    | 対象        |
| R-103  | AreaMissingOrZero | Room           | Parameter Completeness | Medium   | Area        | Areaが空欄、NaN、または0の場合に違反とする | 対象        |
| R-104  | LevelMissing      | Room           | Parameter Completeness | Medium   | Level       | Levelが空欄の場合に違反とする         | 対象        |

## 初期MVPでは制約・将来拡張扱いとするRuleId

| RuleId | RuleName                  | TargetCategory | Category               | Severity | TargetField        | 内容                             | 初期MVPでの扱い         |
| ------ | ------------------------- | -------------- | ---------------------- | -------- | ------------------ | ------------------------------ | ----------------- |
| R-105  | ZoneMissing               | Room           | Parameter Completeness | Low      | Zone               | Zoneが空欄の場合に違反とする               | Zone列が取得できる場合のみ対象 |
| R-106  | ClassificationCodeMissing | Room           | Classification         | High     | ClassificationCode | ClassificationCodeが空欄の場合に違反とする | 初期MVPでは制約扱い       |

## R-101 RoomNameMissing

RoomNameが空欄の場合に違反とする。

RoomNameは空間の意味を把握するための基本情報である。RoomNameが不足している場合、BI、検索、AI Context、RAGで空間の意味を判断しにくくなる。

## R-102 RoomNumberMissing

RoomNumberが空欄の場合に違反とする。

RoomNumberは部屋を参照・検索・識別するための基本情報である。RoomNumberが不足している場合、部屋単位の集計や確認が不安定になる。

## R-103 AreaMissingOrZero

Areaが空欄、NaN、または0の場合に違反とする。

Areaは面積分析、BI、コスト分析、空間規模の把握に使う基本情報である。Areaが不足している場合、空間情報を分析やAI活用に使いにくくなる。

Room Schedule TXTでは、面積が以下のような単位付き文字列として出力される場合がある。

```text
12.34
12.34 m²
12.34㎡
0
0 m²
空欄
```

初期MVPでは、数値部分を抽出してAreaとして扱う。

## R-104 LevelMissing

Levelが空欄の場合に違反とする。

Levelは階別集計、空間把握、検索条件、AI Contextの文脈情報として重要である。Levelが不足している場合、部屋がどの階に属するか判断しにくくなる。

## R-105 ZoneMissingの扱い

Zone列は現時点のRoom Schedule TXTでは確認できていない。

そのため、R-105 `ZoneMissing` はRuleId案としては保持するが、初期MVPでは無理に適用しない。

Zone列がない状態でZoneMissingを強制適用すると、全RoomがLow違反となる可能性があるため、初期MVPでは制約・将来拡張扱いとする。

## R-106 ClassificationCodeMissingの扱い

ClassificationCode列は現時点のRoom Schedule TXTでは確認できていない。

そのため、R-106 `ClassificationCodeMissing` はRoomカテゴリの重要ルール候補ではあるが、初期MVPでは制約扱いとする。

ClassificationCode列が取得できるようになった段階で、Room用品質チェック対象に追加する。

## Rule Master追加方針

Room用RuleIdは、既存のRule Masterに追加する。

対象ファイル：

```text
02_rule_master/bim_rule_master_v003.csv
```

既存DoorルールとRoomルールを同じRule Masterで扱うため、以下の列で対象カテゴリを分ける。

```text
TargetCategory
```

Room用ルールでは以下を設定する。

```text
TargetCategory = Room
```

## 初期MVPでRule Masterに追加するルール

初期MVPでは、まず以下の4ルールをRule Masterに追加する。

```text
R-101 RoomNameMissing
R-102 RoomNumberMissing
R-103 AreaMissingOrZero
R-104 LevelMissing
```

R-105とR-106は、Room Scheduleの列取得状況に依存するため、初期MVPではRule Masterへの追加を急がない。

## 注意点

* Room情報を推測で補完しない
* Revitモデルの自動修正は行わない
* Room用ルールは初期MVPでは増やしすぎない
* Zone列がない場合、R-105を無理に適用しない
* ClassificationCode列がない場合、R-106を無理に適用しない
* 既存Door用ルールの意味を変更しない
* 既存Door用pytestが通る状態を維持する

## 次の作業

次の作業では、`02_rule_master/bim_rule_master_v003.csv` にRoom用RuleIdを追加する。

追加対象：

```text
R-101
R-102
R-103
R-104
```
