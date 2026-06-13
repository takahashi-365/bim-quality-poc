# 第3段階B：Roomカテゴリ追加 計画

## 目的

第3段階Bでは、既存の `BIM Data Quality & AI Readiness Assessment PoC` を拡張し、現在のDoorカテゴリ中心の品質チェック・AI Readiness Assessmentを、Roomカテゴリにも対応させる。

目的は、BIMデータ品質評価の対象を部材情報だけでなく、空間情報にも広げることである。

Roomは、建築BIMにおける空間・用途・面積・階・ゾーンなどの意味情報を持つため、BI、データ分析、生成AI、RAGで活用する前に品質確認が必要な重要カテゴリである。

---

## 位置づけ

本作業は、新規PoCではなく、既存の `BIM Data Quality & AI Readiness Assessment PoC` の第3段階拡張として実施する。

第2段階までの流れ：

```text
Revit集計表TXT
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
AI Context v002
↓
Fix Guide Markdown
↓
Streamlit表示
```

第3段階Bでは、上記の流れにRoomカテゴリを追加する。

```text
Door Schedule TXT
Room Schedule TXT
↓
CSV変換
↓
カテゴリ別データクレンジング
↓
カテゴリ別RuleIdベース品質チェック
↓
QualityScore
↓
AI Readiness Score
↓
AI Context
↓
Fix Guide
↓
Streamlit表示
```

---

## 第3段階Bでやること

* Revit Room Schedule TXTを入力データとして用意する
* Room用CSV変換方針を整理する
* Room用クレンジング方針を整理する
* Room用クレンジング後データに `Category = Room` を付与する
* Roomカテゴリ用RuleIdを設計する
* Rule MasterにRoom用ルールを追加する方針を確認する
* Rule Masterに `TargetCategory` または同等の対象カテゴリ列があるか確認する
* Roomデータの `Category` とRule Masterの `TargetCategory` を照合し、Room用ルールだけを適用できる構造にする
* 既存の品質チェック処理にRoomカテゴリを接続する
* Room用QualityScoreを算出する
* Room用AI Readiness Scoreを算出する
* Room用AI Contextを生成する
* Room用Fix Guide Markdownを生成する
* Room用pytestを追加する
* 既存Door用pytestが通ることを確認する
* Room用出力が安定した段階でStreamlit反映を検討する
* 必要に応じてREADMEへ小さく反映する
* 詳細はdocsに記録する

---

## 第3段階Bでやらないこと

* Revitモデルの自動修正
* Room情報の自動補完
* 設計判断・施工判断
* 実案件データの利用
* 大規模なRevit API / pyRevit連携
* 本格RAG実装
* Azure AI Search実装
* 生成AI API接続
* 機械学習精度追求
* 複雑なPower BI再設計
* 既存Doorパイプラインを壊すような大改修

---

## Roomカテゴリを追加する理由

現在のPoCは主にDoorカテゴリを対象としている。

Doorカテゴリでは、建具番号、分類コード、ファミリ命名、品質チェック結果、AI Readiness Scoreなどを扱っている。

一方、Roomカテゴリでは、空間に関する意味情報を扱える。

Room情報が不十分な場合、以下のような問題が発生する。

```text
部屋名がないと、空間の意味を判断しにくい
部屋番号がないと、参照・検索・集計が不安定になる
面積がないと、BIやコスト分析に使いにくい
階情報がないと、階別集計・空間把握がしにくい
ゾーン情報がないと、管理区分やRAG検索の文脈が弱くなる
分類コードがないと、標準分類や外部データ連携に使いにくい
```

そのため、RoomカテゴリはAI Readiness Assessmentと相性が良い。

---

## 対象データ

### 入力予定データ

RevitからRoom ScheduleをTXTとして書き出し、PoC用の入力データとして利用する。

想定ファイル：

```text
03_input_csv/room_schedule_export_test_v001.txt
```

変換後CSV：

