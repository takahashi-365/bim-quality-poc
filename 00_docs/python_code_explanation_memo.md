# Pythonコード説明メモ

## この資料の目的

この資料は、`BIM Data Quality Engineering & AI Analysis PoC` で作成したPythonコードの目的、処理フロー、主要関数、自分の理解を整理するためのメモです。

目的は、単にコードを作成することではなく、面接やポートフォリオ説明時に、各PythonファイルがPoC全体の中でどの役割を持っているかを自分の言葉で説明できる状態にすることです。

現時点では、主に以下の4つのPythonファイルを対象とします。

- `08_python/convert_revit_schedule.py`
- `08_python/check_bim_quality.py`
- `06_ai_demo/ruleid_lookup_demo.py`
- `06_ai_demo/ruleid_prompt_generator_demo.py`

なお、現時点では `08_python` と `06_ai_demo` に試作コードを配置しています。  
今後は処理を整理し、`src` 配下へ段階的に移行する予定です。

---

# convert_revit_schedule.py

## 目的

`convert_revit_schedule.py` は、Revitから書き出した集計表TXTをPython/pandasで読み込み、品質チェックに使いやすいCSV形式へ変換するためのPythonファイルです。

Revitから書き出したTXTは、そのままでは品質チェックや分析に使いにくいため、必要な列だけを抽出し、品質チェック用CSVとして再構成します。

このファイルは、Revit由来データをPython処理パイプラインへ接続するための前処理です。

現時点では、以下の流れを確認済みです。

```text
Revit書き出しTXT
↓
convert_revit_schedule.py で品質チェック用CSVへ変換
↓
door_schedule_converted_v001.csv
↓
check_bim_quality.py で品質チェック
↓
check_results_revit_v001.csv を出力
```

この処理により、手作成CSVだけでなく、Revitから書き出したデータをPoCに取り込む初期フローを確認できました。

---

## 入力ファイル

```text
03_input_csv/door_schedule_SD_export_test_v001.txt
```

Revitから書き出したドア集計表のTXTファイルです。

---

## 出力ファイル

```text
03_input_csv/door_schedule_converted_v001.csv
```

品質チェック用の列構成に変換したCSVファイルです。

---

## 現時点の実行結果

```text
元データ：26行 × 33列
変換後CSV：26行 × 10列
```

変換後CSVでは、品質チェックで扱うために以下のような列構成に整理しています。

- Category
- ElementId
- FamilyName
- TypeName
- Level
- BIM_ClassificationCode
- BIM_ModelRole
- BIM_Zone
- SourceFile
- ModelName

ただし、現時点の列マッピングは仮設定です。

そのため、`door_schedule_converted_v001.csv` は正式な品質評価用データではなく、Revit由来TXTをPython処理に接続できるかを確認するための初期試作データです。

---

## 処理フロー

1. プロジェクトの基準フォルダを設定する
2. Revit書き出しTXTのパスを設定する
3. 出力CSVのパスを設定する
4. pandasでRevit書き出しTXTを読み込む
5. 元データの行数・列数を確認する
6. 品質チェックに必要な列を抽出・再構成する
7. Category、SourceFile、ModelNameなどを付与する
8. BIM_ClassificationCode、BIM_ModelRole、BIM_Zoneなどの品質チェック用列を用意する
9. 品質チェック用CSVとして出力する
10. 変換結果の行数・列数を表示する

---

## 主な処理内容

### Revit TXTの読み込み

Revitから書き出したタブ区切りTXTを、pandasで読み込みます。

この段階で、Revit由来データをPythonで扱えることを確認します。

---

### 必要列の抽出・再構成

元のRevit集計表TXTには多数の列があります。

その中から、品質チェックに必要な列を抽出し、品質チェック用CSVの列構成に変換します。

---

### SourceFile / ModelName の付与

どのファイルから作成されたデータかを追跡できるように、`SourceFile` と `ModelName` を付与します。

これは、後でチェック結果CSVや品質メトリクスに接続するために重要です。

---

### 品質チェック用CSVの出力

