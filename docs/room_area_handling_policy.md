# Room Area Handling Policy

## 目的

このドキュメントは、Phase 3B：Roomカテゴリ追加における `Area` の扱いを整理するためのメモである。

Room Schedule TXTでは、Revitの `面積` が単位付き文字列として出力されるため、Python側で数値部分を抽出し、Roomカテゴリ用の品質チェック、AI Readiness Score、AI Context、Fix Guide生成に利用できる形式へ変換する。

---

## 対象ファイル

```text
03_input_csv/room_schedule_export_test_v001.txt
```

対象列：

```text
面積
```

PoC側の列名：

```text
Area
```

---

## 確認できたArea形式

今回のRoom Schedule TXTでは、以下のような形式が確認できた。

```text
16.3281 m²
410.8844 m²
13.1075 m²
173.3000 m²
22.7760 m²
```

このため、初期MVPでは `m²` を含む単位付き文字列から数値部分を抽出する方針とする。

---

## 基本方針

Phase 3B初期MVPでは、`面積` 列を以下のように変換する。

```text
"16.3281 m²"
↓
16.3281
```

変換後の値は、PoC側の `Area` として扱う。

---

## 変換方針

Area変換では、以下を基本方針とする。

| 入力値           |      変換後 | 扱い                  |
| ------------- | -------: | ------------------- |
| `16.3281 m²`  |  16.3281 | 正常                  |
| `410.8844 m²` | 410.8844 | 正常                  |
| `22.7760 m²`  |  22.7760 | 正常                  |
| `0 m²`        |      0.0 | AreaMissingOrZero対象 |
| `0`           |      0.0 | AreaMissingOrZero対象 |
| 空欄            | 空欄またはNaN | AreaMissing対象       |
| 変換不可文字列       | 空欄またはNaN | 制約として記録             |

---

## 初期MVPで対応する形式

初期MVPでは、以下の形式に対応する。

```text
12.34
12.34 m²
12.34㎡
0
0 m²
空欄
```

`m²` と `㎡` の両方を想定する。

---

## 初期MVPで無理に対応しない形式

初期MVPでは、以下のような形式には深入りしない。

```text
約12.34 m²
12,345.67 m²
12.34平方メートル
計 12.34 m²
複数値が混在する文字列
```

これらが出た場合は、変換失敗として扱い、制約または改善点として記録する。

---

## AreaMissingOrZeroの判定

Room用RuleIdでは、以下を想定する。

```text
R-103 AreaMissingOrZero
```

判定方針：

```text
Areaが空欄の場合 → 違反
AreaがNaNの場合 → 違反
Areaが0の場合 → 違反
Areaが0より大きい場合 → 違反なし
Areaを数値変換できない場合 → 違反または変換制約として記録
```

初期MVPでは、数値変換できないAreaは安全側に倒し、HumanReviewRequiredの対象にすることを検討する。

---

## AI Readiness Scoreへの影響

Areaは、BI、面積集計、コスト分析、空間分析、RAG検索時の文脈情報として重要である。

そのため、Areaが空欄または0の場合は、AI Readiness上の阻害要因として扱う。

初期MVPでの想定：

| RuleId | RuleName          | Severity | AIReadinessImpact | AIReadinessPenalty |
| ------ | ----------------- | -------- | ----------------- | -----------------: |
| R-103  | AreaMissingOrZero | Medium   | Medium            |                 10 |

数値はPoC用の仮設定であり、正式なBIM品質基準ではない。

---

## AI Contextでの扱い

AI Contextでは、変換後の数値Areaを出力する。

例：

```text
ElementId: 1FL-100
Category: Room
RoomName: ピロティ
Area: 173.3000
```

元の文字列を残す必要がある場合は、補助列として以下を検討する。

```text
AreaRaw
```

初期MVPでは、以下の2列を持つ構成も候補とする。

```text
AreaRaw
Area
```

例：

| AreaRaw       |     Area |
| ------------- | -------: |
| `173.3000 m²` | 173.3000 |

---

## Fix Guideでの扱い

Areaが未入力または0の場合、Fix Guideでは以下のような説明を想定する。

```text
Roomの面積情報を確認し、Revit Room Schedule上で有効なAreaが取得できる状態にする。
```

注意点：

* LLMやPoC側でAreaを推測補完しない
* 面積はRevitモデル由来の値を優先する
* 不明な場合は人間確認対象とする

---

## 実装時の処理イメージ

Python実装では、以下のような処理を想定する。

```text
1. AreaRawとして元の文字列を保持する
2. 文字列から数値部分を抽出する
3. floatに変換する
4. 変換できない場合はNaNとする
5. AreaがNaNまたは0の場合はAreaMissingOrZero違反とする
```

正規表現では、最初に見つかった数値を抽出する方針とする。

---

## 制約

現時点の制約は以下である。

* Revit Scheduleの面積は単位付き文字列として出力される
* 単位表記は環境やRevit設定に依存する可能性がある
* `m²` と `㎡` の表記ゆれがあり得る
* グループ見出し行ではAreaが空欄になる
* Areaが空欄の行がRoom本体なのか見出し行なのかを判定する必要がある
* AreaをPoC側で推測補完しない
* 正式な面積品質基準ではなく、Phase 3B初期MVP用の判定である

---

## Step 5の判断

Phase 3Bでは、Room Schedule TXTの `面積` 列を `AreaRaw` として保持し、数値部分を抽出した値を `Area` として扱う。

Areaが空欄、NaN、または0の場合は、Room用RuleId `R-103 AreaMissingOrZero` の対象とする。

Areaを数値変換できない場合は、PoCの失敗ではなく、Revit Schedule出力形式に依存する制約として記録する。

この方針により、RoomカテゴリのAI Readiness Assessmentで、面積情報の不足を評価できるようにする。
