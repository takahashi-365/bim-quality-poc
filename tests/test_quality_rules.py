"""Tests for the production BIM quality check functions."""

import pandas as pd

from src.check_bim_quality import (
    check_classification_code,
    check_family_naming,
    check_required_parameters,
    run_quality_checks,
)


def create_rule_master() -> pd.DataFrame:
    """Create a minimal Rule Master fixture for R-001 to R-003."""
    return pd.DataFrame(
        [
            {
                "RuleId": "R-001",
                "RuleName": "必須パラメータ未入力",
                "Severity": "High",
                "FixGuide": "必須項目を入力する",
            },
            {
                "RuleId": "R-002",
                "RuleName": "分類コード未入力",
                "Severity": "High",
                "FixGuide": "分類コードを入力する",
            },
            {
                "RuleId": "R-003",
                "RuleName": "ファミリ命名規則違反",
                "Severity": "Medium",
                "FixGuide": "ファミリ名を修正する",
            },
        ]
    )


def test_r001_required_parameters_detects_blank_fields():
    row = pd.Series(
        {
            "ElementId": "101",
            "Category": "Doors",
            "BIM_ModelRole": "",
            "BIM_Zone": "",
        }
    )
    results = []

    check_required_parameters(row, create_rule_master(), results)

    assert len(results) == 2
    assert results[0]["RuleId"] == "R-001"
    assert results[1]["RuleId"] == "R-001"
    assert {result["ParameterName"] for result in results} == {
        "BIM_ModelRole",
        "BIM_Zone",
    }


def test_r002_classification_code_detects_blank_field():
    row = pd.Series(
        {
            "ElementId": "101",
            "Category": "Doors",
            "BIM_ClassificationCode": "",
        }
    )
    results = []

    check_classification_code(row, create_rule_master(), results)

    assert len(results) == 1
    assert results[0]["RuleId"] == "R-002"
    assert results[0]["ParameterName"] == "BIM_ClassificationCode"


def test_r003_family_naming_detects_invalid_door_family_name():
    row = pd.Series(
        {
            "ElementId": "101",
            "Category": "Doors",
            "FamilyName": "SD",
        }
    )
    results = []

    check_family_naming(row, create_rule_master(), results)

    assert len(results) == 1
    assert results[0]["RuleId"] == "R-003"
    assert results[0]["ParameterName"] == "FamilyName"


def test_r003_family_naming_passes_valid_door_family_name():
    row = pd.Series(
        {
            "ElementId": "101",
            "Category": "Doors",
            "FamilyName": "DR_SingleDoor",
        }
    )
    results = []

    check_family_naming(row, create_rule_master(), results)

    assert results == []


def test_all_rules_detect_expected_violations():
    input_df = pd.DataFrame(
        [
            {
                "ElementId": "101",
                "Category": "Doors",
                "FamilyName": "SD",
                "BIM_ClassificationCode": "",
                "BIM_ModelRole": "",
                "BIM_Zone": "",
            }
        ]
    )

    results = run_quality_checks(input_df, create_rule_master())

    rule_ids = [result["RuleId"] for result in results]

    assert rule_ids.count("R-001") == 2
    assert rule_ids.count("R-002") == 1
    assert rule_ids.count("R-003") == 1
    assert len(results) == 4