変換後のデータをCSVとして出力します。

このCSVを `check_bim_quality.py` に入力することで、Revit由来データに対してRuleIdベースの品質チェックを実行できます。

---

## 現時点の注意点

現時点では、列マッピングは仮設定です。

特に、以下の列については今後整理が必要です。

- ElementId
- FamilyName
- TypeName
- Level
- BIM_ClassificationCode
- BIM_ModelRole
- BIM_Zone

また、`BIM_ClassificationCode`、`BIM_ModelRole`、`BIM_Zone` は現時点では空欄のため、品質チェック時に未入力違反が多く検出されます。

そのため、現時点の目的は正確な品質評価ではなく、Revit書き出しTXTから品質チェック結果CSVを出力する一連の処理フローが動くことを確認することです。

---

## 自分の理解

このファイルは、Revit由来データをPythonで扱うための入口になる処理です。

BIMデータをAI・機械学習・データ分析で扱うには、まずRevitから書き出した情報をPythonで処理できる形に整える必要があります。

`convert_revit_schedule.py` は、そのためにRevit書き出しTXTを読み込み、品質チェックに使いやすいCSVへ変換する役割を持っています。

このファイルがあることで、手作成の検証CSVだけでなく、Revit由来データをPoCに接続できます。

今後は、列マッピング、列名標準化、欠損値処理、不要行削除、入力ファイル指定、出力ファイル指定などを整理し、`src/convert_revit_schedule.py` へ発展させる予定です。

---

# check_bim_quality.py

## 目的

`check_bim_quality.py` は、品質チェック用に整形されたBIMデータCSVを読み込み、あらかじめ用意したBIM品質ルールに基づいてデータの不備をチェックするためのPythonファイルです。

主に、必須項目の未入力、分類コードの未入力、ファミリ名の命名規則違反を確認します。

違反が見つかった場合は、RuleId、違反項目、現在の値、重大度、修正ガイドなどを整理し、チェック結果CSVとして出力します。

このファイルは、BIMデータをAI・機械学習・データ分析で扱う前段階として、データ品質を確認する中心処理です。

現時点では、手作成の検証用CSVに加えて、Revit書き出しTXTを `convert_revit_schedule.py` で品質チェック用CSVへ変換し、そのCSVを `check_bim_quality.py` に入力して、RuleId付き品質チェック結果CSVを出力できることを確認しています。

想定する流れは以下です。

```text
Revit書き出しTXT
↓
convert_revit_schedule.py で品質チェック用CSVへ変換
↓
品質チェック用CSV
↓
check_bim_quality.py で品質チェック
↓
check_results.csv を出力
```

---

## 入力ファイル

初期検証用CSV：

```text
03_input_csv/sample_bim_data_v001.csv
```

Revit由来変換CSV：

```text
03_input_csv/door_schedule_converted_v001.csv
```

ルールマスター：

```text
02_rule_master/bim_rule_master_v001.csv
```

---

## 出力ファイル

初期検証用チェック結果：

```text
04_output_csv/check_results_v001.csv
```

Revit由来データのチェック結果：

```text
04_output_csv/check_results_revit_v001.csv
```

---

## 現時点の実行結果

手作成の検証用CSVでは、以下の結果を確認済みです。

```text
9 issues found
```

Revit由来変換CSVでは、以下の結果を確認済みです。

```text
104 issues found
```

ただし、104件の違反は正確な品質評価ではなく、Revit由来データでも一連の処理フローが動くことを確認するための検証結果です。

---

## 処理フロー

1. プロジェクトの基準フォルダを設定する
2. 入力用BIMデータCSV、ルールマスターCSV、出力CSVのパスを設定する
3. 入力CSVとルールマスターCSVが存在するか確認する
4. pandasを使って入力CSVとルールマスターCSVを読み込む
5. 入力データを1行ずつ確認する
6. 各行に対して、必須項目、分類コード、ファミリ名のチェックを行う
7. 違反が見つかった場合、RuleId付きのチェック結果としてリストに追加する
8. チェック結果をDataFrameに変換する
9. 出力フォルダを作成し、チェック結果CSVを書き出す
10. 検出件数と出力先をターミナルに表示する

