# このファイルの目的：
# Revitから書き出した集計表TXTをPython/pandasで読み込み、
# 品質チェックに使いやすいCSV形式へ変換するための試作スクリプト。
#
# 主な処理フロー：
# 1. プロジェクトの基準フォルダを設定する
# 2. 入力TXTファイルと出力CSVファイルのパスを指定する
# 3. Revit書き出しTXTをタブ区切りデータとして読み込む
# 4. 必要な列だけを抽出する
# 5. 品質チェック用の列名に変換する
# 6. 空欄を扱いやすい形に整える
# 7. 品質チェック用CSVとして出力する

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_TXT = BASE_DIR / "03_input_csv" / "door_schedule_SD_export_test_v001.txt"
OUTPUT_CSV = BASE_DIR / "03_input_csv" / "door_schedule_converted_v001.csv"


def main() -> None:
    print("Revit schedule conversion started.")
    print(f"Input file: {INPUT_TXT}")

    if not INPUT_TXT.exists():
        raise FileNotFoundError(f"Input TXT not found: {INPUT_TXT}")

    # Revitから書き出したタブ区切りTXTを読み込む
    # header=None は、元TXTに列名行がないため、列番号で読み込む指定
    raw_df = pd.read_csv(
        INPUT_TXT,
        sep="\t",
        header=None,
        encoding="utf-8-sig"
    )

    print(f"Raw data shape: {raw_df.shape}")

    # 現時点では、ドア集計表TXTの列番号を仮に割り当てる
    # 必要に応じて、後で列番号と列名の対応を見直す
    converted_df = pd.DataFrame({
        "Category": "Doors",
        "ElementId": raw_df[1],
        "FamilyName": raw_df[0],
        "TypeName": raw_df[3],
        "Level": "",
        "BIM_ClassificationCode": "",
        "BIM_ModelRole": "",
        "BIM_Zone": "",
        "SourceFile": INPUT_TXT.name,
        "ModelName": "BIM_Quality_Check_Sample_Model_R2024_v001"
    })

    # NaNを空文字に変換する
    converted_df = converted_df.fillna("")

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    converted_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    print(f"Converted data shape: {converted_df.shape}")
    print(f"Output file: {OUTPUT_CSV}")
    print("Revit schedule conversion completed.")


if __name__ == "__main__":
    main()