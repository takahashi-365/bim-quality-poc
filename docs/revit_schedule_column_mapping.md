# Revit Schedule Column Mapping

## BIM Data Quality & AI Readiness Assessment PoC

## この資料の目的

この資料は、Revit集計表TXTから品質チェック用CSVを作成した初期試作時の列マッピングを整理するための資料です。

現時点のRevit由来データ対応は初期試作であり、一部の列は正式なRevit内部情報ではなく、建具表上の列をPoC用に仮対応させています。

本資料では、以下を明確にします。

* Revit書き出しTXTのどの列を品質チェック用CSVへ対応させたか
* 現在のマッピングが正式情報か仮設定か
* 品質チェック、AI Readiness Score、AI Context、Fix Guideへの影響
* 過去の変換試作と現在の正式な処理範囲
* 将来、正式な列マッピングへ改善するための方針

---

## 1. 対象ファイル

### 入力TXT

```text
03_input_csv/door_schedule_SD_export_test_v001.txt
```

Revitのドア建具表をタブ区切りTXTとして書き出した検証用ファイルです。

### 初期試作で変換したCSV

```text
03_input_csv/door_schedule_converted_v002.csv
```

初期試作の`08_python/convert_revit_schedule.py`を使用して、Revit書き出しTXTから品質チェック用に変換した検証CSVです。

この変換処理は、現在の`src`配下の正式実装には含まれていません。

### クレンジング済みCSV

```text
03_input_csv/cleaned_bim_data_v001.csv
```

`src/clean_bim_data.py`により、品質チェック用に列順、空欄、重複、文字列などを整理したCSVです。

現在の主要な品質チェックパイプラインは、このファイルを入力起点としています。

---

## 2. 初期試作時の変換フロー

```text
Revit書き出しTXT
↓
03_input_csv/door_schedule_SD_export_test_v001.txt
↓
08_python/convert_revit_schedule.py
↓
03_input_csv/door_schedule_converted_v002.csv
↓
src/clean_bim_data.py
↓
03_input_csv/cleaned_bim_data_v001.csv
```

`src/convert_revit_schedule.py`は正式実装として完成しておらず、0バイトの空ファイルだったため削除しました。

そのため、現在の正式な`src`構成にはRevit TXT変換スクリプトを含めていません。

---

## 3. 現在の主要処理フロー

```text
03_input_csv/cleaned_bim_data_v001.csv
↓
src/check_bim_quality.py
↓
04_output_csv/check_results_revit_v002.csv
↓
src/calculate_quality_metrics.py
↓
品質メトリクス・集計CSV
↓
src/create_bim_features.py
↓
04_output_csv/bim_features_v001.csv
↓
src/calculate_ai_readiness_score.py
↓
04_output_csv/ai_readiness_scores_v001.csv
↓
src/generate_ai_context.py
↓
04_output_csv/ai_context_v002.json
04_output_csv/ai_context_v002.md
↓
src/generate_fix_guide.py
↓
04_output_csv/fix_guides_v001.md
```

---

## 4. 現在の列マッピング概要

| 品質チェック用CSV列            | 元TXT列番号 | 元TXTの値の例                                  | 推定される意味      | 現在の扱い       |
| ---------------------- | ------: | ----------------------------------------- | ------------ | ----------- |
| Category               |     固定値 | Doors                                     | Revitカテゴリ    | 固定値         |
| ElementId              |       1 | 101, 102, 201                             | 建具番号・建具符号    | 仮ID         |
| FamilyName             |       0 | SD                                        | 建具種別・種別記号    | 仮FamilyName |
| TypeName               |       3 | 管理用出入口、PS、電気室1F                           | 設置場所・室名・用途名称 | 仮TypeName   |
| Level                  |      なし | 空欄                                        | 階情報          | 未対応         |
| BIM_ClassificationCode |      なし | 空欄                                        | 分類コード        | 未対応         |
| BIM_ModelRole          |      なし | 空欄                                        | モデル上の役割      | 未対応         |
| BIM_Zone               |      なし | 空欄                                        | ゾーン情報        | 未対応         |
| SourceFile             | 入力ファイル名 | door_schedule_SD_export_test_v001.txt     | 元ファイル名       | 固定付与        |
| ModelName              |     固定値 | BIM_Quality_Check_Sample_Model_R2024_v001 | モデル名         | 固定付与        |

---

## 5. 列マッピング詳細

### Category

現在の設定：

```text
Doors
```

ドア建具表のみを対象としているため、固定値`Doors`を使用しています。

制約：

* Walls、Roomsなどの他カテゴリには対応していません。
* 入力ファイルから自動判定する処理ではありません。

今後の方針：

* 入力ファイル種別に応じたカテゴリ設定
* Revit API / pyRevitからのCategory取得
* 複数カテゴリ対応

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

建具表上の建具番号、建具符号、またはスケジュール上の識別番号に近い値です。

重要な注意点：

この`ElementId`はRevit内部ElementIdではありません。

