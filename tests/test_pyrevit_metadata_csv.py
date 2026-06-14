from pathlib import Path
import csv


PYREVIT_METADATA_CSV = Path("03_input_csv/pyrevit_element_metadata_sample_v001.csv")


REQUIRED_COLUMNS = [
    "ElementId",
    "UniqueId",
    "Category",
    "FamilyName",
    "TypeName",
    "Name",
    "LevelName",
    "RoomName",
    "RoomNumber",
]


def read_csv_rows(path):
    with path.open("r", encoding="utf-8-sig", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        return reader.fieldnames, list(reader)


def test_pyrevit_metadata_csv_exists():
    assert PYREVIT_METADATA_CSV.exists()


def test_pyrevit_metadata_csv_has_required_columns():
    fieldnames, _ = read_csv_rows(PYREVIT_METADATA_CSV)

    assert fieldnames is not None

    for column in REQUIRED_COLUMNS:
        assert column in fieldnames


def test_pyrevit_metadata_csv_has_at_least_one_data_row():
    _, rows = read_csv_rows(PYREVIT_METADATA_CSV)

    assert len(rows) >= 1


def test_pyrevit_metadata_required_values_are_not_blank():
    _, rows = read_csv_rows(PYREVIT_METADATA_CSV)

    for row in rows:
        assert row["ElementId"].strip() != ""
        assert row["UniqueId"].strip() != ""
        assert row["Category"].strip() != ""


def test_pyrevit_metadata_door_room_fields_can_be_blank():
    _, rows = read_csv_rows(PYREVIT_METADATA_CSV)

    for row in rows:
        if row["Category"] in ["ドア", "Door", "Doors"]:
            assert "RoomName" in row
            assert "RoomNumber" in row