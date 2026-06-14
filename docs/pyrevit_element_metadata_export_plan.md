# 第3段階C：pyRevitでElementId / UniqueId取得PoC 計画

## 目的

第3段階Cでは、pyRevitを使ってRevitモデル内の要素から `ElementId` / `UniqueId` などの基本メタデータを取得し、既存の `BIM Data Quality & AI Readiness Assessment PoC` に接続できる可能性を検証する。

現在のPoCでは、Revit集計表TXTを書き出してPythonで処理している。
第3段階Cでは、Revitモデルから直接データを取得する入口を作る。

目的は、Revitモデルを自動修正することではない。
まずは、選択要素のメタデータを安全に取得し、CSVとして出力できることを確認する。

---

## 位置づけ

本作業は、新規PoCではなく、既存の `BIM Data Quality & AI Readiness Assessment PoC` の第3段階拡張として実施する。

第3段階Bまでの流れ：

```text
Revit Schedule TXT
↓
CSV変換
↓
品質チェック
↓
AI Readiness Score
↓
AI Context
↓
Fix Guide
```

第3段階Cで追加する検証：

```text
Revitモデル上で要素選択
↓
pyRevit実行
↓
ElementId / UniqueId / Category / FamilyName / TypeName 取得
↓
CSV出力
↓
既存PoCの入力データとの接続可能性を確認
```

---

## 第3段階Cでやること

* pyRevitの実行環境を確認する
* Revit上で選択した要素のメタデータを取得する
* 取得対象は最初は1要素または複数選択要素に限定する
* 選択要素が0件の場合はCSV出力せず、安全に処理を中断する
* `ElementId` と `UniqueId` を取得する
* `Category`、`FamilyName`、`TypeName` を取得する
* 必要に応じて `Name`、`LevelName`、`RoomName`、`RoomNumber` を候補として扱う
* `RoomName` / `RoomNumber` は初期MVPでは必須項目にしない
* 取得できない項目は空欄として出力する
* 取得結果をCSVとして出力する
* pyRevit側ではpandasを前提にせず、標準ライブラリ `csv` を使う
* CSVの文字コード方針を確認する
* 出力CSVを既存PoCのCSV列構成と比較する
* 既存の品質チェックパイプラインに接続できるかを整理する
* docsに制約と今後の接続方針を記録する

---

## 第3段階Cでやらないこと

```text
Revitモデルの自動修正
要素パラメータの自動書き換え
設計判断・施工判断
モデル全体の大規模スキャン
全カテゴリ対応
本格Revit API連携
Revitアドイン製品化
リアルタイム品質チェック
クラウド連携
生成AI API連携
pyRevit上でのpandas前提処理
```

初期MVPでは、**選択要素のメタデータを安全にCSV出力すること**に限定する。

---

## 取得対象項目

初期MVPで取得する項目：

```text
ElementId
UniqueId
Category
FamilyName
TypeName
```

取得できる場合の追加候補：

```text
Name
LevelName
RoomName
RoomNumber
```

ただし、`FamilyName`、`TypeName`、`LevelName`、`RoomName`、`RoomNumber` は、要素カテゴリやモデル構成によって取得できない場合がある。

取得できない場合は、無理に補完せず、空欄または `None` として出力し、制約として記録する。

---

## ElementId / UniqueId の使い分け

`ElementId` は、Revitモデル内で要素を識別するために利用する。

ただし、`ElementId` はモデルの編集、要素の削除・再作成、モデルの作り直しなどにより変わる可能性がある。

そのため、長期的な照合や、将来的なAI Context / RAG用メタデータでは、`UniqueId` の利用を検討する。

初期MVPでは、`ElementId` と `UniqueId` の両方をCSVに出力する。

目的：

```text
既存PoCのElementId列との接続可能性を確認する
第2段階までの仮ElementIdとの違いを整理する
UniqueIdを将来的な安定識別子として使えるか確認する
AI ContextやFix Guideに含めるメタデータ候補として整理する
```

注意点：

```text
ElementIdはRevitモデル内での要素識別に利用する。
ただし、モデルの編集や再作成により変わる可能性があるため、長期的な照合にはUniqueIdの利用を検討する。
初期MVPではElementIdとUniqueIdの両方をCSVに出力し、既存PoCのElementId列との接続可能性を確認する。
```

