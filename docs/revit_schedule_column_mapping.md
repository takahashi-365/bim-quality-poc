# Revit Schedule Column Mapping

## BIM Data Quality & AI Readiness Assessment PoC

## この資料の目的

この資料は、Revit集計表TXTから品質チェック用CSVへ変換する際の列マッピングを整理するための資料です。

現時点では、Revit由来データ対応は初期試作段階であり、一部の列は正式なRevit内部情報ではなく、建具表上の列をPoC用に仮対応させています。

この資料では、以下を明確にします。

* Revit書き出しTXTのどの列を、品質チェック用CSVのどの列に対応させているか
* 現在のマッピングが正式情報か、仮設定か
* 品質チェック、AI Readiness Score、AI Context、Fix Guideへ与える影響
* 今後、正式な列マッピングへ改善するための方針

---

## 1. 対象ファイル

### 入力TXT

```text
03_input_csv/door_schedule_SD_export_test_v001.txt
```

Revitのドア建具表をタブ区切りTXTとして書き出したファイルです。

### 変換後CSV

```text
03_input_csv/door_schedule_converted_v002.csv
```

`src/convert_revit_schedule.py` により、Revit書き出しTXTから品質チェック用に変換したCSVです。

### クレンジング済みCSV

```text
03_input_csv/cleaned_bim_data_v001.csv
```

`src/clean_bim_data.py` により、品質チェック用に列順・空欄・重複などを整理したCSVです。

---

## 2. 現在の処理フロー

```text
Revit書き出しTXT
↓
door_schedule_SD_export_test_v001.txt
↓
convert_revit_schedule.py
↓
door_schedule_converted_v002.csv
↓
clean_bim_data.py
↓
cleaned_bim_data_v001.csv
↓
check_bim_quality.py
↓
check_results_revit_v002.csv
```

その後、以下の処理へ接続します。

```text
calculate_quality_metrics.py
↓
quality_metrics_v001.csv
rule_summary_v001.csv
category_summary_v001.csv
element_summary_v001.csv

create_bim_features.py
↓
bim_features_v001.csv

calculate_ai_readiness_score.py
↓
ai_readiness_scores_v001.csv

generate_ai_context.py
↓
ai_context_v002.json
ai_context_v002.md

generate_fix_guide.py
↓
fix_guides_v001.md
```

---

## 3. 現在の列マッピング概要

現時点では、Revit書き出しTXTの一部列を、PoC用の品質チェック標準列へ仮マッピングしています。

| 品質チェック用CSV列            | 元TXT列番号 | 元TXTの値の例                                  | 推定される意味      | 現在の扱い       |
| ---------------------- | ------: | ----------------------------------------- | ------------ | ----------- |
| Category               |     固定値 | Doors                                     | Revitカテゴリ    | 固定値         |
| ElementId              |       1 | 101, 102, 201                             | 建具番号・建具符号    | 仮ID         |
| FamilyName             |       0 | SD                                        | 建具種別・建具表種別   | 仮FamilyName |
| TypeName               |       3 | 管理用出入口, PS, 電気室 1F                        | 設置場所・室名・用途名称 | 仮TypeName   |
| Level                  |      なし | 空欄                                        | 階情報          | 未対応         |
| BIM_ClassificationCode |      なし | 空欄                                        | 分類コード        | 未対応         |
| BIM_ModelRole          |      なし | 空欄                                        | モデル上の役割      | 未対応         |
| BIM_Zone               |      なし | 空欄                                        | ゾーン情報        | 未対応         |
| SourceFile             | 入力ファイル名 | door_schedule_SD_export_test_v001.txt     | 元ファイル名       | 固定付与        |
| ModelName              |     固定値 | BIM_Quality_Check_Sample_Model_R2024_v001 | モデル名         | 固定付与        |

---

## 4. 現在の仮マッピング詳細

### Category

現在の設定：

```text
Doors
```

扱い：