---

## 主な関数

### is_blank

値が空欄、NaN、またはスペースだけかどうかを判定する関数です。

BIMデータの必須項目が未入力かどうかを確認するために使います。

---

### get_rule

RuleIdを指定して、ルールマスターCSVから該当するルール情報を取得する関数です。

例えば、`R-001` や `R-002` のようなRuleIdに対応するルール名、重大度、修正ガイドなどを取り出します。

---

### add_result

品質チェックで違反が見つかったときに、チェック結果を1件分追加する関数です。

ElementId、Category、FamilyName、RuleId、Severity、FixGuide、DetectedAtなどをまとめて保存します。

---

### check_required_parameters

`BIM_ModelRole` と `BIM_Zone` が未入力かどうかを確認する関数です。

未入力の場合は、`R-001` のルール違反としてチェック結果に追加します。

---

### check_classification_code

`BIM_ClassificationCode` が未入力かどうかを確認する関数です。

未入力の場合は、`R-002` のルール違反としてチェック結果に追加します。

---

### check_family_naming

CategoryごとにFamilyNameの接頭辞が正しいかを確認する関数です。

例えば、Doorsは `DR_`、Roomsは `RM_`、Wallsは `WAL_` で始まるかを確認します。

規則に合っていない場合は、`R-003` のルール違反としてチェック結果に追加します。

---

### main

全体の処理を実行する関数です。

CSVの存在確認、データ読み込み、各チェック処理、結果CSVの出力までをまとめて行います。

---

## 自分の理解

このファイルは、BIMデータをそのまま使うのではなく、AIや分析に使える状態にする前に、データ品質を確認するための処理です。

現時点では入力データはCSVですが、これは品質チェックしやすい形に整えた中間データとしてのCSVです。

手作成の検証CSVに加えて、Revit集計表から書き出したTXTをPythonで読み込み、品質チェック用CSVへ変換し、その後この `check_bim_quality.py` で品質チェックを行う流れも初期確認済みです。

重要なのは、単にエラーを見つけるだけではなく、RuleIdと紐づけて違反内容を出力している点です。

これにより、あとからPower BIで補助的に可視化したり、RuleId検索に利用したり、生成AI向け構造化コンテキスト生成に利用したり、将来的には品質メトリクス作成や特徴量設計にもつなげられます。

自分のPoCでは、このファイルがBIMデータ品質チェックの中心処理になります。

---

# ruleid_lookup_demo.py

## 目的

`ruleid_lookup_demo.py` は、ユーザーが入力したRuleIdをもとに、BIM品質ルールマスターから該当するルール情報を検索し、画面に表示するためのデモ用Pythonファイルです。

例えば、`R-001` と入力すると、そのRuleIdに対応するルール名、カテゴリ、重大度、対象項目、チェックロジック、業務影響、AI活用時の影響、修正ガイドなどを表示します。

このファイルは、`check_bim_quality.py` で出力されたチェック結果に含まれるRuleIdを起点に、「どのルールに基づく違反なのか」を確認するために使います。

---

## 処理フロー

1. プロジェクトの基準フォルダを設定する
2. ルールマスターCSVのパスを設定する
3. ルールマスターCSVが存在するか確認する
4. pandasを使ってルールマスターCSVを読み込む
5. ユーザーに検索したいRuleIdを入力してもらう
6. 入力されたRuleIdを大文字に変換し、余分な空白を削除する
7. ルールマスターの中から一致するRuleIdを検索する
8. 一致するルールがあれば、ルール詳細を画面に表示する
9. 一致するルールがなければ、見つからないことを表示する
10. `q` が入力されたら処理を終了する

---

## 主な関数

### load_rule_master

ルールマスターCSVを読み込む関数です。

CSVファイルが存在しない場合は、エラーを出します。

---

### search_rule

ユーザーが入力したRuleIdに一致するルールを検索する関数です。

大文字・小文字の違いや前後の空白を調整してから検索します。