---

## RoomName / RoomNumber の扱い

`RoomName` / `RoomNumber` は、初期MVPでは必須項目にしない。

理由：

* 選択要素がRoomの場合は取得しやすい可能性がある
* Doorなどの要素から関連Roomを取得する場合、Revit API上の取得方法がモデル構成に依存する
* ドアがどのRoomに属するかは、モデルの作り方や配置条件によって扱いが変わる
* 初期MVPの目的は、ElementId / UniqueId / Category / FamilyName / TypeNameの取得確認である

方針：

```text
RoomName / RoomNumberは、選択要素がRoomの場合、または要素から関連Roomを取得できる場合のみ候補とする。
初期MVPでは必須項目にしない。
取得できない場合は空欄として扱い、制約として記録する。
```

---

## FamilyName / TypeNameの扱い

`FamilyName` / `TypeName` は、要素カテゴリによって取得方法が異なる可能性がある。

方針：

```text
DoorなどのFamilyInstanceでは、FamilyName / TypeNameを取得しやすい
Roomなど一部カテゴリでは、FamilyNameが対象外または空欄になる可能性がある
取得できない場合は空欄としてCSV出力する
カテゴリごとの差異はdocsに制約として記録する
```

初期MVPでは、すべてのカテゴリで同じ項目が取得できることを前提にしない。

---

## 選択要素が0件の場合の扱い

pyRevit実行時に、Revit上で要素が選択されていない可能性がある。

その場合は、CSV出力を行わず、処理を安全に中断する。

方針：

```text
選択要素が0件の場合は、CSV出力を行わない
ユーザーに要素選択が必要であることを通知する
エラーとして強制終了するのではなく、安全に処理を中断する
空CSVは原則として出力しない
```

理由：

* 空CSVを出すと、後続のPoC側処理で誤って入力として扱う可能性がある
* 初期MVPでは、選択要素のメタデータ取得確認を目的とするため、対象要素がない場合は処理対象外とする
* ユーザーに「要素を選択してから実行する」必要があることを明確にする

---

## pyRevitスクリプトの配置方針

GitHub上では、pyRevit用スクリプトを以下に保管する。

```text
pyrevit_scripts/export_selected_element_metadata.py
```

ただし、これはGitHub上の保管場所であり、実際にpyRevitボタンとして実行する配置とは異なる。

実際にpyRevitボタンとして実行する場合は、pyRevitの拡張フォルダ構成に合わせる必要がある。

例：

```text
extension
↓
tab
↓
panel
↓
pushbutton
↓
script.py
```

方針：

```text
GitHub上では pyrevit_scripts/ にスクリプトを保管する
実際にpyRevitボタンとして実行する場合は、pyRevit extension / tab / panel / pushbutton の構成に配置する
初期MVPでは、GitHub上の保管構成とpyRevit実行環境の配置構成を分けて扱う
```

---

## pyRevit実行環境の制約

pyRevitスクリプトは、通常のPython実行環境ではなく、Revit / pyRevit上で実行される。

そのため、以下の制約を考慮する。

```text
pyRevitスクリプトはRevit起動環境でのみ実行できる
通常のpytestではRevit API呼び出し部分を直接検証しにくい
pyRevitの実行環境により、IronPython / CPython の違いがある可能性がある
通常のPoC側Python環境と異なり、pandasなどの外部ライブラリを前提にしない
初期MVPでは、Revit APIで取得した値を標準ライブラリ csv で出力する
pandas処理は、出力CSVをPoC側で読み込んだ後に行う
```

---

## CSV出力方針

初期CSV列は以下にする。

```text
ElementId,UniqueId,Category,FamilyName,TypeName
```

追加候補：

```text
Name,LevelName,RoomName,RoomNumber
```

初期MVPでは、`RoomName` / `RoomNumber` は必須項目にしない。

取得できない列を無理に埋めない。
取得できない場合は空欄または `None` として出力する。

選択要素が0件の場合は、CSV出力を行わない。
その場合、ユーザーに要素選択が必要であることを通知し、処理を安全に中断する。