```text
03_input_csv/room_schedule_converted_v001.csv
```

クレンジング後CSV：

```text
03_input_csv/cleaned_room_data_v001.csv
```

---

## Room用データ項目案

Roomカテゴリでは、以下の項目を候補とする。

```text
ElementId
Category
RoomName
RoomNumber
Level
Area
Zone
Department
ClassificationCode
Finish
Description
```

ただし、Revit集計表から取得できる項目に依存するため、初期版では無理に全項目を揃えない。

初期MVPでは、以下を優先する。

```text
ElementId
Category
RoomName
RoomNumber
Level
Area
ClassificationCode
```

Zone、Department、Finishは、取得できる場合のみ扱う。

---

## Categoryの扱い

Room用クレンジング後データには、カテゴリ識別用に以下を明示的に付与する。

```text
Category = Room
```

目的：

* DoorデータとRoomデータを区別する
* Rule Masterの `TargetCategory` と照合できるようにする
* Door用ルールとRoom用ルールを分けて適用できるようにする
* 将来的な複数カテゴリ対応の土台にする
* AI ContextやRAG用メタデータとしてカテゴリ情報を使えるようにする

想定例：

```text
ElementId,Category,RoomName,RoomNumber,Level,Area,ClassificationCode
R-001,Room,会議室,201,2F,35.2,ROOM-MTG
R-002,Room,事務室,202,2F,48.5,ROOM-OFFICE
```

この `Category = Room` は、Rule Master側の `TargetCategory = Room` と対応させる。

---

## ElementIdの扱い

第3段階Bの初期MVPでは、Room ScheduleからRevit内部ElementIdを取得できない可能性がある。

その場合、Roomカテゴリでは、以下の優先順位でPoC上の仮ElementIdを検討する。

```text
1. Revit内部ElementIdが取得できる場合：内部ElementId
2. RoomNumber + Level
3. RoomName + Level
4. PoC用連番
```

`RoomNumber` 単体は、階をまたいで重複する可能性があるため、初期MVPでは `RoomNumber + Level` を優先する。

注意点：

```text
Roomカテゴリ初期MVPのElementIdは、Revit内部ElementIdではなく、Room Schedule上で識別可能な番号または仮IDを使用する可能性がある。
```

Revit内部ElementId / UniqueIdの取得は、第3段階C：pyRevitでElementId / UniqueId取得PoCで扱う。

---

## Areaの扱い

RoomのAreaは、Revit Scheduleの出力形式により、単位付き文字列になる可能性がある。

想定例：

```text
12.34
12.34 m²
12.34㎡
0
空欄
```

初期MVPでは、数値変換可能な範囲でAreaMissingOrZeroを判定する。

方針：

```text
Areaが空欄の場合は未入力として扱う
Areaが0の場合はAreaMissingOrZeroとして扱う
Areaが数値として変換できる場合は数値化して判定する
Areaが単位付き文字列の場合は、可能な範囲で数値部分を抽出する
Areaを数値変換できない場合は、制約として記録する
```

初期MVPでは、Area変換処理を複雑にしすぎない。
変換できないパターンが出た場合は、失敗ではなく、Room Scheduleの出力形式に依存する制約としてdocsに記録する。

---

## Room用RuleId案

初期MVPでは、ルールを増やしすぎない。

まずは以下の6ルール程度に絞る。

| RuleId | RuleName                  | 内容                    | Severity | AI活用上の影響            | 初期MVPでの扱い         |
| ------ | ------------------------- | --------------------- | -------- | ------------------- | ----------------- |
| R-101  | RoomNameMissing           | RoomName未入力           | High     | 空間の意味をAIが判断しにくい     | 対象                |
| R-102  | RoomNumberMissing         | RoomNumber未入力         | High     | 部屋識別・検索・参照が不安定になる   | 対象                |
| R-103  | AreaMissingOrZero         | Area未入力または0           | Medium   | 面積分析・BI・コスト分析に使いにくい | 対象                |
| R-104  | LevelMissing              | Level未入力              | Medium   | 階別集計・空間把握に使いにくい     | 対象                |
| R-105  | ZoneMissing               | Zone未入力               | Low      | 管理区分・検索・RAGの文脈が弱くなる | Zone列が取得できる場合のみ対象 |
| R-106  | ClassificationCodeMissing | ClassificationCode未入力 | High     | 標準分類・外部データ連携に使いにくい  | 対象                |