該当するRuleIdが見つかった場合は、そのルール情報を返します。

見つからない場合は `None` を返します。

---

### print_rule

検索されたルールの詳細をターミナルに表示する関数です。

RuleId、RuleName、Category、Severity、TargetField、CheckLogic、BusinessImpact、AIUseImpact、FixGuide、Referenceなどを表示します。

---

### main

全体の処理を実行する関数です。

ルールマスターの読み込み、RuleIdの入力受付、ルール検索、結果表示、終了処理をまとめて行います。

---

## 自分の理解

このファイルは、RuleIdからBIM品質ルールの内容を確認するための検索ツールです。

`check_bim_quality.py` で出力されたチェック結果にはRuleIdが含まれるため、そのRuleIdを使って「この違反はどのルールに基づくものか」を確認できます。

この仕組みによって、チェック結果とルールマスターを分けて管理できます。

また、RuleIdを起点に説明や修正ガイドを参照できるため、将来的に生成AI向け構造化コンテキスト生成やRAGに拡張しやすい構成になっています。

このファイル自体は、Revit書き出しTXTやBIMデータCSVを直接処理するものではなく、ルールマスターCSVを検索するための補助的なデモです。

---

# ruleid_prompt_generator_demo.py

## 目的

`ruleid_prompt_generator_demo.py` は、ユーザーが入力したRuleIdをもとに、BIM品質ルールマスターから該当ルールを取得し、そのルール情報を使って生成AI向けのプロンプト文を作成するデモ用Pythonファイルです。

現時点では、OpenAI APIなどを直接呼び出すのではなく、生成AIに渡すためのプロンプト文を作成するところまでを検証しています。

このファイルは、RuleIdベース生成AI向け構造化コンテキスト生成へ発展させるための前段階です。

作成されたプロンプトには、RuleId、ルール名、重大度、対象項目、チェックロジック、業務影響、AI活用時の影響、修正ガイドなどが含まれます。

現時点では、品質チェック結果CSVを直接読み込んでプロンプトを作成しているのではなく、RuleIdを手入力し、そのRuleIdに対応するルールマスター情報を使ってプロンプトを作成しています。

---

## 処理フロー

1. プロジェクトの基準フォルダを設定する
2. ルールマスターCSVとプロンプト出力フォルダのパスを設定する
3. ルールマスターCSVが存在するか確認する
4. pandasを使ってルールマスターCSVを読み込む
5. ユーザーにプロンプトを作成したいRuleIdを入力してもらう
6. 入力されたRuleIdに一致するルールを検索する
7. 該当するルールが見つかった場合、ルール概要を画面に表示する
8. ルール情報をもとに生成AI向けプロンプトを作成する
9. 作成したプロンプトを画面に表示する
10. 必要に応じて、プロンプトをtxtファイルとして保存する
11. `q` が入力されたら処理を終了する

---

## 主な関数

### load_rule_master

ルールマスターCSVを読み込む関数です。

CSVファイルが存在しない場合は、エラーを出します。

---

### search_rule

ユーザーが入力したRuleIdに一致するルールを検索する関数です。

RuleIdの前後の空白を削除し、大文字に変換してから検索します。

見つかった場合はルール情報を返し、見つからない場合は `None` を返します。

---

### build_ai_prompt

ルール情報をもとに、生成AIへ渡すプロンプト文を作成する関数です。

プロンプトには、参照するRuleId、ルール名、重大度、チェックロジック、業務影響、修正ガイドなどが含まれます。

また、資料にない内容を断定しないこと、自動修正を前提にしないこと、人間が最終確認することなど、生成AIに対する回答条件も含めています。

---

### save_prompt

作成したプロンプトをtxtファイルとして保存する関数です。

保存先は `06_ai_demo/generated_prompts` フォルダです。

ファイル名にはRuleIdと日時が入るため、いつ作成したプロンプトか分かるようになっています。

---

### print_rule_summary

選択されたRuleIdの概要を画面に表示する関数です。

RuleId、RuleName、Severity、FixGuideを簡単に確認できます。

---

