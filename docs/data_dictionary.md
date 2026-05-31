# Data Dictionary

## BIM Data Quality Engineering & AI Analysis PoC

## この資料の目的

この資料は、Revit由来CSV、品質チェック用CSV、チェック結果CSVで使用する主な列の意味、現時点の扱い、注意点を整理するためのデータ辞書です。

現時点では、Revit由来データ対応は初期試作段階であり、一部の列は正式なRevit内部情報ではなく、建具表上の列をPoC用に仮対応させています。

この資料では、現時点の仮マッピングを明記し、今後の正式な列マッピング、データクレンジング、品質チェック、特徴量設計へつなげることを目的とします。

---

## 1. 品質チェック用CSVの主な列

| 列名 | 意味 | 現時点の扱い | 注意点 | 今後の対応 |
|---|---|---|---|---|
| Category | BIM要素カテゴリ | 現時点では `Doors` を固定値として付与 | ドア集計表のみを対象にした初期試作 | 将来的には Walls、Rooms などにも対応 |
| ElementId | BIM要素を識別するID | 現時点ではRevit内部ElementIdではなく、建具表上の建具番号を仮IDとして使用 | `101`、`102` などの建具番号であり、Revit内部IDではない | Revit内部ElementIdを出力できるか検討。難しい場合は `ElementKey` や `DoorNumber` への名称変更を検討 |
| FamilyName | Revitファミリ名 | 現時点ではRevitファミリ名ではなく、建具表上の種別記号 `SD` を仮格納 | 正式なFamilyNameではないため、命名規則チェック結果は参考扱い | Revitファミリ名を出力できる集計表設定を検討 |
| TypeName | Revitタイプ名 | 現時点ではRevitタイプ名ではなく、設置場所・室名に近い列を仮格納 | `管理用出入口`、`PS`、`電気室 1F` などが入る | `LocationName` または `RoomName` として扱うか、別列をTypeName候補として検討 |
| Level | 階情報 | 現時点では空欄 | ドア集計表TXTからは階情報を取得していない | Revit集計表側で階情報を追加するか検討 |
| BIM_ClassificationCode | 分類コード | 現時点では空欄 | 未入力チェック対象として使用 | 将来的に分類コードを持つ列を追加 |
| BIM_ModelRole | モデル上の役割 | 現時点では空欄 | 未入力チェック対象として使用 | Revit側またはCSV側で値を追加するか検討 |
| BIM_Zone | ゾーン情報 | 現時点では空欄 | 未入力チェック対象として使用 | Revit側またはCSV側で値を追加するか検討 |
| SourceFile | 元データファイル名 | 入力TXTファイル名を付与 | 変換元ファイルを追跡するために使用 | 継続使用 |
| ModelName | モデル名 | 固定値としてサンプルモデル名を付与 | 現時点では固定文字列 | 将来的には設定値化を検討 |

---

## 2. 元TXT列との対応

| 変換後CSVの列 | 元TXT列番号 | 元TXTの値の例 | 推定される意味 | 現時点の判定 |
|---|---:|---|---|---|
| Category | 固定値 | Doors | カテゴリ | 問題なし |
| ElementId | 1 | 101, 102, 201 | 建具番号・建具符号 | Revit内部ElementIdではない |
| FamilyName | 0 | SD | 建具種別・建具表種別 | Revitファミリ名ではない |
| TypeName | 3 | 管理用出入口, PS, 電気室 1F | 設置場所・室名・用途名称 | Revitタイプ名ではない |
| Level | なし | 空欄 | 階情報 | 未対応 |
| BIM_ClassificationCode | なし | 空欄 | 分類コード | 未対応 |
| BIM_ModelRole | なし | 空欄 | モデル上の役割 | 未対応 |
| BIM_Zone | なし | 空欄 | ゾーン情報 | 未対応 |
| SourceFile | 入力ファイル名 | door_schedule_SD_export_test_v001.txt | 元ファイル名 | 問題なし |
| ModelName | 固定値 | BIM_Quality_Check_Sample_Model_R2024_v001 | モデル名 | 問題なし |

---

## 3. チェック結果CSVの主な列

| 列名 | 意味 | 現時点の扱い |
|---|---|---|
| CheckId | チェック結果のID | 違反ごとに付与 |
| ElementId | チェック対象要素のID | 現時点では建具番号を仮IDとして使用 |
| Category | カテゴリ | 現時点では Doors |
| FamilyName | ファミリ名相当 | 現時点では建具種別記号 |
| TypeName | タイプ名相当 | 現時点では設置場所・室名に近い値 |
| Level | 階情報 | 現時点では空欄 |
| ParameterName | 違反対象パラメータ | `BIM_ClassificationCode`、`BIM_ModelRole`、`BIM_Zone`、`FamilyName` など |
| CurrentValue | 現在値 | 空欄または命名規則違反の対象値 |
| RuleId | 適用されたルールID | `R-001`、`R-002`、`R-003` |
| RuleName | ルール名 | ルールマスタから取得 |
| Severity | 重大度 | ルールマスタから取得 |
| Status | チェック結果 | 現時点では主に `NG` |
| FixGuide | 修正ガイド | ルールマスタから取得 |
| DetectedAt | 検出日時 | チェック実行時に付与 |
| SourceFile | 元ファイル名 | 変換元TXT名 |
| ModelName | モデル名 | サンプルモデル名 |

---

## 4. 現時点の注意点

- `ElementId` は、現時点ではRevit内部ElementIdではなく、建具表上の建具番号を仮IDとして使用している。
- `FamilyName` は、現時点ではRevitファミリ名ではなく、建具表上の種別記号 `SD` を仮格納している。
- `TypeName` は、現時点ではRevitタイプ名ではなく、設置場所・室名に近い列を仮格納している。
- `Level` は現時点では空欄である。
- `BIM_ClassificationCode`、`BIM_ModelRole`、`BIM_Zone` は現時点では空欄であり、未入力チェック対象として使用している。
- `check_results_revit_v001.csv` の104件の違反は、正確な品質評価ではなく、処理フロー確認のための結果である。
- 104件の内訳は、26行に対して、`BIM_ModelRole`、`BIM_Zone`、`BIM_ClassificationCode`、`FamilyName` の4種類の違反が出ているためである。
- 元TXTの先頭行は実データではない可能性があるため、今後は `ElementId` が空欄の行を除外することを検討する。

---

## 5. 今後の対応

- Revit集計表側で正式なRevit内部ElementIdを出力できるか確認する。
- Revitファミリ名、タイプ名を取得できる列を追加できるか確認する。
- `raw_df[4]` の値をTypeName候補として確認する。
- `raw_df[3]` は `LocationName` または `RoomName` として扱うか検討する。
- `ElementId` という列名が不正確な場合は、`ElementKey`、`DoorNumber`、`ScheduleMark` などへの名称変更を検討する。
- 先頭の非データ行を除外する。
- 列マッピング確定後、`convert_revit_schedule.py` をv0.2化する。

---

## 6. まとめ

現時点の `door_schedule_converted_v001.csv` は、Revit由来TXTをPython処理へ接続するための初期試作データです。

そのため、`ElementId`、`FamilyName`、`TypeName` などの列名は、PoCの標準列に合わせるために仮で対応させていますが、正式なRevit内部情報とは一致していません。

今後は、Revit集計表側の列構成を見直し、正式なElementId、FamilyName、TypeName、Levelなどを取得できるか確認したうえで、品質チェック用CSVの列定義を更新します。

このデータ辞書は、6月以降のデータクレンジング、品質チェックv0.2、品質メトリクス作成、特徴量設計へつなげるための基礎資料として使用します。