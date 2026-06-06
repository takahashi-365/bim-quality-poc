from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

CHECK_RESULTS_PATH = BASE_DIR / "04_output_csv" / "check_results_revit_v002.csv"
RULE_MASTER_PATH = BASE_DIR / "02_rule_master" / "bim_rule_master_v003.csv"
OUTPUT_PATH = BASE_DIR / "04_output_csv" / "ai_readiness_scores_v001.csv"


def classify_ai_readiness_level(score: float) -> str:
    """Classify AI Readiness Score into High / Medium / Low."""
    if score >= 80:
        return "High"
    if score >= 60:
        return "Medium"
    return "Low"


def validate_columns(df: pd.DataFrame, required_columns: list[str], file_label: str) -> None:
    """Validate that required columns exist in the dataframe."""
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(
            f"{file_label} is missing required columns: {missing_columns}"
        )


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

    validate_columns(
        rule_master,
        ["RuleId", "AIReadinessImpact", "AIReadinessPenalty"],
        "bim_rule_master_v003.csv",
    )

    rule_master_for_merge = rule_master[
        ["RuleId", "AIReadinessImpact", "AIReadinessPenalty"]
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

    merged["AIReadinessImpact"] = merged["AIReadinessImpact"].fillna("Unknown")
    merged["AIReadinessPenalty"] = merged["AIReadinessPenalty"].fillna(0)

    if "Category" not in merged.columns:
        merged["Category"] = ""

    grouped = (
        merged.groupby("ElementId")
        .agg(
            Category=("Category", lambda x: ", ".join(sorted(set(x.dropna().astype(str))))),
            RuleViolationCount=("RuleId", "count"),
            AIReadinessPenaltyTotal=("AIReadinessPenalty", "sum"),
            BlockingRuleIds=("RuleId", lambda x: ", ".join(sorted(set(x.dropna().astype(str))))),
            HighImpactRuleCount=("AIReadinessImpact", lambda x: (x == "High").sum()),
            MediumImpactRuleCount=("AIReadinessImpact", lambda x: (x == "Medium").sum()),
        )
        .reset_index()
    )

    grouped["AIReadinessScore"] = 100 - grouped["AIReadinessPenaltyTotal"]
    grouped["AIReadinessScore"] = grouped["AIReadinessScore"].clip(lower=0)

    grouped["AIReadinessLevel"] = grouped["AIReadinessScore"].apply(
        classify_ai_readiness_level
    )

    grouped["HumanReviewRequired"] = (
        (grouped["AIReadinessLevel"] == "Low")
        | (grouped["HighImpactRuleCount"] >= 1)
    )

    grouped["ElementId"] = (
        pd.to_numeric(grouped["ElementId"], errors="coerce")
        .astype("Int64")
        .astype(str)
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
    grouped.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print(f"AI Readiness scores shape: {grouped.shape}")
    print(f"Output saved to: {OUTPUT_PATH}")

    print("\nAI Readiness Level counts:")
    print(grouped["AIReadinessLevel"].value_counts())


if __name__ == "__main__":
    main()