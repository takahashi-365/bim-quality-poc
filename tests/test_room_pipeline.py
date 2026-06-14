import pandas as pd

from src.clean_room_data import build_element_id, parse_area
from src.check_room_quality import is_blank
from src.calculate_room_ai_readiness_score import classify_ai_readiness_level


def test_parse_area_from_unit_string():
    assert parse_area("12.34 m²") == 12.34
    assert parse_area("12.34㎡") == 12.34
    assert parse_area("0 m²") == 0
    assert parse_area("") is None


def test_build_element_id_is_unique_with_sequence():
    assert build_element_id("1FL", "101", "会議室", 0) == "1FL-101-0001"
    assert build_element_id("1FL", "101", "会議室", 1) == "1FL-101-0002"
    assert build_element_id("1FL", "", "会議室", 2) == "1FL-会議室-0003"
    assert build_element_id("", "", "", 3) == "Room-0004"


def test_is_blank_for_room_quality_check():
    assert is_blank("") is True
    assert is_blank(None) is True
    assert is_blank(float("nan")) is True
    assert is_blank("RoomName") is False


def test_room_ai_readiness_level_classification():
    assert classify_ai_readiness_level(100) == "High"
    assert classify_ai_readiness_level(80) == "High"
    assert classify_ai_readiness_level(79) == "Medium"
    assert classify_ai_readiness_level(60) == "Medium"
    assert classify_ai_readiness_level(59) == "Low"


def test_room_output_files_have_expected_columns():
    cleaned = pd.read_csv("03_input_csv/cleaned_room_data_v001.csv")
    check_results = pd.read_csv("04_output_csv/check_results_room_v001.csv")
    ai_scores = pd.read_csv("04_output_csv/room_ai_readiness_scores_v001.csv")

    assert "Category" in cleaned.columns
    assert set(cleaned["Category"]) == {"Room"}
    assert cleaned["ElementId"].nunique() == len(cleaned)

    assert {"ElementId", "RuleId", "Category", "CheckResult"}.issubset(
        check_results.columns
    )
    assert set(check_results["Category"]) == {"Room"}

    assert {
        "ElementId",
        "AIReadinessScore",
        "AIReadinessLevel",
        "HumanReviewRequired",
    }.issubset(ai_scores.columns)

    assert len(ai_scores) == len(cleaned)