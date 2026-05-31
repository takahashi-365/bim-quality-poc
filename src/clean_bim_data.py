# このファイルの目的：
# Revit由来の品質チェック用CSVを読み込み、
# 品質チェック・品質メトリクス作成・特徴量設計に使いやすい形へ整える。
#
# 主な処理：
# 1. 入力CSVを読み込む
# 2. 必要な列が存在するか確認する
# 3. 不足列があれば空列として追加する
# 4. 列順を標準化する
# 5. 文字列の前後スペースを削除する
# 6. NaNを空文字へ統一する
# 7. ElementIdが空欄の行を除外する
# 8. 重複行を除外する
# 9. クレンジング済みCSVを出力する

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_CSV = BASE_DIR / "03_input_csv" / "door_schedule_converted_v002.csv"
OUTPUT_CSV = BASE_DIR / "03_input_csv" / "cleaned_bim_data_v001.csv"


STANDARD_COLUMNS = [
    "Category",
    "ElementId",
    "FamilyName",
    "TypeName",
    "Level",
    "BIM_ClassificationCode",
    "BIM_ModelRole",
    "BIM_Zone",
    "SourceFile",
    "ModelName",
]


def read_input_csv(input_path: Path) -> pd.DataFrame:
    """入力CSVを読み込む。"""
    if not input_path.exists():
        raise FileNotFoundError(f"Input CSV not found: {input_path}")

    return pd.read_csv(input_path, encoding="utf-8-sig")


def add_missing_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    必要な列が存在しない場合、空列として追加する。
    これにより、後続の品質チェック処理で列不足エラーを防ぐ。
    """
    for column in STANDARD_COLUMNS:
        if column not in df.columns:
            df[column] = ""

    return df


def standardize_column_order(df: pd.DataFrame) -> pd.DataFrame:
    """列順を標準列順にそろえる。"""
    return df[STANDARD_COLUMNS].copy()


def clean_text_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    NaNを空文字に統一し、文字列の前後スペースを削除する。
    """
    df = df.fillna("")

    for column in df.columns:
        df[column] = df[column].astype(str).str.strip()

    return df


def remove_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    ElementIdが空欄の行を除外する。
    ElementIdは現時点ではRevit内部ElementIdではなく、
    建具表上の建具番号を仮IDとして使用している。
    """
    before_rows = len(df)

    df = df[df["ElementId"].astype(str).str.strip() != ""].copy()

    after_rows = len(df)
    print(f"Removed rows with blank ElementId: {before_rows - after_rows}")

    return df


def remove_duplicate_rows(df: pd.DataFrame) -> pd.DataFrame:
    """完全一致の重複行を除外する。"""
    before_rows = len(df)

    df = df.drop_duplicates().copy()

    after_rows = len(df)
    print(f"Removed duplicate rows: {before_rows - after_rows}")

    return df


def save_output_csv(df: pd.DataFrame, output_path: Path) -> None:
    """クレンジング済みCSVを出力する。"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")


def main() -> None:
    print("BIM data cleaning started.")
    print(f"Input file: {INPUT_CSV}")

    df = read_input_csv(INPUT_CSV)

    print(f"Input data shape: {df.shape}")

    df = add_missing_columns(df)
    df = standardize_column_order(df)
    df = clean_text_values(df)
    df = remove_invalid_rows(df)
    df = remove_duplicate_rows(df)

    save_output_csv(df, OUTPUT_CSV)

    print(f"Cleaned data shape: {df.shape}")
    print(f"Output file: {OUTPUT_CSV}")
    print("BIM data cleaning completed.")


if __name__ == "__main__":
    main()