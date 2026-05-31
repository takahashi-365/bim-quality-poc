# このファイルの目的：
# Revitから書き出した集計表TXTをPython/pandasで読み込み、
# 品質チェックに使いやすいCSV形式へ変換するためのスクリプト。
#
# v0.2の主な改善点：
# 1. 出力ファイル名を v002 に変更
# 2. 元TXTの先頭にある非データ行を除外
# 3. ElementId が空欄の行を除外
# 4. 現時点の列マッピングが仮設定であることを明記
# 5. 変換前後の行数・列数を表示
#
# 注意：
# 現時点の列マッピングは仮設定。
# ElementId は Revit内部ElementId ではなく、建具表上の建具番号を仮IDとして使用している。
# FamilyName は Revitファミリ名ではなく、建具表上の種別記号 SD を仮格納している。
# TypeName は Revitタイプ名ではなく、設置場所・室名に近い列を仮格納している。

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_TXT = BASE_DIR / "03_input_csv" / "door_schedule_SD_export_test_v001.txt"
OUTPUT_CSV = BASE_DIR / "03_input_csv" / "door_schedule_converted_v002.csv"

MODEL_NAME = "BIM_Quality_Check_Sample_Model_R2024_v001"
CATEGORY = "Doors"


def read_revit_schedule_txt(input_path: Path) -> pd.DataFrame:
    """
    Revitから書き出したタブ区切りTXTを読み込む。

    header=None は、元TXTに正式な列名行がないため、
    列番号で読み込む指定。
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input TXT not found: {input_path}")

    return pd.read_csv(
        input_path,
        sep="\t",
        header=None,
        encoding="utf-8-sig",
    )


def convert_to_quality_check_csv(raw_df: pd.DataFrame, source_file_name: str) -> pd.DataFrame:
    """
    Revit書き出しTXTのデータを、品質チェック用CSVの列構成に変換する。

    現時点の仮マッピング：
    - Category: 固定値 Doors
    - ElementId: raw_df[1]
      - Revit内部ElementIdではなく、建具表上の建具番号を仮IDとして使用
    - FamilyName: raw_df[0]
      - Revitファミリ名ではなく、建具表上の種別記号 SD を仮格納
    - TypeName: raw_df[3]
      - Revitタイプ名ではなく、設置場所・室名に近い列を仮格納
    - Level: 現時点では空欄
    - BIM_ClassificationCode: 現時点では空欄
    - BIM_ModelRole: 現時点では空欄
    - BIM_Zone: 現時点では空欄
    - SourceFile: 入力TXTファイル名
    - ModelName: 固定値
    """

    converted_df = pd.DataFrame(
        {
            "Category": CATEGORY,
            "ElementId": raw_df[1],
            "FamilyName": raw_df[0],
            "TypeName": raw_df[3],
            "Level": "",
            "BIM_ClassificationCode": "",
            "BIM_ModelRole": "",
            "BIM_Zone": "",
            "SourceFile": source_file_name,
            "ModelName": MODEL_NAME,
        }
    )

    converted_df = converted_df.fillna("")

    # 先頭の非データ行や空行を除外する。
    # 今回の元TXTでは、先頭行に SD のみが入り、ElementId が空欄のため除外対象とする。
    before_rows = len(converted_df)
    converted_df = converted_df[converted_df["ElementId"].astype(str).str.strip() != ""].copy()
    after_rows = len(converted_df)

    print(f"Removed non-data rows: {before_rows - after_rows}")

    return converted_df


def save_csv(df: pd.DataFrame, output_path: Path) -> None:
    """変換後CSVを出力する。"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")


def main() -> None:
    print("Revit schedule conversion started.")
    print(f"Input file: {INPUT_TXT}")

    raw_df = read_revit_schedule_txt(INPUT_TXT)

    print(f"Raw data shape: {raw_df.shape}")

    converted_df = convert_to_quality_check_csv(
        raw_df=raw_df,
        source_file_name=INPUT_TXT.name,
    )

    save_csv(converted_df, OUTPUT_CSV)

    print(f"Converted data shape: {converted_df.shape}")
    print(f"Output file: {OUTPUT_CSV}")
    print("Revit schedule conversion completed.")


if __name__ == "__main__":
    main()