from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

CHECK_RESULTS_PATH = BASE_DIR / "04_output_csv" / "check_results_revit_v002.csv"
RULE_MASTER_PATH = BASE_DIR / "02_rule_master" / "bim_rule_master_v003.csv"
OUTPUT_PATH = BASE_DIR / "04_output_csv" / "ai_readiness_scores_v001.csv"


RULE_MASTER_V003_REQUIRED_COLUMNS = [
    "RuleId",
    "AIReadinessImpact",
    "AIReadinessPenalty",
]


def classify_ai_readiness_level(score: float) -> str:
    """Classify AI Readiness Score into High / Medium / Low."""
    if score >= 80:
        return "High"
    if score >= 60:
        return "Medium"
    return "Low"


def calculate_ai_readiness_score(penalty_total: float) -> float:
    """Calculate AI Readiness Score with a lower bound of zero."""
    score = 100 - penalty_total
    return max(score, 0)


def is_human_review_required(
    ai_readiness_level: str,
    high_impact_rule_count: int,
) -> bool:
    """Return True when human review is required."""
    return (
        ai_readiness_level == "Low"
        or high_impact_rule_count >= 1
    )


def validate_columns(
    df: pd.DataFrame,
    required_columns: list[str],
    file_label: str,
) -> None:
    """Validate that required columns exist in the dataframe."""
    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"{file_label} is missing required columns: {missing_columns}"
        )


def validate_rule_master_v003_columns(columns) -> bool:
    """Validate the required columns for Rule Master v003."""
    missing_columns = [
        column
        for column in RULE_MASTER_V003_REQUIRED_COLUMNS
        if column not in columns
    ]

    if missing_columns:
        raise ValueError(
            "Rule Master v003 is missing required columns: "
            f"{missing_columns}"
        )

    return True


def format_element_id(value) -> str:
    """Format an ElementId without a trailing decimal zero."""
    try:
        numeric_value = float(value)

        if numeric_value.is_integer():
            return str(int(numeric_value))

        return str(value)

    except (TypeError, ValueError):
        return str(value)


def main() -> None:
    print("Loading input files...")

    check_results = pd.read_csv(CHECK_RESULTS_PATH)
    rule_master = pd.read_csv(RULE_MASTER_PATH)

    print(f"Check results shape: {check_results.shape}")
    print(f"Rule master shape: {rule_master.shape}")

    validate_columns(
        check_results,
        ["ElementId", "RuleId"],
        "check_results_revit_v002.csv",
    )

    validate_rule_master_v003_columns(rule_master.columns)

    rule_master_for_merge = rule_master[
        RULE_MASTER_V003_REQUIRED_COLUMNS
    ].copy()

    rule_master_for_merge["AIReadinessPenalty"] = pd.to_numeric(
        rule_master_for_merge["AIReadinessPenalty"],
        errors="coerce",
    ).fillna(0)

    merged = check_results.merge(
        rule_master_for_merge,
        on="RuleId",
        how="left",
    )

    merged["AIReadinessImpact"] = (
        merged["AIReadinessImpact"].fillna("Unknown")
    )
    merged["AIReadinessPenalty"] = (
        merged["AIReadinessPenalty"].fillna(0)
    )

    if "Category" not in merged.columns:
        merged["Category"] = ""

    grouped = (
        merged.groupby("ElementId")
        .agg(
            Category=(
                "Category",
                lambda values: ", ".join(
                    sorted(set(values.dropna().astype(str)))
                ),
            ),
            RuleViolationCount=("RuleId", "count"),
            AIReadinessPenaltyTotal=("AIReadinessPenalty", "sum"),
            BlockingRuleIds=(
                "RuleId",
                lambda values: ", ".join(
                    sorted(set(values.dropna().astype(str)))
                ),
            ),
            HighImpactRuleCount=(
                "AIReadinessImpact",
                lambda values: (values == "High").sum(),
            ),
            MediumImpactRuleCount=(
                "AIReadinessImpact",
                lambda values: (values == "Medium").sum(),
            ),
        )
        .reset_index()
    )

    grouped["AIReadinessScore"] = grouped[
        "AIReadinessPenaltyTotal"
    ].apply(calculate_ai_readiness_score)

    grouped["AIReadinessLevel"] = grouped[
        "AIReadinessScore"
    ].apply(classify_ai_readiness_level)

    grouped["HumanReviewRequired"] = grouped.apply(
        lambda row: is_human_review_required(
            ai_readiness_level=row["AIReadinessLevel"],
            high_impact_rule_count=row["HighImpactRuleCount"],
        ),
        axis=1,
    )

    grouped["ElementId"] = grouped["ElementId"].apply(
        format_element_id
    )

    output_columns = [
        "ElementId",
        "Category",
        "RuleViolationCount",
        "AIReadinessPenaltyTotal",
        "AIReadinessScore",
        "AIReadinessLevel",
        "BlockingRuleIds",
        "HighImpactRuleCount",
        "MediumImpactRuleCount",
        "HumanReviewRequired",
    ]

    grouped = grouped[output_columns]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    grouped.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    print(f"AI Readiness scores shape: {grouped.shape}")
    print(f"Output saved to: {OUTPUT_PATH}")

    print("\nAI Readiness Level counts:")
    print(grouped["AIReadinessLevel"].value_counts())


if __name__ == "__main__":
    main()