---

## ZoneMissingの扱い

R-105 `ZoneMissing` は、Room ScheduleからZone列を取得できる場合のみ初期MVPのチェック対象とする。

Zone列が取得できない場合は、以下の扱いとする。

```text
R-105はRuleIdとして定義してもよい
ただし、初期MVPの品質チェック対象からは外す
将来拡張ルールとして扱う
Zone列が取得できないことをdocsに制約として記録する
```

理由：

* RevitサンプルモデルやRoom ScheduleにZone列がない可能性がある
* Zone列がない状態で強制的にチェックすると、全件Low違反になる可能性がある
* 実務上、Zone管理を行っていないモデルもある
* 初期MVPではRoomName、RoomNumber、Area、Level、ClassificationCodeを優先する

---

## Rule Master拡張方針

既存のRule Master v003を拡張するか、Room用Rule Masterを分けるかを検討する。

初期方針：

```text
02_rule_master/bim_rule_master_v003.csv
```

にRoom用ルールを追加する方向を基本とする。

理由：

* RuleIdを一元管理できる
* Door / Roomを同じ品質チェック思想で扱える
* AI Readiness Score、AI Context、Fix Guide生成に接続しやすい

ただし、Door用ルールとRoom用ルールが混在するため、Rule Masterに対象カテゴリを区別できる列があるか確認する。

確認対象：

```text
TargetCategory
Category
Target
ApplicableCategory
```

いずれかの列で、適用対象カテゴリを区別できる構造が望ましい。

例：

```text
RuleId,TargetCategory,RuleName,Severity
D-001,Door,DoorNumberMissing,High
D-002,Door,DoorClassificationCodeMissing,High
R-101,Room,RoomNameMissing,High
R-102,Room,RoomNumberMissing,High
```

方針：

```text
Rule MasterにTargetCategoryまたは同等の対象カテゴリ列があるか確認する。
Door用ルールとRoom用ルールが混在する場合、対象カテゴリで適用ルールを分けられる構造にする。
Room用クレンジング後データには Category = Room を付与し、Rule MasterのTargetCategoryと照合する。
```

TargetCategory相当の列がない場合は、Roomルール追加前に列追加を検討する。

---

## 処理フロー案

```text
Revit Room Schedule TXT
↓
room_schedule_converted_v001.csv
↓
cleaned_room_data_v001.csv
↓
Category = Room を付与
↓
Room用RuleIdベース品質チェック
↓
check_results_room_v001.csv
↓
room_quality_metrics_v001.csv
↓
room_ai_readiness_scores_v001.csv
↓
room_ai_context_v001.md / .json
↓
room_fix_guides_v001.md
↓
Streamlit表示
```

---

## 既存処理への影響

既存のDoor処理を壊さないことを最優先とする。

方針：

* Door用既存ファイルは基本的に変更しない
* Room用処理を追加する形にする
* Room用データには `Category = Room` を付与する
* Rule Master側でDoor用ルールとRoom用ルールを分けられる構造を確認する
* 共通化は必要最小限にする
* 既存pytestが通る状態を維持する
* 追加テストはRoom用に別途作成する

---

## 実装方針

### 方針A：既存スクリプトを拡張

既存スクリプトにCategory分岐を追加する。

候補：

```text
src/convert_revit_schedule.py
src/clean_bim_data.py
src/check_bim_quality.py
src/calculate_quality_metrics.py
src/calculate_ai_readiness_score.py
src/generate_ai_context.py
src/generate_fix_guide.py
```

