# create_bim_features.py 構想メモ

## 目的

`create_bim_features.py` は、BIM品質チェック結果CSVをもとに、分析や簡易機械学習で使える特徴量データセットを作成するためのPythonスクリプトとして構想する。

現時点では、`check_bim_quality.py` によって出力された品質チェック結果CSVを入力とし、要素ごとの違反数、未入力項目数、分類コード有無、命名規則適合、重大度スコア、品質スコアなどを作成することを想定する。

このスクリプトは、BIM品質チェック結果を単なるエラー一覧で終わらせず、AI・機械学習・データ分析で扱いやすい形に変換するための前処理として位置づける。

## 入力データ

想定する入力データは以下。

```text
04_output_csv/check_results_v001.csv
```

または、Revit由来データ対応後は以下。

```text
04_output_csv/check_results_revit_v001.csv
```

入力データには、以下のような列が含まれる想定。

- CheckId
- ElementId
- Category
- FamilyName
- TypeName
- Level
- ParameterName
- CurrentValue
- RuleId
- RuleName
- Severity
- Status
- FixGuide
- DetectedAt
- SourceFile
- ModelName

## 出力データ

想定する出力データは以下。

```text
04_output_csv/bim_features_v001.csv
```

出力データは、要素単位で1行になる特徴量データセットを想定する。

## 作成したい特徴量

### MissingFieldCount

未入力項目数を表す特徴量。

`ParameterName` が `BIM_ModelRole`、`BIM_Zone`、`BIM_ClassificationCode` などの未入力違反に該当する場合、要素ごとに件数を集計する。

### HasClassificationCode

分類コードが入力されているかどうかを表す特徴量。

- 入力あり：1
- 未入力：0

現時点では、`R-002：分類コード未入力` がある場合は 0、ない場合は 1 とする想定。

### FamilyNameValid

ファミリ名が命名規則に適合しているかどうかを表す特徴量。

- 適合：1
- 違反あり：0

現時点では、`R-003：ファミリ命名規則違反` がある場合は 0、ない場合は 1 とする想定。

### RuleViolationCount

要素ごとのルール違反数を表す特徴量。

同じ `ElementId` に紐づく違反件数を集計する。

### SeverityScore

重大度を数値化した特徴量。

例：

- High：3
- Medium：2
- Low：1

現時点のルールマスターに合わせて、Severityの値を確認しながらマッピングする。

### CategoryEncoded

カテゴリを数値化した特徴量。

例：

- Walls：1
- Doors：2
- Rooms：3

機械学習モデルで扱いやすくするため、カテゴリを数値に変換する。

### QualityScore

要素ごとの品質スコア。

例：

```text
QualityScore = 100 - (RuleViolationCount × 10) - (SeverityScore合計 × 5)
```

ただし、初期版では仮の計算式とし、後で見直す。

## 出力CSVの列案

`bim_features_v001.csv` には、以下の列を持たせる想定。

- ElementId
- Category
- FamilyName
- TypeName
- SourceFile
- ModelName
- MissingFieldCount
- HasClassificationCode
- FamilyNameValid
- RuleViolationCount
- SeverityScore
- CategoryEncoded
- QualityScore
- FixPriorityLabel

## FixPriorityLabel の考え方

修正優先度ラベルを、簡易的に High / Medium / Low で作成する。

初期案：

- RuleViolationCount が 3件以上：High
- RuleViolationCount が 2件：Medium
- RuleViolationCount が 1件以下：Low

または、SeverityScoreを使って以下のように判定する。

- SeverityScore合計が高い：High
- SeverityScore合計が中程度：Medium
- SeverityScore合計が低い：Low

このラベルは、8月に作成予定の `train_fix_priority_model.py` の教師データとして使う可能性がある。

## 主な処理フロー

1. 品質チェック結果CSVを読み込む
2. ElementId単位でデータをグループ化する
3. 要素ごとの違反件数を集計する
4. 未入力項目数を集計する
5. 分類コード有無を判定する
6. ファミリ名の命名規則適合を判定する
7. Severityを数値化する
8. Categoryを数値化する
9. QualityScoreを計算する
10. FixPriorityLabelを仮作成する
11. 特徴量データセットをCSVとして出力する

## このスクリプトで示したいこと

- BIM品質チェック結果を分析用データセットに変換できる
- ルール違反一覧から、要素単位の特徴量を作成できる
- pandasでグループ化、集計、条件判定ができる
- 将来的な機械学習モデルに使える入力データを作成できる
- BIMデータをAI・機械学習で扱うための前処理を設計できる

## 今後の拡張案

- 重大度ごとの違反件数を特徴量に追加する
- RuleIdごとのフラグ列を作成する
- Categoryのone-hot encodingを検討する
- QualityScoreの計算式を改善する
- 修正履歴データがあれば、実際の修正優先度ラベルを作る
- Power BIで特徴量データを可視化する
- scikit-learnで修正優先度分類モデルを作成する

## 5月時点の位置づけ

5月時点では、`create_bim_features.py` の本格実装は行わず、構想メモの作成までとする。

目的は、7月に予定している特徴量作成タスクに向けて、どのような入力データを使い、どのような特徴量を作るかを事前に整理することである。

このメモにより、BIM品質チェックPoCを単なるルールチェックで終わらせず、機械学習やデータ分析へ拡張する方向性を明確にする。