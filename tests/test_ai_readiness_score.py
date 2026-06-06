# tests/test_ai_readiness_score.py

"""
AI Readiness Scoreの最小テスト。

現時点では、src/calculate_ai_readiness_score.py の内部処理全体を直接実行するのではなく、
AI Readiness Assessmentで使用する主要ロジックの期待動作を確認する。

確認対象：
- AI Readiness Level分類
- AI Readiness Score計算
- スコア下限0の扱い
- HumanReviewRequired判定
- Rule Master v003必須列確認
- ElementId表示整形
"""


def classify_ai_readiness_level(score):
    """AI Readiness Scoreを High / Medium / Low に分類する。"""
    if score >= 80:
        return "High"
    if score >= 60:
        return "Medium"
    return "Low"


def calculate_ai_readiness_score(penalty_total):
    """AI Readiness Scoreを計算する。スコアは0未満にしない。"""
    score = 100 - penalty_total
    return max(score, 0)


def is_human_review_required(ai_readiness_level, high_impact_rule_count):
    """
    人間確認要否を判定する。

    現時点では、以下のいずれかに該当する場合 True とする。
    - AIReadinessLevel が Low
    - HighImpactRuleCount が1件以上
    """
    return ai_readiness_level == "Low" or high_impact_rule_count >= 1


def validate_rule_master_v003_columns(columns):
    """Rule Master v003に必要な列が存在するか確認する。"""
    required_columns = [
        "RuleId",
        "AIReadinessImpact",
        "AIReadinessPenalty",
    ]

    missing_columns = [col for col in required_columns if col not in columns]

    if missing_columns:
        raise ValueError(f"Rule Master v003 is missing required columns: {missing_columns}")

    return True


def format_element_id(value):
    """
    ElementIdを表示用に整形する。

    例：
    101.0 -> "101"
    101   -> "101"
    "101" -> "101"
    """
    try:
        numeric_value = float(value)
        if numeric_value.is_integer():
            return str(int(numeric_value))
        return str(value)
    except (TypeError, ValueError):
        return str(value)


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
    penalty_total = 60

    score = calculate_ai_readiness_score(penalty_total)

    assert score == 40


def test_ai_readiness_score_does_not_go_below_zero():
    penalty_total = 150

    score = calculate_ai_readiness_score(penalty_total)

    assert score == 0


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

    result = validate_rule_master_v003_columns(columns)

    assert result is True


def test_rule_master_v003_missing_required_column_raises_error():
    columns = [
        "RuleId",
        "RuleName",
        "Severity",
        "AIReadinessImpact",
    ]

    try:
        validate_rule_master_v003_columns(columns)
    except ValueError as error:
        assert "AIReadinessPenalty" in str(error)
    else:
        raise AssertionError("ValueError was not raised")


def test_format_element_id_removes_decimal_zero():
    assert format_element_id(101.0) == "101"
    assert format_element_id("101.0") == "101"
    assert format_element_id(101) == "101"
    assert format_element_id("101") == "101"
