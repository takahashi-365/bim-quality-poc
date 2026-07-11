# Phase 1 Empty Source File Cleanup

## 対象

- `src/convert_revit_schedule.py`
- `src/utils.py`

## 修正前

両ファイルとも0バイトであり、実行可能な本番コードは存在しなかった。

### convert_revit_schedule.py

過去の試作コードは`08_python/convert_revit_schedule.py`に存在するが、
`src/convert_revit_schedule.py`への正式移行は行われていなかった。

現在のGit管理対象パイプラインは、
整形済みの`cleaned_bim_data_v001.csv`を入力起点としている。

### utils.py

0バイトであり、現在の本番コードおよびテストからimportされていなかった。

## 対応

- 空の`src/convert_revit_schedule.py`を削除
- 空の`src/utils.py`を削除
- 現行文書に残る参照箇所を調査
- 過去資料およびbaseline記録は履歴として維持

## 方針

Revit書き出しデータの変換処理を将来正式実装する場合は、
列マッピング仕様を確定したうえで`src`配下へ新規実装する。

共通処理が複数の本番モジュールで必要になった場合に限り、
`utils.py`または用途別の共通モジュールを新規作成する。