### main

全体の処理を実行する関数です。

ルールマスターの読み込み、RuleIdの入力受付、ルール検索、プロンプト作成、表示、保存確認までをまとめて行います。

---

## 自分の理解

このファイルは、BIM品質ルールを生成AIに渡すためのプロンプトを作る処理です。

重要なのは、生成AIに自由に回答させるのではなく、RuleIdに紐づくルール情報だけを参照させる形にしている点です。

これにより、AIの回答範囲を制限し、根拠のない回答や過度な自動判断を避けることができます。

現時点では、品質チェック結果CSVから自動で違反内容を取り込むのではなく、RuleIdを入力して、そのRuleIdのルール情報からプロンプトを作成する仕組みです。

将来的には、`check_bim_quality.py` のチェック結果CSVに含まれるRuleIdや対象要素情報を使って、違反内容に応じた生成AI向け構造化コンテキストを自動生成する形に拡張できます。

現時点ではプロンプト文をtxtとして出力していますが、将来的にはRuleId、違反内容、重大度、品質スコア、修正優先度、FixGuideなどをJSONまたはMarkdown形式で構造化し、生成AIに渡す情報を制御する形へ拡張します。

この処理は、本格的なRAGやローカルLLM連携の前段階として位置づけられます。

---

# まとめ

今回確認した4つのPythonファイルは、BIMデータ品質チェックPoCの中でそれぞれ次の役割を持っています。

## convert_revit_schedule.py

Revit書き出しTXTを品質チェック用CSVへ変換する前処理です。

Revit由来データをPython処理パイプラインに接続する入口になります。

---

## check_bim_quality.py

品質チェック用CSVを読み込み、RuleId付きの品質チェック結果を出力する中心処理です。

必須項目未入力、分類コード未入力、ファミリ命名規則違反などを検出します。

---

## ruleid_lookup_demo.py

RuleIdからBIM品質ルールの内容を検索・表示する処理です。

チェック結果CSVに含まれるRuleIdを起点に、該当するルール内容、重大度、業務影響、AI活用時の影響、修正ガイドを確認できます。

---

## ruleid_prompt_generator_demo.py

RuleIdに紐づくルール情報から、生成AI向け構造化コンテキスト生成の前段階となるプロンプトを作成する処理です。

現時点ではtxt形式のプロンプト生成ですが、将来的にはJSONまたはMarkdown形式の構造化コンテキスト生成へ発展させます。

---

# PoC全体での位置づけ

この4つのPythonファイルを組み合わせることで、以下の流れを説明できるようになります。

```text
Revit書き出しTXT
↓
convert_revit_schedule.py
↓
品質チェック用CSV
↓
check_bim_quality.py
↓
RuleId付き品質チェック結果CSV
↓
ruleid_lookup_demo.py
↓
RuleIdに紐づくルール確認
↓
ruleid_prompt_generator_demo.py
↓
生成AI向け構造化コンテキスト生成の前段階
```

この流れにより、BIMデータの前処理、品質チェック、ルール参照、生成AI活用前処理までを一連のPoCとして説明できます。

現時点では試作コードを `08_python` と `06_ai_demo` に配置していますが、今後は処理を整理し、`src` 配下へ段階的に移行する予定です。

---

# 今後の拡張予定

今後は、以下の方向へ拡張します。

- `convert_revit_schedule.py` のv0.2化
- `check_bim_quality.py` のv0.2化
- `src/convert_revit_schedule.py` への整理
- `src/check_bim_quality.py` への整理
- `src/clean_bim_data.py` の実装
- `src/calculate_quality_metrics.py` の実装
- `src/create_bim_features.py` による特徴量設計
- `src/train_fix_priority_model.py` による修正優先度分類プロトタイプ
- `src/generate_ai_context.py` による生成AI向け構造化コンテキスト生成
- `tests/test_quality_rules.py` による最小テスト追加

今後も、AIモデルの精度そのものを追求するのではなく、建築BIMデータをAI・機械学習・生成AIが扱える形へ整備するデータ処理パイプラインを重視します。