ドア建具表のみを対象としているため、`Category` は固定値 `Doors` としています。

注意点：

現時点では Walls、Rooms などの他カテゴリには未対応です。

今後の方針：

将来的には、入力ファイルやRevitカテゴリに応じて `Walls`、`Doors`、`Rooms` などを切り替える方針です。

---

### ElementId

現在の設定：

```text
元TXT列番号 1
```

値の例：

```text
101
102
201
```

現時点の意味：

建具表上の建具番号、建具符号、またはスケジュール上の識別番号に近い値として扱っています。

重要な注意点：

この `ElementId` は、Revit内部ElementIdではありません。

現在のPoCでは、ElementIdという標準列名に合わせるため、建具番号を仮IDとして使用しています。

影響：

`ElementId` は以下の処理でキーとして使っています。

* 品質チェック結果の集計
* ElementId別 QualityScore
* 特徴量データセット
* AI Readiness Score
* AI Context v002
* Fix Guide Markdown
* Streamlit上のElement Detail表示

今後の方針：

Revit集計表またはRevit API / pyRevitから正式なRevit内部ElementIdを取得できるか確認します。

正式なElementIdを取得できない場合は、現在の列名を以下のように変更することを検討します。

* `ElementKey`
* `DoorNumber`
* `ScheduleMark`
* `DoorMark`

---

### FamilyName

現在の設定：

```text
元TXT列番号 0
```

値の例：

```text
SD
```

現時点の意味：

建具表上の種別記号、建具種別、または建具表分類に近い値として扱っています。

重要な注意点：

この `FamilyName` は、Revitファミリ名ではありません。

現在のPoCでは、品質チェック標準列に合わせるため、建具種別記号 `SD` を `FamilyName` に仮格納しています。

影響：

`FamilyName` は、R-003「ファミリ命名規則違反」のチェック対象になっています。

ただし、現時点では正式なRevitファミリ名ではないため、R-003の結果は厳密なRevitファミリ命名規則チェックではなく、処理フロー確認用の参考結果として扱います。

今後の方針：

Revit集計表側で、実際のRevitファミリ名を出力できるか確認します。

正式なファミリ名を取得できない場合は、現在の列名を以下のように分けることを検討します。

* `ScheduleTypeCode`
* `DoorTypeCode`
* `FamilyName`

---

### TypeName

現在の設定：

```text
元TXT列番号 3
```

値の例：

```text
管理用出入口
PS
電気室 1F
ごみ置き場
```

現時点の意味：

設置場所、室名、用途名称、または建具が関連する空間名に近い値として扱っています。

重要な注意点：

この `TypeName` は、Revitタイプ名ではありません。

現在のPoCでは、品質チェック標準列に合わせるため、設置場所・室名に近い列を `TypeName` に仮格納しています。

影響：

`TypeName` は、現時点では主に表示用、特徴量確認用、AI Context上の要素説明用として使用しています。

今後の方針：

Revit集計表側で、正式なRevitタイプ名を出力できるか確認します。

現在の列は、正式には以下のような名前で扱う方が自然な可能性があります。

* `LocationName`
* `RoomName`
* `UseName`
* `OpeningLocation`

---

### Level

現在の設定：

```text
空欄
```

現時点の意味：

階情報として列は用意していますが、現時点ではRevit書き出しTXTから値を取得していません。

影響：

現時点では品質チェック、AI Readiness Score、AI Context、Fix Guideへの影響は限定的です。

今後の方針：

Revit集計表側で、配置階、関連レベル、またはドアが属する階情報を出力できるか確認します。

---

### BIM_ClassificationCode

現在の設定：

```text
空欄
```

現時点の意味：

BIM分類コードを想定した列です。

影響：

R-002「分類コード未入力」のチェック対象になっています。

現時点では全要素で空欄のため、全要素が分類コード未入力として検出されます。

この結果は、現時点では正確な実務品質評価ではなく、分類コード未入力を検出する処理フロー確認用の結果として扱います。