メリット：

* 既存処理の延長として見えやすい
* 将来的な複数カテゴリ対応へつながる

デメリット：

* 既存Door処理を壊すリスクがある
* 条件分岐が増える

### 方針B：Room用スクリプトを別に作る

Room用に別スクリプトを作成する。

候補：

```text
src/convert_room_schedule.py
src/clean_room_data.py
src/check_room_quality.py
```

メリット：

* 既存Door処理を壊しにくい
* 初期MVPとして安全

デメリット：

* 共通処理が重複する可能性がある

---

## 初期採用方針

初期MVPでは、方針B寄りで進める。

理由：

* 既存PoCの安定状態を崩さないため
* Roomカテゴリの列構成やルールを試しやすいため
* 後で共通化できるため

初期MVPでRoom専用として作る候補：

```text
src/convert_room_schedule.py
src/clean_room_data.py
src/check_room_quality.py
```

一方で、以下は既存処理を流用できるか先に確認する。

```text
src/calculate_quality_metrics.py
src/calculate_ai_readiness_score.py
src/generate_ai_context.py
src/generate_fix_guide.py
```

既存処理を流用できない場合のみ、Room専用スクリプトを追加する。

候補：

```text
src/calculate_room_quality_metrics.py
src/calculate_room_ai_readiness_score.py
src/generate_room_ai_context.py
src/generate_room_fix_guide.py
```

この方針により、初期MVPでファイル数を増やしすぎないようにする。

---

## 作成予定ファイル

### input

```text
03_input_csv/room_schedule_export_test_v001.txt
03_input_csv/room_schedule_converted_v001.csv
03_input_csv/cleaned_room_data_v001.csv
```

### output

```text
04_output_csv/check_results_room_v001.csv
04_output_csv/room_quality_metrics_v001.csv
04_output_csv/room_rule_summary_v001.csv
04_output_csv/room_category_summary_v001.csv
04_output_csv/room_element_summary_v001.csv
04_output_csv/room_ai_readiness_scores_v001.csv
04_output_csv/room_ai_context_v001.json
04_output_csv/room_ai_context_v001.md
04_output_csv/room_fix_guides_v001.md
```

### rule master

基本方針：

```text
02_rule_master/bim_rule_master_v003.csv
```

必要に応じて検討：

```text
02_rule_master/room_rule_master_v001.csv
```

### src

初期MVPで優先：

```text
src/convert_room_schedule.py
src/clean_room_data.py
src/check_room_quality.py
```

既存流用を確認：

```text
src/calculate_quality_metrics.py
src/calculate_ai_readiness_score.py
src/generate_ai_context.py
src/generate_fix_guide.py
```

必要な場合のみ追加：

```text
src/calculate_room_quality_metrics.py
src/calculate_room_ai_readiness_score.py
src/generate_room_ai_context.py
src/generate_room_fix_guide.py
```

### docs

```text
docs/room_category_extension_plan.md
docs/room_rule_specification.md
docs/room_schedule_column_mapping.md
```

### tests

```text
tests/test_room_quality_rules.py
tests/test_room_ai_readiness_score.py
```

---

## Streamlit反映方針

初期MVPでは、Streamlitへ大きく組み込まない。

まずは以下を優先する。

```text
CSV出力
Markdown出力
pytest
docs記録
```

Room用出力が安定した段階で、Streamlitに以下を追加する。

```text
Room Quality Metrics
Room RuleId Summary
Room Element Summary
Room AI Readiness Assessment
Room AI Context Preview
Room Fix Guide Preview
```

READMEへの反映は、Roomカテゴリの出力が安定してから小さく行う。

---

## README / Portfolio PDF更新方針

第3段階Bの初期実装時点では、READMEやPortfolio PDFを大きく更新しない。

まずは以下に記録する。

