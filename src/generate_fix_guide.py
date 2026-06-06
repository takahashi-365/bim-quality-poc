# このファイルの目的：
# BIM品質チェック結果、Rule Master v003、AI Readiness Scoreをもとに、
# 修正方針をMarkdown形式で出力する。
#
# 注意：
# このスクリプトではOpenAI APIなどの生成AI APIは呼び出さない。
# RuleIdベースのテンプレート方式で、人間確認向けの修正ガイドを生成する。

from pathlib import Path

import pandas as pd


# =========================================
# Path settings
# =========================================

BASE_DIR = Path(__file__).resolve().parents[1]

CHECK_RESULTS_CSV = BASE_DIR / "04_output_csv" / "check_results_revit_v002.csv"
RULE_MASTER_CSV = BASE_DIR / "02_rule_master" / "bim_rule_master_v003.csv"
AI_READINESS_CSV = BASE_DIR / "04_output_csv" / "ai_readiness_scores_v001.csv"

OUTPUT_MD = BASE_DIR / "04_output_csv" / "fix_guides_v001.md"


# =========================================
# Helper functions
# =========================================

def validate_input_files() -> None:
    """Validate that required input files exist."""
    if not CHECK_RESULTS_CSV.exists():
        raise FileNotFoundError(f"Check results CSV not found: {CHECK_RESULTS_CSV}")

    if not RULE_MASTER_CSV.exists():
        raise FileNotFoundError(f"Rule master CSV not found: {RULE_MASTER_CSV}")

    if not AI_READINESS_CSV.exists():
        raise FileNotFoundError(f"AI readiness CSV not found: {AI_READINESS_CSV}")


def validate_columns(
    df: pd.DataFrame,
    required_columns: list[str],
    file_label: str,
) -> None:
    """Validate that required columns exist in the dataframe."""
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing columns in {file_label}: {missing_columns}")


def normalize_element_id_series(series: pd.Series) -> pd.Series:
    """Normalize ElementId values such as 101.0 to 101."""
    return (
        pd.to_numeric(series, errors="coerce")
        .astype("Int64")
        .astype(str)
        .replace("<NA>", "")
    )


def safe_value(value) -> str:
    """Convert NaN to empty string."""
    if pd.isna(value):
        return ""
    return str(value)


def safe_int(value, default: int = 0) -> int:
    """Convert value to int safely."""
    if pd.isna(value):
        return default

    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def safe_bool(value) -> bool:
    """Convert value to bool safely."""
    if isinstance(value, bool):
        return value

    if pd.isna(value):
        return False

    return str(value).strip().lower() == "true"


def relative_posix_path(path: Path) -> str:
    """Return a project-relative path using forward slashes."""
    return path.relative_to(BASE_DIR).as_posix()


# =========================================
# Load and prepare data
# =========================================

