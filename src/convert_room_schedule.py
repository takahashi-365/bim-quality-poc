from pathlib import Path
import pandas as pd


INPUT_PATH = Path("03_input_csv/room_schedule_export_test_v001.txt")
OUTPUT_PATH = Path("03_input_csv/room_schedule_converted_v001.csv")


def convert_room_schedule(input_path: Path = INPUT_PATH, output_path: Path = OUTPUT_PATH) -> pd.DataFrame:
    """Convert Revit Room Schedule TXT export to CSV for Phase 3B."""

    df = pd.read_csv(
        input_path,
        sep="\t",
        quotechar='"',
        header=0,
        dtype=str,
        encoding="utf-8-sig",
        engine="python",
    )

    # Revit schedule export includes grouped column headers as the first data row.
    # In this Room schedule, that row has empty Room name and Area values.
    df = df.fillna("")

    if "名前" not in df.columns or "面積" not in df.columns:
        raise ValueError("Required columns are missing: 名前 and/or 面積")

    # Remove grouped header / blank / group summary rows.
    df = df[
        ~(
            df["名前"].astype(str).str.strip().eq("")
            & df["面積"].astype(str).str.strip().eq("")
        )
    ].copy()

    # Remove rows where Level is a group heading and Room name / Area are blank.
    df = df.reset_index(drop=True)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    return df


if __name__ == "__main__":
    converted = convert_room_schedule()
    print(f"Converted rows: {len(converted)}")
    print(f"Output: {OUTPUT_PATH}")
    print(converted.head().to_string(index=False))