---

## CSV文字コード方針

Revit要素名やタイプ名に日本語が含まれる可能性があるため、CSV出力時の文字コードに注意する。

初期MVPでは、以下を候補とする。

```text
UTF-8
UTF-8 with BOM
```

Excelで確認する場合に文字化けする可能性があるため、必要に応じて `UTF-8 with BOM` を採用する。

既存PoC側で文字コード方針がある場合は、それに合わせる。

---

## 出力先パスの扱い

pyRevitはRevit内で実行されるため、スクリプト実行時のカレントディレクトリがPoCリポジトリ直下とは限らない。

そのため、初期MVPでは以下の方針とする。

```text
pyRevit実行時の相対パスは環境依存になりやすい
初期MVPでは、出力先パスをスクリプト内で明示する
または、ユーザーが保存先を確認できる形にする
GitHub公開用のサンプルCSVは、実行後に 03_input_csv/ へ配置する
```

想定保存先：

```text
03_input_csv/pyrevit_element_metadata_sample_v001.csv
```

ただし、Revit実行環境から直接この場所へ出力できない場合は、一時出力後に手動で配置してもよい。

---

## 想定成果物

### docs

```text
docs/pyrevit_element_metadata_export_plan.md
docs/pyrevit_element_metadata_mapping.md
docs/pyrevit_limitations.md
```

### pyRevit script

```text
pyrevit_scripts/export_selected_element_metadata.py
```

### sample output

```text
03_input_csv/pyrevit_element_metadata_sample_v001.csv
```

### optional output

```text
04_output_csv/pyrevit_metadata_connection_notes_v001.md
```

---

## 作業手順

## Step 1：現在のPoC状態を確認する

作業前に、Gitの状態を確認する。

```powershell
git status
```

作業ブランチを分ける場合は、以下のようにする。

```powershell
git checkout -b phase3c-pyrevit-element-metadata
```

mainでそのまま作業する場合でも、作業前に `git status` が clean であることを確認する。

---

## Step 2：pyRevit用フォルダを作成する

既存PoC内に、GitHub保管用のpyRevitスクリプト置き場を作る。

```text
pyrevit_scripts/
```

作成候補：

```powershell
mkdir pyrevit_scripts
```

作成予定ファイル：

```text
pyrevit_scripts/export_selected_element_metadata.py
```

注意：

```text
pyrevit_scripts/ はGitHub上の保管場所であり、実際のpyRevit実行配置とは別に扱う。
```

---

## Step 3：計画書を作成する

以下のdocsを作成する。

```text
docs/pyrevit_element_metadata_export_plan.md
```

記載内容：

```text
目的
対象範囲
取得項目
ElementId / UniqueId の使い分け
RoomName / RoomNumber の扱い
選択要素が0件の場合の扱い
やらないこと
pyRevit実行環境の制約
GitHub保管場所とpyRevit実行配置の違い
出力CSV形式
出力パス方針
既存PoCへの接続方針
制約
完了条件
```

---

## Step 4：最小スクリプトを作る

最初は、Revit上で選択した要素から以下だけを取得する。

```text
ElementId
UniqueId
Category
FamilyName
TypeName
```

初期スクリプトの役割：

```text
Revitで要素を選択
↓
pyRevitボタン実行
↓
選択要素の情報を取得
↓
標準ライブラリ csv でCSVに書き出す
```

選択要素が0件の場合は、CSV出力を行わず、ユーザーに要素選択が必要であることを通知して処理を中断する。

pyRevit側では、pandasを使わない。

---

## Step 5：CSV出力形式を決める

初期CSV列は以下にする。

```text
ElementId,UniqueId,Category,FamilyName,TypeName
```

追加候補：

```text
Name,LevelName,RoomName,RoomNumber
```

ただし、`RoomName` / `RoomNumber` は初期MVPでは必須項目にしない。

取得できない列を無理に埋めない。
取得できない場合は空欄または `None` として出力する。

---

## Step 6：Revit上でテスト実行する

Revitで以下を試す。

