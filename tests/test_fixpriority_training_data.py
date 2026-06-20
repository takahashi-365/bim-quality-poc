import csv
from pathlib import Path


CSV_PATH = Path("07_fixpriority_training/fixpriority_training_samples_v001.csv")


REQUIRED_COLUMNS = {
    "TrainingSampleId",
    "ElementId",
    "Category",
    "RuleId",
    "RuleName",
    "Severity",
    "HumanReviewRequired",
    "IssueSummary",
    "CurrentFixPriority",
    "ProposedFixPriorityLabel",
    "LabelReason",
    "ReviewStatus",
    "SourceFile",
    "CreatedDate",
}

ALLOWED_FIX_PRIORITY_LABELS = {"High", "Medium", "Low", "Review"}
ALLOWED_REVIEW_STATUS = {"Draft", "Reviewed", "Approved"}
ALLOWED_CATEGORIES = {"Door", "Room", "Other"}


def read_rows():
    assert CSV_PATH.exists(), f"CSV file does not exist: {CSV_PATH}"

    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    return reader.fieldnames, rows


def test_fixpriority_training_csv_exists():
    assert CSV_PATH.exists()


def test_fixpriority_training_csv_has_expected_row_count():
    _, rows = read_rows()
    assert len(rows) == 8


def test_fixpriority_training_csv_has_required_columns():
    fieldnames, _ = read_rows()
    assert fieldnames is not None

    missing_columns = REQUIRED_COLUMNS - set(fieldnames)
    assert not missing_columns, f"Missing required columns: {sorted(missing_columns)}"


def test_training_sample_id_is_required_and_unique():
    _, rows = read_rows()

    sample_ids = [row["TrainingSampleId"].strip() for row in rows]

    assert all(sample_ids), "TrainingSampleId must not be empty"
    assert len(sample_ids) == len(set(sample_ids)), "TrainingSampleId must be unique"


def test_required_values_are_not_empty():
    _, rows = read_rows()

    for row in rows:
        for column in REQUIRED_COLUMNS:
            assert row[column].strip(), (
                f"{column} must not be empty "
                f"for TrainingSampleId={row.get('TrainingSampleId')}"
            )


def test_proposed_fixpriority_label_allowed_values():
    _, rows = read_rows()

    for row in rows:
        label = row["ProposedFixPriorityLabel"].strip()
        assert label in ALLOWED_FIX_PRIORITY_LABELS, (
            f"Invalid ProposedFixPriorityLabel={label} "
            f"for TrainingSampleId={row.get('TrainingSampleId')}"
        )


def test_review_status_allowed_values():
    _, rows = read_rows()

    for row in rows:
        status = row["ReviewStatus"].strip()
        assert status in ALLOWED_REVIEW_STATUS, (
            f"Invalid ReviewStatus={status} "
            f"for TrainingSampleId={row.get('TrainingSampleId')}"
        )


def test_category_allowed_values():
    _, rows = read_rows()

    for row in rows:
        category = row["Category"].strip()
        assert category in ALLOWED_CATEGORIES, (
            f"Invalid Category={category} "
            f"for TrainingSampleId={row.get('TrainingSampleId')}"
        )


def test_label_reason_is_required():
    _, rows = read_rows()

    for row in rows:
        assert row["LabelReason"].strip(), (
            f"LabelReason must not be empty "
            f"for TrainingSampleId={row.get('TrainingSampleId')}"
        )


def test_review_label_has_reason():
    _, rows = read_rows()

    for row in rows:
        if row["ProposedFixPriorityLabel"].strip() == "Review":
            assert row["LabelReason"].strip(), (
                f"Review label must have LabelReason "
                f"for TrainingSampleId={row.get('TrainingSampleId')}"
            )


def test_human_review_required_true_has_reason():
    _, rows = read_rows()

    for row in rows:
        if row["HumanReviewRequired"].strip() == "True":
            assert row["LabelReason"].strip(), (
                f"HumanReviewRequired=True must have LabelReason "
                f"for TrainingSampleId={row.get('TrainingSampleId')}"
            )