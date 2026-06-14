# pyRevit Element Metadata Export 制約事項

## 目的

このドキュメントは、第3段階C「pyRevitでElementId / UniqueId取得PoC」における制約事項を整理する。

第3段階Cでは、pyRevitを使ってRevitモデル上の選択要素から基本メタデータを取得し、CSVとして出力できるかを検証した。

本作業の目的は、Revitモデルの自動修正ではない。

目的は、以下の情報を安全に取得し、既存の `BIM Data Quality & AI Readiness Assessment PoC` へ接続できる可能性を確認することである。

```text
ElementId
UniqueId
Category
FamilyName
TypeName
Name
LevelName
RoomName
RoomNumber
```

---

## 検証環境

今回の検証では、以下の環境でpyRevitを使用した。

```text
Revit: Revit 2024
pyRevit: pyRevit 6.4.0
OS: Windows
```

pyRevitはAutodesk公式アドオンではなく、サードパーティ製のRevit拡張ツールである。

そのため、業務PCや実務環境に導入する場合は、社内ルール、BIM管理方針、管理者権限、既存アドオンとの影響を確認する必要がある。

---

## GitHub保管場所とpyRevit実行配置の違い

GitHub上では、pyRevit用スクリプトを以下に保管する。

```text
pyrevit_scripts/export_selected_element_metadata.py
```

一方、pyRevitで実際にボタンとして実行するには、pyRevitのExtension構成に合わせて `script.py` として配置する必要がある。

今回の検証では、以下に配置した。

```text
C:\Users\PLS-39\AppData\Roaming\pyRevit\Extensions\BIMQuality.extension\BIM Quality.tab\Phase 3C.panel\Export Metadata.pushbutton\script.py
```

このため、GitHub保管用スクリプトを修正した場合は、pyRevit実行用の `script.py` に再コピーする必要がある。

---

## pyRevit実行環境の制約

pyRevitスクリプトは、通常のPython実行環境ではなく、Revit上のpyRevit実行環境で動作する。

そのため、以下の制約がある。

```text
Revitを起動している必要がある
Revitモデルを開いている必要がある
通常のpytestではRevit API呼び出し部分を直接検証しにくい
PowerShell上で pyrevit CLI が常に使えるとは限らない
pyRevitのバージョンによりPython実行環境の挙動が異なる可能性がある
```

今回の検証では、PowerShell上で当初 `pyrevit` コマンドは認識されなかった。

そのため、Revit上のpyRevitタブからExtensionを読み込み、リボンボタンとしてスクリプトを実行した。

---

## 文字コードに関する制約

スクリプト内に日本語コメントや日本語メッセージを含める場合、ファイル先頭に文字コード宣言が必要だった。

今回、初回実行時に以下のようなエラーが発生した。

```text
Non-ASCII character ... but no encoding declared
```

このため、スクリプト先頭に以下を追加した。

```python
# -*- coding: utf-8 -*-
```

CSV出力は、日本語のカテゴリ名、ファミリ名、タイプ名をExcel等で確認しやすくするため、UTF-8 with BOMで出力した。

```python
codecs.open(output_path, "w", "utf-8-sig")
```

---

## 選択要素0件時の制約

Revit上で要素を選択していない状態でスクリプトを実行した場合は、CSVを出力しない。

今回の検証では、0件選択時に以下の動作を確認した。

```text
要素が選択されていないことを通知する
CSVを出力しない
処理を安全に中断する
```

空CSVを出力しない理由は、後続のPoC処理で誤って入力データとして扱うことを避けるためである。

---

## ElementId / UniqueId の制約

`ElementId` は、Revitモデル内で要素を識別するために利用できる。

ただし、以下のような場合に変わる可能性がある。

```text
要素の削除
要素の再作成
モデルの作り直し
別モデルへの移行
```

そのため、長期的な照合や、将来的なAI Context / RAG用メタデータでは、`UniqueId` の利用を検討する。

初期MVPでは、`ElementId` と `UniqueId` の両方をCSVに出力する。

---

## FamilyName / TypeName の制約

`FamilyName` / `TypeName` は、要素カテゴリによって取得方法や取得可否が異なる可能性がある。

DoorなどのFamilyInstanceでは、今回の検証で以下を取得できた。

```text
Category
FamilyName
TypeName
Name
LevelName
```

一方、Roomなどのカテゴリでは、FamilyNameが対象外または空欄になる可能性がある。

初期MVPでは、すべてのカテゴリで同じ項目が取得できることを前提にしない。

取得できない項目は空欄として扱う。

---

## RoomName / RoomNumber の制約

`RoomName` / `RoomNumber` は、初期MVPでは必須項目にしない。

Doorなどの要素から関連Roomを取得するには、Revit API上で追加の処理が必要であり、モデル構成やドアの配置条件にも依存する。

今回の初期実装では、一度Doorの `Name` が `RoomName` に入る状態になった。

これは実際の部屋名ではなく、Doorのタイプ名相当の値であり、誤解を招くため修正した。

現在の方針は以下である。

```text
Roomカテゴリの場合のみ RoomName / RoomNumber を取得する
DoorなどRoom以外のカテゴリでは RoomName / RoomNumber は空欄にする
Doorから関連Roomを推定しない
```

---

## リンクモデルの制約

初期MVPでは、リンクモデル内の要素取得は対象外とする。

対象は、現在開いているRevitモデル上で直接選択できる要素に限定する。

リンクモデル内要素の扱いは、将来の拡張検討とする。

---

## 出力パスの制約

pyRevitはRevit内で実行されるため、スクリプト実行時のカレントディレクトリがPoCリポジトリ直下とは限らない。

そのため、今回の初期MVPでは、CSVをいったんデスクトップに出力した。

```text
C:\Users\PLS-39\Desktop\pyrevit_element_metadata_sample_v001.csv
```

その後、GitHub公開用のサンプルとして、以下へ手動コピーした。

```text
03_input_csv/pyrevit_element_metadata_sample_v001.csv
```

---

## 自動修正は行わない

第3段階Cでは、Revitモデルの自動修正は行わない。

対象外とする内容は以下である。

```text
Revitモデルの自動修正
要素パラメータの自動書き換え
設計判断
施工判断
全モデルスキャン
リアルタイム品質チェック
クラウド連携
生成AI API連携
```

---

## 今回確認できたこと

今回の検証では、以下を確認できた。

```text
pyRevitをRevit 2024に導入できた
BIM Qualityタブを作成できた
Export Metadataボタンを作成できた
選択要素0件時にCSVを出力せず安全に中断できた
Door 1件からCSVを出力できた
Door複数件からCSVを出力できた
ElementIdを取得できた
UniqueIdを取得できた
Categoryを取得できた
FamilyNameを取得できた
TypeNameを取得できた
LevelNameを取得できた
日本語を含むCSVをUTF-8 with BOMで確認できた
DoorではRoomName / RoomNumberを空欄にできた
```

---

## 今後の課題

今後の課題は以下である。

```text
Room要素を選択した場合のRoomName / RoomNumber取得確認
複数カテゴリでのFamilyName / TypeName取得可否確認
pyRevit出力CSVを既存品質チェックパイプラインへ接続する変換方針の検討
ElementId / UniqueId をAI Contextへ含める方針の検討
Revitモデル由来データを公開用サンプルとして扱う場合の匿名化・情報管理
```