```text
1. ドアを1つ選択する
2. pyRevitスクリプトを実行する
3. CSVが出力されるか確認する
4. ElementId / UniqueId / Category / FamilyName / TypeName が入っているか確認する
```

次に、複数要素選択を試す。

```text
1. ドアを複数選択する
2. pyRevitスクリプトを実行する
3. 複数行のCSVが出力されるか確認する
```

選択要素0件のケースも確認する。

```text
1. 要素を選択していない状態でpyRevitスクリプトを実行する
2. CSVが出力されないことを確認する
3. ユーザーに要素選択が必要であることが通知されるか確認する
4. 処理が安全に中断されるか確認する
```

必要に応じて、Room要素でも確認する。

```text
1. Roomを選択する
2. pyRevitスクリプトを実行する
3. FamilyName / TypeNameが取得できるか確認する
4. RoomName / RoomNumberを取得できるか確認する
5. 取得できない場合は空欄として扱えるか確認する
```

---

## Step 7：CSV文字化けを確認する

日本語のカテゴリ名、ファミリ名、タイプ名が含まれる場合、ExcelまたはVS CodeでCSVを開き、文字化けがないか確認する。

確認結果に応じて、以下を判断する。

```text
UTF-8で問題ないか
UTF-8 with BOMにする必要があるか
既存PoC側のCSV処理と文字コードを合わせる必要があるか
```

---

## Step 8：Door / Roomとの接続可能性を確認する

第2段階・第3段階Bの既存CSVと比較する。

確認観点：

```text
既存PoCのElementId列と接続できるか
UniqueIdを将来の安定識別子として使えるか
Category列としてDoor / Roomを扱えるか
FamilyName / TypeNameを品質チェックに使えるか
Roomカテゴリでも利用できるか
RoomではFamilyName / TypeNameが空欄になる可能性があるか
RoomName / RoomNumberは必須ではなく候補として扱えるか
```

---

## Step 9：制約をdocsに記録する

以下のような制約を記録する。

保存先候補：

```text
docs/pyrevit_limitations.md
```

記録する制約候補：

```text
pyRevitスクリプトはRevit起動環境でのみ実行できる
通常のpytestではRevit API呼び出し部分を直接検証しにくい
GitHub上のpyrevit_scripts/配置と、実際のpyRevit extension配置は異なる可能性がある
外部Pythonライブラリの利用は制限される可能性がある
pyRevit側ではpandasを前提にせず、標準ライブラリcsvで出力する
選択要素が0件の場合はCSV出力せず、処理を中断する
ElementIdはモデル内識別に使えるが、長期的な照合にはUniqueIdを検討する
FamilyName / TypeNameはカテゴリによって取得できない場合がある
RoomName / RoomNumberは選択要素やモデル構成によって取得できない場合がある
RoomName / RoomNumberは初期MVPでは必須項目にしない
Room情報は選択要素のカテゴリやモデル構成によって取得できない場合がある
リンクモデル内要素は初期MVP対象外
相対パス出力は環境依存になりやすい
CSV文字コードはUTF-8またはUTF-8 with BOMを検討する
```

---

## Step 10：既存PoCへの接続方針を整理する

以下を整理する。

保存先候補：

```text
docs/pyrevit_element_metadata_mapping.md
```

整理する内容：

```text
pyRevit出力CSVを 03_input_csv/ に置けるか
既存CSV変換処理をスキップできるか
既存品質チェックに必要な列を満たせるか
Door / RoomのCategory判定に使えるか
ElementId / UniqueIdをAI Contextへ含められるか
UniqueIdを将来的な安定識別子として使えるか
第2段階までの仮ElementIdとどう区別するか
RoomName / RoomNumberを初期MVPでは必須にしない場合の扱い
選択要素が0件の場合の出力方針
```

---

## Step 11：pytest対象を整理する

pyRevitスクリプト自体はRevit環境依存のため、通常のpytestでは直接テストしにくい。

そのため、pytestでは以下を対象にする。

```text
pyRevit出力CSVを読み込めるか
必要列が存在するか
ElementId / UniqueId が空でないか
Category列が存在するか
FamilyName / TypeName列が存在するか
RoomName / RoomNumberがなくてもテストが成立するか
既存PoC用の入力形式に変換できるか
```

