from pathlib import Path
import re

import pandas as pd


INPUT_PATH = Path("03_input_csv/room_schedule_converted_v001.csv")
OUTPUT_PATH = Path("03_input_csv/cleaned_room_data_v001.csv")


def clean_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def parse_area(value: object) -> float | None:
    text = clean_text(value)

    if text == "":
        return None

    match = re.search(r"[-+]?\d+(?:\.\d+)?", text)

    if not match:
        return None

    return float(match.group(0))


def build_element_id(level: str, room_number: str, room_name: str, index: int) -> str:
    """Build unique temporary ElementId for Room MVP.

    Room Schedule TXT does not include Revit internal ElementId / UniqueId.
    Therefore, Phase 3B uses a temporary PoC ElementId.

    A sequential suffix is always added because the Room Schedule may contain
    multiple rows for the same Level + RoomNumber or Level + RoomName.
    """

    sequence = f"{index + 1:04d}"

    if level and room_number:
        return f"{level}-{room_number}-{sequence}"

    if level and room_name:
        return f"{level}-{room_name}-{sequence}"

    return f"Room-{sequence}"


def clean_room_data(
    input_path: Path = INPUT_PATH,
    output_path: Path = OUTPUT_PATH,
) -> pd.DataFrame:
    df = pd.read_csv(input_path, dtype=str, encoding="utf-8-sig").fillna("")

    required_columns = ["レベル", "名前", "面積"]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Required column is missing: {column}")

    cleaned_rows = []

    for index, row in df.iterrows():
        level = clean_text(row.get("レベル", ""))
        room_name = clean_text(row.get("名前", ""))
        room_number = clean_text(row.get("仕上表 整列番号", ""))
        area_raw = clean_text(row.get("面積", ""))

        cleaned_rows.append(
            {
                "ElementId": build_element_id(level, room_number, room_name, index),
                "Category": "Room",
                "Level": level,
                "RoomName": room_name,
                "RoomNumber": room_number,
                "RoomAlias": clean_text(row.get("仕上表 別名(室名)", "")),
                "RoomGroupName": clean_text(row.get("仕上表 グループ名", "")),
                "RoomGroupNumber": clean_text(row.get("仕上表 グループ番号*", "")),
                "AreaRaw": area_raw,
                "Area": parse_area(area_raw),
                "CH": clean_text(row.get("CH", "")),
                "FloorFinish": clean_text(row.get("Unnamed: 18", "")),
                "WallFinish": clean_text(row.get("Unnamed: 23", "")),
                "CeilingFinish": clean_text(row.get("Unnamed: 26", "")),
                "Notes": clean_text(row.get("備考", "")),
            }
        )

    cleaned = pd.DataFrame(cleaned_rows)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(output_path, index=False, encoding="utf-8-sig")

    return cleaned


if __name__ == "__main__":
    cleaned_df = clean_room_data()
    print(f"Cleaned rows: {len(cleaned_df)}")
    print(f"Unique ElementIds: {cleaned_df['ElementId'].nunique()}")
    print(f"Output: {OUTPUT_PATH}")
    print(cleaned_df.head().to_string(index=False))