```text
docs/room_category_extension_plan.md
docs/room_rule_specification.md
docs/room_schedule_column_mapping.md
```

Roomカテゴリの品質チェック、AI Readiness Score、AI Context、Fix Guideが安定した段階で、READMEに小さく追記する。

Portfolio PDFは、第3段階A〜C程度までまとまった段階で更新を検討する。

---

## テスト方針

Room用の最小pytestを追加する。

確認対象：

```text
RoomName未入力判定
RoomNumber未入力判定
Area未入力判定
Area=0判定
Area数値変換
Level未入力判定
ClassificationCode未入力判定
Category = Room が付与されていること
Category = Room の場合にRoom用ルールが適用されること
Zone列がない場合にR-105を無理に適用しないこと
Room用AI Readiness Score計算
Room用HumanReviewRequired判定
```

Areaに関する追加確認候補：

```text
Area="0" を0として扱えるか
Area="" を未入力として扱えるか
Area="12.34㎡" から数値を抽出できるか
Area="12.34 m²" から数値を抽出できるか
数値変換できないAreaを制約として扱えるか
```

初期目標：

```text
既存テストを壊さない
Room用テストを追加する
python -m pytest tests -v が通る
```

---

## 完了条件

第3段階Bの完了条件は以下。

* Room Schedule TXTを用意した
* Room Schedule TXTをCSVへ変換した
* Roomデータをクレンジングした
* Room用クレンジング後データに `Category = Room` を付与した
* Room用RuleIdを定義した
* R-105 ZoneMissingを条件付きルールとして扱った
* Room用ElementIdの扱いを整理した
* 仮ElementIdの優先順位を整理した
* Areaの数値変換方針を整理した
* Rule Masterの対象カテゴリ列を確認した
* Roomデータの `Category` とRule Masterの `TargetCategory` を照合できる構造を確認した
* Room用品質チェック結果を出力した
* Room用QualityScoreを算出した
* Room用AI Readiness Scoreを算出した
* Room用AI Contextを生成した
* Room用Fix Guide Markdownを生成した
* Room用pytestを追加した
* 既存Door用pytestが通ることを確認した
* Roomカテゴリ追加の制約をdocsに記録した
* README反映要否を判断した

---

## 成功とみなす状態

以下の状態になれば、第3段階BのMVPとして成功とする。

```text
Room Schedule TXT
↓
CSV変換
↓
Category = Room を付与
↓
Room品質チェック
↓
Room QualityScore
↓
Room AI Readiness Score
↓
Room AI Context
↓
Room Fix Guide
↓
pytestで主要ロジック確認
```

Roomカテゴリで完璧なルール網羅を目指す必要はない。
重要なのは、Door以外のカテゴリにも既存PoCの品質チェック・AI Readiness Assessmentの考え方を拡張できることを示すことである。

---

## 制約として記録する可能性がある項目

初期MVPでは、以下は制約として記録する可能性がある。

```text
Room ScheduleからRevit内部ElementIdを取得できない
RoomNumber + Level または仮IDをPoC上のElementIdとして扱う
Zone列がRoom Scheduleに存在しない
Areaが単位付き文字列として出力される
Areaを数値変換できないケースがある
ClassificationCode列がRoom Scheduleに存在しない
Door用ルールとRoom用ルールをRule Master上で分ける必要がある
TargetCategory相当の列がRule Masterに存在しない可能性がある
```

制約が出た場合は、PoCの失敗ではなく、実務BIMデータをAI活用する前に確認すべきデータ条件として整理する。

---

## 注意点

