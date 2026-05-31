# このファイルの目的：
# Revitから書き出した集計表TXTをPython/pandasで読み込み、
# 表データとして取得できるかを確認するためのテスト用スクリプト。
#
# 主な処理フロー：
# 1. プロジェクトの基準フォルダを設定する
# 2. 読み込み対象のRevit書き出しTXTファイルのパスを指定する
# 3. pandasでタブ区切りTXTを読み込む
# 4. 読み込んだデータの先頭行を表示する
# 5. 読み込んだデータの行数・列数を表示する
# 6. Revit由来TXTをPythonで処理できるか確認する

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_TXT = BASE_DIR / "03_input_csv" / "door_schedule_SD_export_test_v001.txt"

df = pd.read_csv(
    INPUT_TXT,
    sep="\t",
    header=None,
    encoding="utf-8-sig"
)

print(df.head())
print(df.shape)