今後の方針：

分類体系、社内BIM標準、またはプロジェクト要件に応じて、分類コードを格納する列を追加することを検討します。

---

### BIM_ModelRole

現在の設定：

```text
空欄
```

現時点の意味：

モデル上の役割を想定した列です。

影響：

R-001「必須パラメータ未入力」のチェック対象になっています。

現時点では全要素で空欄のため、全要素が未入力として検出されます。

今後の方針：

設備、意匠、構造、管理、分析用途など、モデル上の役割を表す列として定義できるか検討します。

---

### BIM_Zone

現在の設定：

```text
空欄
```

現時点の意味：

ゾーン情報を想定した列です。

影響：

R-001「必須パラメータ未入力」のチェック対象になっています。

現時点では全要素で空欄のため、全要素が未入力として検出されます。

今後の方針：

建物ゾーン、フロアゾーン、防火区画、管理区分などの情報を格納できるか検討します。

---

### SourceFile

現在の設定：

```text
door_schedule_SD_export_test_v001.txt
```

現時点の意味：

変換元のRevit書き出しTXTファイル名です。

扱い：

品質チェック結果、AI Context、Fix Guideで元データ追跡用として使用します。

今後の方針：

継続使用します。

---

### ModelName

現在の設定：

```text
BIM_Quality_Check_Sample_Model_R2024_v001
```

現時点の意味：

検証用サンプルモデル名です。

扱い：

現時点では固定値として付与しています。

今後の方針：

将来的には設定ファイル化、または入力ファイル単位で切り替えられるようにすることを検討します。

---

## 5. 現在の変換結果

`convert_revit_schedule.py` の実行結果は以下です。

```text
Raw data shape: (26, 33)
Removed non-data rows: 1
Converted data shape: (25, 10)
```

解釈：

* 元TXTは26行、33列として読み込まれた。
* 先頭に実データではない可能性がある行が1行含まれていた。
* `ElementId` が空欄の非データ行を除外し、25行を品質チェック対象とした。
* 変換後CSVは25行、10列となった。

---

## 6. 品質チェックへの影響

現在の仮マッピングにより、品質チェックでは以下の結果が出ています。

対象ファイル：

```text
04_output_csv/check_results_revit_v002.csv
```

対象要素数：

```text
25
```

違反件数：

```text
100
```

RuleId別内訳：

| RuleId | 内容         | 件数 | 主な理由                                  |
| ------ | ---------- | -: | ------------------------------------- |
| R-001  | 必須パラメータ未入力 | 50 | `BIM_ModelRole` と `BIM_Zone` が空欄      |
| R-002  | 分類コード未入力   | 25 | `BIM_ClassificationCode` が空欄          |
| R-003  | ファミリ命名規則違反 | 25 | `FamilyName` に仮格納した `SD` が命名規則に合わない扱い |

注意点：

この100件の違反は、Revitモデルの正式な品質評価ではありません。

現時点では、PoCとして品質チェック処理、RuleId連携、メトリクス作成、AI Readiness Score、AI Context、Fix Guide生成の流れを確認するための結果として扱います。

---

## 7. AI Readiness Assessmentへの影響

現在の仮マッピングにより、AI Readiness Scoreは以下の結果になっています。

対象ファイル：

```text
04_output_csv/ai_readiness_scores_v001.csv
```

結果：

```text
AIReadinessScore = 40
AIReadinessLevel = Low
HumanReviewRequired = True
```

全25要素が同じ結果になっています。

理由：

各要素に以下の違反が含まれているためです。

* `BIM_ModelRole` 未入力
* `BIM_Zone` 未入力
* `BIM_ClassificationCode` 未入力
* `FamilyName` 命名規則違反

この結果は、現時点の入力データがAI活用に適していないという正式評価ではなく、AI活用前に属性情報、分類コード、命名規則を整備する必要があることを説明するためのPoC結果として扱います。