* Roomカテゴリ追加で既存Door処理を壊さない
* 最初からルールを増やしすぎない
* Revit集計表に存在しない列を無理に要求しない
* 不明な値を推測で補完しない
* Room用クレンジング後データには `Category = Room` を付与する
* Rule Masterの `TargetCategory` とRoomデータの `Category` を照合できるようにする
* ZoneMissingはZone列がある場合のみ初期MVPのチェック対象にする
* Areaは単位付き文字列の可能性を考慮する
* RoomのElementIdは初期MVPでは仮IDの可能性がある
* 仮ElementIdは `RoomNumber + Level` を優先する
* AI Readiness ScoreはPoC用指標であり、正式基準ではないことを維持する
* Room情報の正しさは最終的にBIM担当者が確認する
* Revitモデル自動修正は行わない
* READMEやPDFをすぐに大きく更新しない

---

## 次の作業手順

### Step 1：Room Schedule TXTの準備

RevitからRoom ScheduleをTXTとして書き出す。

保存先候補：

```text
03_input_csv/room_schedule_export_test_v001.txt
```

---

### Step 2：Room Scheduleの列確認

TXT / CSVの列名を確認し、以下の対応を整理する。

```text
RoomName
RoomNumber
Level
Area
Zone
Department
ClassificationCode
Finish
```

列マッピングは以下に記録する。

```text
docs/room_schedule_column_mapping.md
```

---

### Step 3：ElementIdの扱いを決める

Room ScheduleからRevit内部ElementIdを取得できるか確認する。

取得できない場合、以下の優先順位で仮ElementIdを検討する。

```text
1. Revit内部ElementIdが取得できる場合：内部ElementId
2. RoomNumber + Level
3. RoomName + Level
4. PoC用連番
```

この制約をdocsに記録する。

---

### Step 4：Category = Room の付与方針を確認する

Room用クレンジング後データに、カテゴリ識別用として以下を付与する。

```text
Category = Room
```

この列をRule Masterの `TargetCategory` と照合し、RoomデータにはRoom用ルールだけを適用できるようにする。

---

### Step 5：Areaの形式を確認する

Area列の値を確認する。

確認例：

```text
12.34
12.34 m²
12.34㎡
0
空欄
```

数値変換方針を `docs/room_schedule_column_mapping.md` に記録する。

---

### Step 6：Rule Masterの対象カテゴリ列を確認する

`02_rule_master/bim_rule_master_v003.csv` に、以下のような列があるか確認する。

```text
TargetCategory
Category
Target
ApplicableCategory
```

対象カテゴリ列がない場合は、Roomルール追加前に列追加を検討する。

---

### Step 7：Room用ルール設計

Room用RuleIdを整理する。

保存先候補：

```text
docs/room_rule_specification.md
```

必要に応じて、`bim_rule_master_v003.csv` にRoom用RuleIdを追加する。

---

### Step 8：Room用変換・クレンジング

Room Schedule TXTをCSVへ変換し、品質チェックに使える形式へ整形する。

クレンジング後データには `Category = Room` を付与する。

---

### Step 9：Room用品質チェック

RoomName、RoomNumber、Area、Level、ClassificationCodeなどを対象に、RuleIdベースの品質チェックを行う。

Zone列が取得できる場合のみ、ZoneMissingをチェック対象にする。

---

### Step 10：Room用メトリクス・AI Readiness

Room用QualityScore、AI Readiness Scoreを出力する。

---

### Step 11：Room用AI Context / Fix Guide生成

Room用AI ContextとFix Guide Markdownを生成する。

---

### Step 12：pytest追加

Room用の最小テストを追加し、既存テストと合わせて実行する。

```powershell
python -m pytest tests -v
```

---

### Step 13：docs整理

Roomカテゴリ追加の方針、列マッピング、ルール仕様、制約をdocsへ記録する。

---

### Step 14：README反映判断

MVPが安定した段階で、READMEに小さく反映するか判断する。

---

## 次段階への接続

第3段階Bが完了したら、以下へ接続する。

```text
第3段階C：pyRevitでElementId / UniqueId取得PoC
```

Roomカテゴリ追加により、将来的なRAG / Azure AI Search構成検討でも、DoorだけでなくRoom情報を検索対象・メタデータ候補として扱えるようになる。