候補ファイル：

```text
tests/test_pyrevit_metadata_csv.py
```

Revit API呼び出しそのものは、Revit上での手動実行確認として扱う。

選択要素0件時の通知や処理中断は、Revit上での手動確認対象とする。

---

## Step 12：GitHub公開方針を確認する

GitHubに公開してよいもの：

```text
pyrevit_scripts/export_selected_element_metadata.py
docs/pyrevit_element_metadata_export_plan.md
docs/pyrevit_element_metadata_mapping.md
docs/pyrevit_limitations.md
03_input_csv/pyrevit_element_metadata_sample_v001.csv
tests/test_pyrevit_metadata_csv.py
```

公開しないもの：

```text
実案件Revitモデル
社外秘モデル
個人情報を含むモデル情報
大量の実モデル由来パラメータ
ローカル環境固有の設定ファイル
pyRevitローカル設定
Revitユーザー環境固有パス
```

---

## Step 13：README反映判断

初期MVP完了直後は、READMEを大きく更新しない。

まずはdocsに記録する。

READMEに反映する場合は、以下のように小さく追記する。

```text
pyRevitを用いて、Revitモデル上の選択要素からElementId / UniqueId / Category / FamilyName / TypeNameを取得し、既存のBIMデータ品質チェックPoCへ接続するための小規模検証を行っています。
```

Portfolio PDFの更新は、第3段階C単体では必須としない。

---

## 完了条件

第3段階Cの完了条件は以下。

```text
pyRevit用スクリプトを作成した
GitHub上の保管場所とpyRevit実行配置の違いを整理した
Revit上で選択要素からElementIdを取得した
UniqueIdを取得した
ElementId / UniqueId の使い分けを整理した
Categoryを取得した
FamilyName / TypeNameを取得した
RoomName / RoomNumberは初期MVPでは必須にしないことを整理した
選択要素が0件の場合はCSV出力せず、安全に処理を中断できることを確認した
取得できない項目は空欄として扱った
標準ライブラリcsvでCSVとして出力した
CSV文字コードを確認した
出力CSVを03_input_csv/に保存した
既存PoCの入力形式との接続可能性を整理した
pyRevit実行環境の制約をdocsに記録した
GitHub公開対象と非公開対象を整理した
README反映要否を判断した
```

---

## 成功とみなす状態

以下の状態になれば、第3段階CのMVPとして成功とする。

```text
Revit上で要素選択
↓
pyRevit実行
↓
ElementId / UniqueId / Category / FamilyName / TypeName取得
↓
標準ライブラリcsvでCSV出力
↓
既存PoCへの接続可能性をdocsに整理
```

選択要素が0件の場合は、CSVを出力せず、処理を安全に中断できることも確認する。

この段階では、Revitモデル自動修正や全モデルスキャンは行わない。
重要なのは、Revit集計表TXTだけでなく、Revit API / pyRevit経由でモデル情報を取得できる入口を作ることである。

---

## 注意点

* pyRevitはRevit起動環境で実行する
* GitHub上の `pyrevit_scripts/` と実際のpyRevit実行配置は別に考える
* pyRevit側ではpandasを前提にしない
* 初期MVPでは標準ライブラリ `csv` を使う
* 選択要素が0件の場合はCSV出力せず、安全に中断する
* 相対パス出力は環境依存になりやすい
* CSV文字コードはUTF-8またはUTF-8 with BOMを検討する
* ElementIdはモデル内識別に使い、長期的な照合にはUniqueIdを検討する
* FamilyName / TypeNameはカテゴリによって取得できない場合がある
* RoomName / RoomNumberは初期MVPでは必須項目にしない
* Room情報はカテゴリやモデル構成によって取得できない場合がある
* リンクモデル内要素は初期MVP対象外
* Revitモデル自動修正は行わない
* READMEやPDFをすぐに大きく更新しない

---

## 次段階への接続

第3段階Cが完了したら、以下へ接続する。

```text
第3段階D：RAG / Azure AI Search構成検討
```

第3段階Cにより、将来的にAI ContextやRAG用メタデータへ `ElementId` / `UniqueId` を含める検討がしやすくなる。