---

## 8. AI Context / Fix Guideへの影響

現在の仮マッピングは、AI Context v002とFix Guide Markdownにも影響します。

### AI Context v002

対象ファイル：

```text
04_output_csv/ai_context_v002.json
04_output_csv/ai_context_v002.md
```

影響：

* `ElementId` は建具番号として表示される。
* `FamilyName` は `SD` として表示される。
* `TypeName` は設置場所・室名に近い値として表示される。
* `AIReadinessScore` は全要素40となる。
* `AIReadinessLevel` は全要素Lowとなる。
* `HumanReviewRequired` は全要素Trueとなる。

### Fix Guide Markdown

対象ファイル：

```text
04_output_csv/fix_guides_v001.md
```

影響：

* ElementId別に修正ガイドが出力される。
* R-001、R-002、R-003が主な修正対象として表示される。
* `FamilyName = SD` は命名規則違反として表示される。
* 空欄の `BIM_ModelRole`、`BIM_Zone`、`BIM_ClassificationCode` が修正対象として表示される。

---

## 9. 正式マッピングで目指す列構成

将来的には、以下のような列構成を目指します。

| 標準列名                   | 正式に取得したい情報       | 取得方法の候補                         |
| ---------------------- | ---------------- | ------------------------------- |
| ElementId              | Revit内部ElementId | Revit API / pyRevit / 集計表にID列追加 |
| ElementKey             | PoCまたはCSV上の識別キー  | CSV変換時に付与                       |
| DoorNumber             | 建具番号・建具符号        | Revit集計表                        |
| Category               | Revitカテゴリ        | Revitカテゴリまたは入力ファイル種別            |
| FamilyName             | Revitファミリ名       | Revit集計表 / Revit API            |
| TypeName               | Revitタイプ名        | Revit集計表 / Revit API            |
| LocationName           | 設置場所・用途名称        | Revit集計表                        |
| RoomName               | 関連室名             | Revit集計表                        |
| Level                  | 配置階              | Revit集計表 / Revit API            |
| BIM_ClassificationCode | 分類コード            | 共有パラメータ / CSV列                  |
| BIM_ModelRole          | モデル上の役割          | 共有パラメータ / CSV列                  |
| BIM_Zone               | ゾーン情報            | 共有パラメータ / CSV列                  |
| SourceFile             | 元ファイル名           | CSV変換時に付与                       |
| ModelName              | モデル名             | 設定ファイル / CSV変換時に付与              |

---

## 10. 今後の改善方針

今後、列マッピング改善では以下を確認します。

* Revit集計表側で正式なRevit内部ElementIdを出力できるか
* Revitファミリ名を集計表に含められるか
* Revitタイプ名を集計表に含められるか
* 階情報を取得できるか
* 関連室名、設置場所、用途名称をどの列として扱うべきか
* 分類コードをどのパラメータに格納するか
* BIM_ModelRole、BIM_Zoneを共有パラメータとして持たせるか
* `ElementId` と `DoorNumber` を分離するか
* `FamilyName` と `DoorTypeCode` を分離するか
* `TypeName` と `LocationName` または `RoomName` を分離するか
* 列名変更時に、既存スクリプト、README、docs、Streamlit表示にどの影響が出るか

---

## 11. 現時点の結論

現時点の列マッピングは、Revit由来TXTをPython処理へ接続するための初期試作です。

そのため、`ElementId`、`FamilyName`、`TypeName` は、PoCの標準列に合わせるために仮で対応させていますが、正式なRevit内部情報とは一致していません。

ただし、この仮マッピングを明記することで、PoCとしての前提条件、制約、品質チェック結果の意味、AI Readiness Scoreの意味を説明できる状態にしています。

今後は、正式なRevit内部ElementId、Revitファミリ名、Revitタイプ名、Level、分類コード、モデル上の役割、ゾーン情報を取得できるか確認し、品質チェック用CSVの列定義を改善します。
