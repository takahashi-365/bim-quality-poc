# 修正優先度分類モデル 設計メモ

## 目的

このメモは、将来的に作成する `train_fix_priority_model.py` の設計方針を整理するためのものです。

`train_fix_priority_model.py` は、BIM品質チェック結果から作成した特徴量データセットをもとに、各BIM要素の修正優先度を High / Medium / Low に分類する簡易機械学習モデルとして構想します。

このモデルは、本格的な実務判定や自動修正を目的とするものではなく、BIM品質チェック結果をAI・機械学習の入力データとして扱い、修正優先度分類の考え方を検証するためのPoCです。

## 位置づけ

このモデルは、以下の流れの後半に位置づけます。

```text
Revit書き出しTXT
↓
convert_revit_schedule.py でCSVへ変換
↓
check_bim_quality.py で品質チェック
↓
check_results_v001.csv / check_results_revit_v001.csv を出力
↓
create_bim_features.py で特徴量データセットを作成
↓
bim_features_v001.csv を出力
↓
train_fix_priority_model.py で修正優先度分類モデルを作成
↓
fix_priority_predictions_v001.csv を出力
```

## 入力データ

想定する入力データは以下です。

```text
04_output_csv/bim_features_v001.csv
```

このファイルは、`create_bim_features.py` によって作成される特徴量データセットです。

## 入力特徴量候補

モデルに入力する特徴量は、以下を想定します。

### Category

BIM要素のカテゴリです。

例：

- Doors
- Rooms
- Walls

機械学習モデルでは文字列のまま扱いにくいため、数値化またはone-hot encodingを検討します。

### MissingFieldCount

要素ごとの未入力項目数です。

未入力が多い要素ほど修正優先度が高くなる可能性があります。

### HasClassificationCode

分類コードが入力されているかどうかを表します。

- 入力あり：1
- 未入力：0

分類コードが未入力の場合、集計・検索・分析・AI活用に影響する可能性があるため、修正優先度に影響する特徴量として扱います。

### FamilyNameValid

ファミリ名が命名規則に適合しているかどうかを表します。

- 適合：1
- 違反あり：0

命名規則違反がある場合、BIM標準化や検索性に影響するため、修正優先度に影響する特徴量として扱います。

### RuleViolationCount

要素ごとのルール違反数です。

違反数が多いほど、修正優先度が高くなる可能性があります。

### SeverityScore

重大度を数値化した値です。

例：

- High：3
- Medium：2
- Low：1

重大度が高い違反を含む要素ほど、修正優先度が高くなる可能性があります。

### QualityScore

要素ごとの品質スコアです。

点数が低いほど、修正優先度が高くなる可能性があります。

## 出力ラベル

モデルが予測する出力は以下です。

```text
FixPriority
```

分類クラスは以下の3つを想定します。

- High
- Medium
- Low

## FixPriority の初期ラベル作成案

実案件の修正履歴データがないため、初期PoCではルールベースで仮ラベルを作成します。

### 案1：違反件数ベース

```text
RuleViolationCount >= 3 → High
RuleViolationCount == 2 → Medium
RuleViolationCount <= 1 → Low
```

### 案2：重大度スコアベース

```text
SeverityScore >= 5 → High
SeverityScore >= 3 → Medium
SeverityScore < 3 → Low
```

### 案3：品質スコアベース

```text
QualityScore < 60 → High
QualityScore < 80 → Medium
QualityScore >= 80 → Low
```

初期版では、まず違反件数と重大度スコアを組み合わせてラベルを作成することを検討します。

例：

```text
RuleViolationCount >= 3 または SeverityScore >= 5 → High
RuleViolationCount == 2 または SeverityScore >= 3 → Medium
それ以外 → Low
```

## 使用予定ライブラリ

- pandas
- scikit-learn

## 使用予定モデル

初期版では、以下の分類モデルを試します。

### DecisionTreeClassifier

判断の流れが比較的説明しやすいモデルです。

修正優先度分類の初期PoCとして使いやすいです。

### RandomForestClassifier

複数の決定木を組み合わせた分類モデルです。

DecisionTreeより安定した予測が期待できます。

初期版では、DecisionTreeClassifierを先に作成し、その後RandomForestClassifierを試す予定です。

## 学習・評価の流れ

1. `bim_features_v001.csv` を読み込む
2. 入力特徴量と出力ラベルを分ける
3. カテゴリなどの文字列データを数値化する
4. 学習データとテストデータに分割する
5. DecisionTreeClassifierでモデルを学習する
6. テストデータで予測する
7. accuracyを確認する
8. classification_reportを出力する
9. RandomForestClassifierでも同様に試す
10. 予測結果をCSVに出力する

## 出力データ

想定する出力ファイルは以下です。

```text
04_output_csv/model_evaluation_v001.txt
04_output_csv/fix_priority_predictions_v001.csv
```

### model_evaluation_v001.txt

モデルの評価結果を保存します。

含める内容の例：

- 使用モデル
- 使用特徴量
- accuracy
- classification_report
- モデルの限界

### fix_priority_predictions_v001.csv

修正優先度の予測結果を保存します。

含める列の例：

- ElementId
- Category
- FamilyName
- TypeName
- RuleViolationCount
- SeverityScore
- QualityScore
- FixPriority
- PredictedFixPriority

## モデルの限界

このモデルは、実案件の修正履歴や人間の判断結果を教師データにしているわけではありません。

初期PoCでは、ルールベースで作成した仮ラベルをもとに分類モデルを作成するため、実務上の正解を予測するモデルではなく、機械学習の流れを検証するためのものです。

そのため、READMEやポートフォリオでは以下のように説明します。

```text
本モデルは、BIM品質チェック結果を特徴量化し、修正優先度分類の流れを検証するための簡易PoCです。
実案件の修正履歴データを用いた実運用モデルではなく、ルールベースで作成した仮ラベルを教師データとして使用しています。
```

## このモデルで示したいこと

- BIM品質チェック結果を機械学習の入力データとして扱える
- pandasで特徴量データを読み込み、学習用データに整形できる
- scikit-learnで分類モデルを作成できる
- 学習データとテストデータに分割して評価できる
- accuracyやclassification_reportでモデル評価ができる
- 予測結果をCSVとして出力できる
- AI・機械学習エンジニア向けの成果物として説明できる

## 今後の改善案

- 実際の修正履歴データを使って教師ラベルを作成する
- 修正工数や影響範囲を特徴量に追加する
- RuleIdごとの重要度を特徴量に追加する
- Severityごとの違反件数を特徴量に追加する
- Categoryをone-hot encodingにする
- モデル比較を増やす
- Power BIで予測結果を可視化する
- Streamlitで予測結果を表示する
- 生成AI向けプロンプトに修正優先度予測結果を含める

## 5月時点の位置づけ

5月時点では、`train_fix_priority_model.py` の実装は行わず、設計メモの作成までとします。

目的は、8月に予定している簡易機械学習モデル作成に向けて、入力データ、特徴量、出力ラベル、使用モデル、評価方法、モデルの限界を事前に整理することです。

このメモにより、BIM品質チェックPoCを、単なるルールチェックや可視化にとどめず、機械学習による修正優先度分類へ拡張する方向性を明確にします。