PoC内の集計キーとして利用するため、建具番号を仮IDとして標準列`ElementId`へ格納しています。

使用箇所：

* 品質チェック結果
* ElementId別QualityScore
* 特徴量データセット
* AI Readiness Score
* AI Context v002
* Fix Guide Markdown
* StreamlitのElement Detail

今後の方針：

* Revit内部ElementIdを取得する
* Revit UniqueIdを取得する
* 建具番号は`DoorNumber`または`ScheduleMark`として分離する
* PoC内の識別キーとして`ElementKey`を追加する

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

建具種別、種別記号、または建具表分類に近い値です。

重要な注意点：

この`FamilyName`は正式なRevitファミリ名ではありません。

品質チェック用の標準列へ合わせるため、種別記号`SD`を仮格納しています。

影響：

`FamilyName`はR-003「ファミリ命名規則違反」のチェック対象です。

ただし、正式なRevitファミリ名ではないため、R-003の結果は厳密なRevitファミリ命名規則評価ではありません。

処理経路を確認するための参考結果です。

今後の方針：

* Revit集計表へ正式なFamilyName列を追加する
* pyRevit / Revit APIからFamilyNameを取得する
* `DoorTypeCode`と`FamilyName`を分離する

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

設置場所、室名、用途名称、または建具が関連する空間名に近い値です。

重要な注意点：

この`TypeName`は正式なRevitタイプ名ではありません。

品質チェック用の標準列へ合わせるため、設置場所・室名に近い列を仮格納しています。

使用箇所：

* 品質チェック結果の表示
* 特徴量確認
* AI Context上の要素説明
* Streamlit表示

今後の方針：

* 正式なRevit TypeNameを取得する
* 現在の列を`LocationName`または`RoomName`へ変更する
* TypeNameとLocationNameを別列として管理する

---

### Level

現在の設定：

```text
空欄
```

階情報として列は用意していますが、現在のTXTから値を取得していません。

今後の方針：

* Revit集計表へLevel列を追加する
* 配置レベルをpyRevit / Revit APIから取得する
* 表示用Levelと内部LevelIdを必要に応じて分離する

---

### BIM_ClassificationCode

現在の設定：

```text
空欄
```

BIM分類コードを想定した列です。

影響：

R-002「分類コード未入力」のチェック対象です。

全要素が空欄のため、全25要素でR-002が検出されます。

この結果は正式な実務評価ではなく、分類コード未入力を検出する処理経路の確認結果です。

今後の方針：

* 採用する分類体系を決める
* 共有パラメータとして保持する
* 社内BIM標準や発注者要件と対応させる
* 分類コードの形式検証ルールを追加する

---

### BIM_ModelRole

現在の設定：

```text
空欄
```

モデル上の役割を想定した列です。

影響：

R-001「必須パラメータ未入力」のチェック対象です。

全要素が空欄のため、全要素で未入力として検出されます。

今後の方針：

* 意匠、構造、設備、管理、分析用途などの定義
* 共有パラメータ化
* モデル用途との対応整理

---

### BIM_Zone

現在の設定：

```text
空欄
```

ゾーン情報を想定した列です。

影響：

R-001「必須パラメータ未入力」のチェック対象です。

全要素が空欄のため、全要素で未入力として検出されます。

今後の方針：

* 建物ゾーン
* フロアゾーン
* 防火区画
* 管理区分
* 工区
* 設備系統

など、用途に応じた定義を検討します。

---

### SourceFile

現在の設定：

```text
door_schedule_SD_export_test_v001.txt
```

変換元のRevit書き出しTXTファイル名です。

使用目的：

* 元データの追跡
* 品質チェック結果の出典確認
* AI Contextへの入力情報付与
* Fix Guideへの入力情報付与

今後も継続して使用します。

---

### ModelName

現在の設定：

```text
BIM_Quality_Check_Sample_Model_R2024_v001
```

検証用サンプルモデル名です。

現時点では固定値として付与しています。

今後の方針：

* 設定ファイル化
* 入力ファイル単位で切り替える
* Revitモデル情報から取得する

---

## 6. 初期試作時の変換結果

初期試作の`08_python/convert_revit_schedule.py`を実行した際の記録は以下です。

```text
Raw data shape: (26, 33)
Removed non-data rows: 1
Converted data shape: (25, 10)
```

解釈：

* 元TXTは26行、33列として読み込まれた
* 先頭に非データ行が1行含まれていた
* ElementId相当列が空欄の行を除外した
* 25行を品質チェック対象とした
* 変換後CSVは25行、10列となった

この結果は初期試作時の記録であり、現在の`src`配下に同じ変換処理が存在することを示すものではありません。

---

## 7. 品質チェックへの影響

対象：

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

| RuleId | 内容         | 件数 | 主な理由                      |
| ------ | ---------- | -: | ------------------------- |
| R-001  | 必須パラメータ未入力 | 50 | BIM_ModelRoleとBIM_Zoneが空欄 |
| R-002  | 分類コード未入力   | 25 | BIM_ClassificationCodeが空欄 |
| R-003  | ファミリ命名規則違反 | 25 | 仮FamilyNameのSDが命名規則に合わない  |