def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load input CSV files."""
    check_results_df = pd.read_csv(CHECK_RESULTS_CSV, encoding="utf-8-sig")
    rule_master_df = pd.read_csv(RULE_MASTER_CSV, encoding="utf-8-sig")
    ai_readiness_df = pd.read_csv(AI_READINESS_CSV, encoding="utf-8-sig")

    check_results_df["ElementId"] = normalize_element_id_series(
        check_results_df["ElementId"]
    )
    ai_readiness_df["ElementId"] = normalize_element_id_series(
        ai_readiness_df["ElementId"]
    )

    return check_results_df, rule_master_df, ai_readiness_df


def prepare_fix_guide_data(
    check_results_df: pd.DataFrame,
    rule_master_df: pd.DataFrame,
    ai_readiness_df: pd.DataFrame,
) -> pd.DataFrame:
    """Merge check results, rule master, and AI readiness scores."""

    required_check_columns = [
        "ElementId",
        "Category",
        "FamilyName",
        "TypeName",
        "ParameterName",
        "CurrentValue",
        "RuleId",
        "RuleName",
        "Severity",
        "FixGuide",
        "SourceFile",
        "ModelName",
    ]

    validate_columns(
        check_results_df,
        required_check_columns,
        "check_results_revit_v002.csv",
    )

    required_rule_columns = [
        "RuleId",
        "AIReadinessImpact",
        "AIReadinessPenalty",
        "BusinessImpact",
        "AIUseImpact",
    ]

    validate_columns(
        rule_master_df,
        required_rule_columns,
        "bim_rule_master_v003.csv",
    )

    required_ai_readiness_columns = [
        "ElementId",
        "AIReadinessPenaltyTotal",
        "AIReadinessScore",
        "AIReadinessLevel",
        "BlockingRuleIds",
        "HighImpactRuleCount",
        "MediumImpactRuleCount",
        "HumanReviewRequired",
    ]

    validate_columns(
        ai_readiness_df,
        required_ai_readiness_columns,
        "ai_readiness_scores_v001.csv",
    )

    rule_columns = [
        "RuleId",
        "AIReadinessImpact",
        "AIReadinessPenalty",
        "BusinessImpact",
        "AIUseImpact",
    ]

    ai_readiness_columns = [
        "ElementId",
        "AIReadinessPenaltyTotal",
        "AIReadinessScore",
        "AIReadinessLevel",
        "BlockingRuleIds",
        "HighImpactRuleCount",
        "MediumImpactRuleCount",
        "HumanReviewRequired",
    ]

    merged_df = check_results_df.merge(
        rule_master_df[rule_columns],
        on="RuleId",
        how="left",
    )

    merged_df = merged_df.merge(
        ai_readiness_df[ai_readiness_columns],
        on="ElementId",
        how="left",
    )

    merged_df["AIReadinessImpact"] = merged_df["AIReadinessImpact"].fillna("Unknown")
    merged_df["AIReadinessPenalty"] = pd.to_numeric(
        merged_df["AIReadinessPenalty"],
        errors="coerce",
    ).fillna(0)

    merged_df["AIReadinessPenaltyTotal"] = pd.to_numeric(
        merged_df["AIReadinessPenaltyTotal"],
        errors="coerce",
    ).fillna(0)

    merged_df["AIReadinessScore"] = pd.to_numeric(
        merged_df["AIReadinessScore"],
        errors="coerce",
    ).fillna(0)

    merged_df["HumanReviewRequired"] = merged_df["HumanReviewRequired"].apply(
        safe_bool
    )

    return merged_df


# =========================================
# Markdown builders
# =========================================

def build_summary_section(fix_guide_df: pd.DataFrame) -> list[str]:
    """Build summary section for Markdown."""
    element_summary = fix_guide_df.drop_duplicates(subset=["ElementId"]).copy()

    total_elements = element_summary["ElementId"].nunique()
    total_violations = len(fix_guide_df)
    human_review_required_count = int(element_summary["HumanReviewRequired"].sum())
    average_ai_readiness_score = round(
        float(element_summary["AIReadinessScore"].mean()),
        2,
    )

    level_summary = (
        element_summary["AIReadinessLevel"]
        .value_counts()
        .reset_index()
    )
    level_summary.columns = ["AIReadinessLevel", "Count"]

    rule_summary = (
        fix_guide_df.groupby(["RuleId", "RuleName", "Severity", "AIReadinessImpact"])
        .size()
        .reset_index(name="ViolationCount")
        .sort_values("ViolationCount", ascending=False)
    )

    lines = []

    lines.append("# Fix Guide v001")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total target elements: {total_elements}")
    lines.append(f"- Total violations: {total_violations}")
    lines.append(f"- Average AI Readiness Score: {average_ai_readiness_score}")
    lines.append(f"- Human Review Required Count: {human_review_required_count}")
    lines.append("")
    lines.append("## Input Files")
    lines.append("")
    lines.append(f"- Check results CSV: `{relative_posix_path(CHECK_RESULTS_CSV)}`")
    lines.append(f"- Rule master CSV: `{relative_posix_path(RULE_MASTER_CSV)}`")
    lines.append(f"- AI readiness CSV: `{relative_posix_path(AI_READINESS_CSV)}`")
    lines.append("")
    lines.append("## AI Readiness Level Summary")
    lines.append("")
    lines.append("| AIReadinessLevel | Count |")
    lines.append("|---|---:|")

    for _, row in level_summary.iterrows():
        lines.append(
            f"| {safe_value(row['AIReadinessLevel'])} | {safe_int(row['Count'])} |"
        )

    lines.append("")
    lines.append("## Blocking Rule Summary")
    lines.append("")
    lines.append("| RuleId | RuleName | Severity | AIReadinessImpact | ViolationCount |")
    lines.append("|---|---|---|---|---:|")

    for _, row in rule_summary.iterrows():
        lines.append(
            f"| {safe_value(row['RuleId'])} "
            f"| {safe_value(row['RuleName'])} "
            f"| {safe_value(row['Severity'])} "
            f"| {safe_value(row['AIReadinessImpact'])} "
            f"| {safe_int(row['ViolationCount'])} |"
        )

    lines.append("")

    return lines


def build_element_fix_guide_section(fix_guide_df: pd.DataFrame) -> list[str]:
    """Build element-level fix guide section."""
    lines = []

    lines.append("## Element Fix Guide")
    lines.append("")

    sorted_element_ids = sorted(
        fix_guide_df["ElementId"].dropna().unique(),
        key=lambda x: int(x) if str(x).isdigit() else str(x),
    )

    for element_id in sorted_element_ids:
        element_df = fix_guide_df[fix_guide_df["ElementId"] == element_id].copy()
        first_row = element_df.iloc[0]

        lines.append(f"### ElementId: {safe_value(element_id)}")
        lines.append("")
        lines.append(f"- Category: {safe_value(first_row.get('Category', ''))}")
        lines.append(f"- FamilyName: {safe_value(first_row.get('FamilyName', ''))}")
        lines.append(f"- TypeName: {safe_value(first_row.get('TypeName', ''))}")
        lines.append(
            f"- AI Readiness Score: {safe_int(first_row.get('AIReadinessScore', 0))}"
        )
        lines.append(
            f"- AI Readiness Level: {safe_value(first_row.get('AIReadinessLevel', ''))}"
        )
        lines.append(
            f"- AI Readiness Penalty Total: "
            f"{safe_int(first_row.get('AIReadinessPenaltyTotal', 0))}"
        )
        lines.append(
            f"- Blocking RuleIds: {safe_value(first_row.get('BlockingRuleIds', ''))}"
        )
        lines.append(
            f"- Human Review Required: "
            f"{safe_bool(first_row.get('HumanReviewRequired', False))}"
        )
        lines.append("")

        lines.append("Recommended fix approach:")
        lines.append("")
        lines.append(
            "- Review the listed RuleId violations before using this BIM data for AI, BI, or analytics."
        )
        lines.append(
            "- Prioritize High severity and High AIReadinessImpact issues."
        )
        lines.append(
            "- Confirm final model correction decisions with a human BIM reviewer."
        )
        lines.append("")

        lines.append(
            "| RuleId | RuleName | Severity | ParameterName | CurrentValue | "
            "AIReadinessImpact | AIReadinessPenalty | FixGuide |"
        )
        lines.append("|---|---|---|---|---|---|---:|---|")

        for _, row in element_df.iterrows():
            lines.append(
                f"| {safe_value(row.get('RuleId', ''))} "
                f"| {safe_value(row.get('RuleName', ''))} "
                f"| {safe_value(row.get('Severity', ''))} "
                f"| {safe_value(row.get('ParameterName', ''))} "
                f"| {safe_value(row.get('CurrentValue', ''))} "
                f"| {safe_value(row.get('AIReadinessImpact', ''))} "
                f"| {safe_int(row.get('AIReadinessPenalty', 0))} "
                f"| {safe_value(row.get('FixGuide', ''))} |"
            )

        lines.append("")

    return lines


def build_limitations_section() -> list[str]:
    """Build limitations section."""
    lines = []

    lines.append("## Limitations")
    lines.append("")
    lines.append(
        "- This Fix Guide is generated by rule-based templates, not by a generative AI API."
    )
    lines.append(
        "- AIReadinessScore is a simple PoC metric, not an official AI readiness standard."
    )
    lines.append(
        "- Fix recommendations are intended to support human review, not automate BIM model correction."
    )
    lines.append(
        "- Final design, construction, and model correction decisions should be made by a human reviewer."
    )
    lines.append(
        "- Revit API and pyRevit integration are not implemented in this stage."
    )
    lines.append("")

    return lines


def save_fix_guide_markdown(fix_guide_df: pd.DataFrame) -> None:
    """Save fix guide as Markdown."""
    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)

    lines = []
    lines.extend(build_summary_section(fix_guide_df))
    lines.extend(build_element_fix_guide_section(fix_guide_df))
    lines.extend(build_limitations_section())

    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")


# =========================================
# Main process
# =========================================

def main() -> None:
    print("Fix guide generation started.")

    validate_input_files()

    print(f"Check results file: {CHECK_RESULTS_CSV}")
    print(f"Rule master file: {RULE_MASTER_CSV}")
    print(f"AI readiness file: {AI_READINESS_CSV}")

    check_results_df, rule_master_df, ai_readiness_df = load_data()

    print(f"Check results shape: {check_results_df.shape}")
    print(f"Rule master shape: {rule_master_df.shape}")
    print(f"AI readiness shape: {ai_readiness_df.shape}")

    fix_guide_df = prepare_fix_guide_data(
        check_results_df,
        rule_master_df,
        ai_readiness_df,
    )

    print(f"Fix guide merged shape: {fix_guide_df.shape}")

    save_fix_guide_markdown(fix_guide_df)

    print(f"Markdown output file: {OUTPUT_MD}")
    print("Fix guide generation completed.")


if __name__ == "__main__":
    main()