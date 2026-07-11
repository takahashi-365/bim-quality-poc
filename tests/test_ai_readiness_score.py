"""Tests for production AI Readiness scoring functions."""

import pytest

from src.calculate_ai_readiness_score import (
    calculate_ai_readiness_score,
    classify_ai_readiness_level,
    format_element_id,
    is_human_review_required,
    validate_rule_master_v003_columns,
)


def test_ai_readiness_level_high():
    assert classify_ai_readiness_level(100) == "High"
    assert classify_ai_readiness_level(80) == "High"


def test_ai_readiness_level_medium():
    assert classify_ai_readiness_level(79) == "Medium"
    assert classify_ai_readiness_level(60) == "Medium"


def test_ai_readiness_level_low():
    assert classify_ai_readiness_level(59) == "Low"
    assert classify_ai_readiness_level(0) == "Low"


def test_ai_readiness_score_subtracts_penalty_total():
    assert calculate_ai_readiness_score(60) == 40


def test_ai_readiness_score_does_not_go_below_zero():
    assert calculate_ai_readiness_score(150) == 0


def test_human_review_required_when_level_is_low():
    result = is_human_review_required(
        ai_readiness_level="Low",
        high_impact_rule_count=0,
    )

    assert result is True


def test_human_review_required_when_high_impact_rule_exists():
    result = is_human_review_required(
        ai_readiness_level="Medium",
        high_impact_rule_count=1,
    )

    assert result is True


def test_human_review_not_required_when_level_is_not_low_and_no_high_impact_rule():
    result = is_human_review_required(
        ai_readiness_level="Medium",
        high_impact_rule_count=0,
    )

    assert result is False


def test_rule_master_v003_required_columns_exist():
    columns = [
        "RuleId",
        "RuleName",
        "Severity",
        "AIReadinessImpact",
        "AIReadinessPenalty",
    ]

    assert validate_rule_master_v003_columns(columns) is True


def test_rule_master_v003_missing_required_column_raises_error():
    columns = [
        "RuleId",
        "RuleName",
        "Severity",
        "AIReadinessImpact",
    ]

    with pytest.raises(ValueError, match="AIReadinessPenalty"):
        validate_rule_master_v003_columns(columns)


def test_format_element_id_removes_decimal_zero():
    assert format_element_id(101.0) == "101"
    assert format_element_id("101.0") == "101"
    assert format_element_id(101) == "101"
    assert format_element_id("101") == "101"