この100件は、Revitモデルの正式な品質評価ではありません。

仮マッピングを用いて品質チェック、RuleId連携、メトリクス作成、AI Readiness Score、AI Context、Fix Guideの処理経路を確認した結果です。

---

## 8. AI Readiness Assessmentへの影響

対象：

```text
04_output_csv/ai_readiness_scores_v001.csv
```

結果：

```text
AIReadinessScore = 40
AIReadinessLevel = Low
HumanReviewRequired = True
```

全25要素が同じ結果です。

主な理由：

* BIM_ModelRole未入力
* BIM_Zone未入力
* BIM_ClassificationCode未入力
* 仮FamilyNameが命名規則違反

AIReadinessScoreは、Rule Master v003に設定した仮ペナルティを用いるルールベース指標です。

この結果は、入力データが正式にAI活用不適格であることを証明するものではありません。

属性情報、分類コード、命名規則を整備する必要性を説明するためのPoC結果です。

---

## 9. AI Contextへの影響

対象：

```text
04_output_csv/ai_context_v002.json
04_output_csv/ai_context_v002.md
```

仮マッピングによる影響：

* ElementIdは建具番号として表示される
* FamilyNameは`SD`として表示される
* TypeNameは設置場所・室名に近い値として表示される
* AIReadinessScoreは全要素40
* AIReadinessLevelは全要素Low
* HumanReviewRequiredは全要素True

このため、AI Contextを参照する場合も、列の意味が正式なRevit内部情報ではないことを前提とする必要があります。

---

## 10. Fix Guideへの影響

対象：

```text
04_output_csv/fix_guides_v001.md
```

仮マッピングによる影響：

* R-001、R-002、R-003が主な修正対象として表示される
* `FamilyName = SD`が命名規則違反として表示される
* BIM_ModelRoleが未入力として表示される
* BIM_Zoneが未入力として表示される
* BIM_ClassificationCodeが未入力として表示される

Fix Guideは、正式なモデル修正指示ではありません。

RuleIdベースで、人間が確認すべき項目を整理するための参考情報です。

---

## 11. 正式マッピングで目指す列構成

| 標準列名                   | 正式に取得したい情報       | 取得方法候補                         |
| ---------------------- | ---------------- | ------------------------------ |
| ElementId              | Revit内部ElementId | pyRevit / Revit API            |
| UniqueId               | Revit UniqueId   | pyRevit / Revit API            |
| ElementKey             | PoC内の安定識別キー      | データ生成時に付与                      |
| DoorNumber             | 建具番号・建具符号        | Revit集計表                       |
| Category               | Revitカテゴリ        | 集計表 / pyRevit / Revit API      |
| FamilyName             | Revitファミリ名       | 集計表 / pyRevit / Revit API      |
| TypeName               | Revitタイプ名        | 集計表 / pyRevit / Revit API      |
| LocationName           | 設置場所・用途名称        | Revit集計表                       |
| RoomName               | 関連室名             | Revit集計表 / pyRevit / Revit API |
| Level                  | 配置階              | 集計表 / pyRevit / Revit API      |
| BIM_ClassificationCode | 分類コード            | 共有パラメータ                        |
| BIM_ModelRole          | モデル上の役割          | 共有パラメータ                        |
| BIM_Zone               | ゾーン情報            | 共有パラメータ                        |
| SourceFile             | 元ファイル名           | データ生成時に付与                      |
| ModelName              | モデル名             | 設定またはRevit情報                   |

---

## 12. 今後の改善方針

* 正式なRevit内部ElementIdを取得する
* UniqueIdを取得する
* Revitファミリ名を取得する
* Revitタイプ名を取得する
* Levelを取得する
* RoomNameを取得する
* DoorNumberとElementIdを分離する
* DoorTypeCodeとFamilyNameを分離する
* TypeNameとLocationNameを分離する
* 分類コードの格納方法を決める
* BIM_ModelRoleの定義を決める
* BIM_Zoneの定義を決める
* pyRevit出力と品質チェックを接続する
* 入力変換処理を正式な`src`モジュールとして再設計する
* 列名変更時の影響範囲をテストする

---

## 13. 現時点の結論

現在の列マッピングは、Revit由来TXTをPython処理へ接続するための初期試作です。

`ElementId`、`FamilyName`、`TypeName`には仮対応が含まれており、正式なRevit内部情報とは一致していません。

また、TXTからCSVへの変換処理は初期試作の`08_python/convert_revit_schedule.py`で検証したものであり、現在の`src`配下の正式実装には含まれていません。

現在の主要品質チェックパイプラインは、整形済みの`cleaned_bim_data_v001.csv`を入力起点としています。

本資料で仮マッピング、制約、影響範囲を明記することで、品質チェック結果、AI Readiness Score、AI Context、Fix Guideの意味を過大評価せず説明できる状態にしています。
