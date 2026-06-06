# このファイルの目的：
# BIM品質チェック結果、品質メトリクス、特徴量データセット、AI Readiness Scoreをもとに、
# 生成AIへ渡すための構造化コンテキストをJSON / Markdownとして出力する。
#
# 注意：
# このスクリプトではOpenAI APIなどの生成AI APIは呼び出さない。
# 生成AIに渡す前段階の「参照情報を整理する処理」として位置づける。

from pathlib import Path
import json

import pandas as pd


# =========================================
# Path settings
# =========================================

BASE_DIR = Path(__file__).resolve().parents[1]

CHECK_RESULTS_CSV = BASE_DIR / "04_output_csv" / "check_results_revit_v002.csv"
FEATURES_CSV = BASE_DIR / "04_output_csv" / "bim_features_v001.csv"
AI_READINESS_CSV = BASE_DIR / "04_output_csv" / "ai_readiness_scores_v001.csv"

OUTPUT_JSON = BASE_DIR / "04_output_csv" / "ai_context_v002.json"
OUTPUT_MD = BASE_DIR / "04_output_csv" / "ai_context_v002.md"


# =========================================
# Helper functions
# =========================================

def validate_input_files() -> None:
    """Validate that required input files exist."""
    if not CHECK_RESULTS_CSV.exists():
        raise FileNotFoundError(f"Check results CSV not found: {CHECK_RESULTS_CSV}")

    if not FEATURES_CSV.exists():
        raise FileNotFoundError(f"Features CSV not found: {FEATURES_CSV}")

    if not AI_READINESS_CSV.exists():
        raise FileNotFoundError(f"AI readiness CSV not found: {AI_READINESS_CSV}")


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load check results, feature dataset, and AI readiness scores."""
    check_results_df = pd.read_csv(CHECK_RESULTS_CSV, encoding="utf-8-sig")
    features_df = pd.read_csv(FEATURES_CSV, encoding="utf-8-sig")
    ai_readiness_df = pd.read_csv(AI_READINESS_CSV, encoding="utf-8-sig")

    check_results_df["ElementId"] = normalize_element_id_series(
        check_results_df["ElementId"]
    )
    features_df["ElementId"] = normalize_element_id_series(features_df["ElementId"])
    ai_readiness_df["ElementId"] = normalize_element_id_series(
        ai_readiness_df["ElementId"]
    )

    return check_results_df, features_df, ai_readiness_df


def normalize_element_id_series(series: pd.Series) -> pd.Series:
    """Normalize ElementId values such as 101.0 to 101."""
    return (
        pd.to_numeric(series, errors="coerce")
        .astype("Int64")
        .astype(str)
        .replace("<NA>", "")
    )


def safe_value(value):
    """Convert NaN to empty string and return a JSON-safe value."""
    if pd.isna(value):
        return ""
    return value


def relative_posix_path(path: Path) -> str:
    """Return a project-relative path using forward slashes."""
    return path.relative_to(BASE_DIR).as_posix()


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


def split_rule_ids(value) -> list[str]:
    """Split comma-separated RuleIds into a list."""
    if pd.isna(value) or value == "":
        return []

    return [item.strip() for item in str(value).split(",") if item.strip()]


def validate_columns(
    df: pd.DataFrame,
    required_columns: list[str],
    file_label: str,
) -> None:
    """Validate that required columns exist in the dataframe."""
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing columns in {file_label}: {missing_columns}")


# =========================================
# Context builders
# =========================================

def build_element_context(
    check_results_df: pd.DataFrame,
    features_df: pd.DataFrame,
    ai_readiness_df: pd.DataFrame,
) -> list[dict]:
    """Build structured context by ElementId."""

    required_check_columns = [
        "ElementId",
        "Category",
        "FamilyName",
        "TypeName",
        "Level",
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

    required_feature_columns = [
        "ElementId",
        "RuleViolationCount",
        "MissingFieldCount",
        "HighViolationCount",
        "MediumViolationCount",
        "LowViolationCount",
        "SeverityScore",
        "QualityScore",
        "FixPriority",
    ]

    validate_columns(
        features_df,
        required_feature_columns,
        "bim_features_v001.csv",
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

    ai_readiness_lookup = ai_readiness_df.set_index("ElementId").to_dict(
        orient="index"
    )

    contexts = []

    for _, feature_row in features_df.iterrows():
        element_id = safe_value(feature_row["ElementId"])

        element_checks = check_results_df[
            check_results_df["ElementId"] == element_id
        ].copy()

        ai_readiness_row = ai_readiness_lookup.get(element_id, {})

        violations = []

        for _, check_row in element_checks.iterrows():
            violations.append({
                "rule_id": safe_value(check_row.get("RuleId", "")),
                "rule_name": safe_value(check_row.get("RuleName", "")),
                "severity": safe_value(check_row.get("Severity", "")),
                "parameter_name": safe_value(check_row.get("ParameterName", "")),
                "current_value": safe_value(check_row.get("CurrentValue", "")),
                "fix_guide": safe_value(check_row.get("FixGuide", "")),
            })

        first_check = element_checks.iloc[0] if not element_checks.empty else {}

        context = {
            "element": {
                "element_id": safe_value(element_id),
                "category": safe_value(first_check.get("Category", "")),
                "family_name": safe_value(first_check.get("FamilyName", "")),
                "type_name": safe_value(first_check.get("TypeName", "")),
                "level": safe_value(first_check.get("Level", "")),
                "source_file": safe_value(first_check.get("SourceFile", "")),
                "model_name": safe_value(first_check.get("ModelName", "")),
            },
            "quality_summary": {
                "rule_violation_count": safe_int(
                    feature_row.get("RuleViolationCount", 0)
                ),
                "missing_field_count": safe_int(
                    feature_row.get("MissingFieldCount", 0)
                ),
                "high_violation_count": safe_int(
                    feature_row.get("HighViolationCount", 0)
                ),
                "medium_violation_count": safe_int(
                    feature_row.get("MediumViolationCount", 0)
                ),
                "low_violation_count": safe_int(
                    feature_row.get("LowViolationCount", 0)
                ),
                "severity_score": safe_int(feature_row.get("SeverityScore", 0)),
                "quality_score": safe_int(feature_row.get("QualityScore", 0)),
                "fix_priority": safe_value(feature_row.get("FixPriority", "")),
            },
            "ai_readiness": {
                "ai_readiness_penalty_total": safe_int(
                    ai_readiness_row.get("AIReadinessPenaltyTotal", 0)
                ),
                "ai_readiness_score": safe_int(
                    ai_readiness_row.get("AIReadinessScore", 0)
                ),
                "ai_readiness_level": safe_value(
                    ai_readiness_row.get("AIReadinessLevel", "")
                ),
                "blocking_rule_ids": split_rule_ids(
                    ai_readiness_row.get("BlockingRuleIds", "")
                ),
                "high_impact_rule_count": safe_int(
                    ai_readiness_row.get("HighImpactRuleCount", 0)
                ),
                "medium_impact_rule_count": safe_int(
                    ai_readiness_row.get("MediumImpactRuleCount", 0)
                ),
                "human_review_required": safe_bool(
                    ai_readiness_row.get("HumanReviewRequired", False)
                ),
            },
            "violations": violations,
            "ai_instruction": {
                "role": "BIM data quality and AI readiness assistant",
                "task": (
                    "Explain detected BIM data quality issues, AI readiness risks, "
                    "and human-review-oriented fix actions."
                ),
                "constraints": [
                    "Do not assume information that is not included in the context.",
                    "Do not claim that the model can be automatically fixed.",
                    "Use RuleId, Severity, FixGuide, QualityScore, FixPriority, and AIReadinessScore as the primary reference information.",
                    "Explain that final design or model correction decisions should be made by a human reviewer.",
                    "Treat Low AIReadinessLevel and HumanReviewRequired=True as indicators that the BIM data should be reviewed before AI or BI usage.",
                ],
            },
        }

        contexts.append(context)

    return contexts


def build_summary_context(
    check_results_df: pd.DataFrame,
    features_df: pd.DataFrame,
    ai_readiness_df: pd.DataFrame,
) -> dict:
    """Build summary information for the AI context file."""
    rule_summary = (
        check_results_df.groupby(["RuleId", "RuleName", "Severity"])
        .size()
        .reset_index(name="ViolationCount")
        .sort_values("ViolationCount", ascending=False)
    )

    fix_priority_summary = (
        features_df["FixPriority"]
        .value_counts()
        .reset_index()
    )
    fix_priority_summary.columns = ["FixPriority", "Count"]

    ai_readiness_level_summary = (
        ai_readiness_df["AIReadinessLevel"]
        .value_counts()
        .reset_index()
    )
    ai_readiness_level_summary.columns = ["AIReadinessLevel", "Count"]

    average_ai_readiness_score = float(
        ai_readiness_df["AIReadinessScore"].mean()
    )

    human_review_required_count = int(
        ai_readiness_df["HumanReviewRequired"]
        .astype(str)
        .str.lower()
        .eq("true")
        .sum()
    )

    return {
        "project": {
            "name": "BIM Data Quality & AI Readiness Assessment PoC",
            "previous_name": "BIM Data Quality Engineering & AI Analysis PoC",
            "purpose": (
                "Prepare BIM quality check results and AI readiness scores as "
                "structured context for future generative AI or RAG usage."
            ),
            "note": "This context is generated for PoC purposes. It is not a production AI system.",
        },
        "input_files": {
            "check_results_csv": relative_posix_path(CHECK_RESULTS_CSV),
            "features_csv": relative_posix_path(FEATURES_CSV),
            "ai_readiness_csv": relative_posix_path(AI_READINESS_CSV),
        },
        "summary": {
            "total_violations": int(len(check_results_df)),
            "total_elements": int(features_df["ElementId"].nunique()),
            "rule_summary": rule_summary.to_dict(orient="records"),
            "fix_priority_summary": fix_priority_summary.to_dict(orient="records"),
            "ai_readiness_level_summary": ai_readiness_level_summary.to_dict(
                orient="records"
            ),
            "average_ai_readiness_score": round(average_ai_readiness_score, 2),
            "human_review_required_count": human_review_required_count,
        },
        "limitations": [
            "QualityScore is a simple PoC metric, not an official business quality standard.",
            "AIReadinessScore is a simple PoC metric, not an official AI readiness standard.",
            "FixPriority is a provisional label, not a verified business ground truth.",
            "The generated context is intended to support human review, not automate BIM model correction.",
            "Generative AI API integration is not implemented in this stage.",
            "Revit API and pyRevit integration are not implemented in this stage.",
        ],
    }


# =========================================
# Output writers
# =========================================

def save_json_context(context: dict) -> None:
    """Save AI context as JSON."""
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(context, f, ensure_ascii=False, indent=2)


def save_markdown_context(context: dict) -> None:
    """Save AI context as Markdown summary."""
    project = context["project"]
    summary = context["summary"]

    lines = []

    lines.append("# AI Context v002")
    lines.append("")
    lines.append("## Project")
    lines.append("")
    lines.append(f"- Name: {project['name']}")
    lines.append(f"- Previous Name: {project['previous_name']}")
    lines.append(f"- Purpose: {project['purpose']}")
    lines.append(f"- Note: {project['note']}")
    lines.append("")
    lines.append("## Input Files")
    lines.append("")
    lines.append(f"- Check results CSV: `{context['input_files']['check_results_csv']}`")
    lines.append(f"- Features CSV: `{context['input_files']['features_csv']}`")
    lines.append(f"- AI readiness CSV: `{context['input_files']['ai_readiness_csv']}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total violations: {summary['total_violations']}")
    lines.append(f"- Total elements: {summary['total_elements']}")
    lines.append(f"- Average AI Readiness Score: {summary['average_ai_readiness_score']}")
    lines.append(f"- Human Review Required Count: {summary['human_review_required_count']}")
    lines.append("")
    lines.append("## Rule Summary")
    lines.append("")
    lines.append("| RuleId | RuleName | Severity | ViolationCount |")
    lines.append("|---|---|---|---:|")

    for row in summary["rule_summary"]:
        lines.append(
            f"| {row['RuleId']} | {row['RuleName']} | {row['Severity']} | {row['ViolationCount']} |"
        )

    lines.append("")
    lines.append("## FixPriority Summary")
    lines.append("")
    lines.append("| FixPriority | Count |")
    lines.append("|---|---:|")

    for row in summary["fix_priority_summary"]:
        lines.append(f"| {row['FixPriority']} | {row['Count']} |")

    lines.append("")
    lines.append("## AI Readiness Level Summary")
    lines.append("")
    lines.append("| AIReadinessLevel | Count |")
    lines.append("|---|---:|")

    for row in summary["ai_readiness_level_summary"]:
        lines.append(f"| {row['AIReadinessLevel']} | {row['Count']} |")

    lines.append("")
    lines.append("## Sample Element Context")
    lines.append("")

    sample_elements = context["elements"][:3]

    for item in sample_elements:
        element = item["element"]
        quality = item["quality_summary"]
        ai_readiness = item["ai_readiness"]

        lines.append(f"### ElementId: {element['element_id']}")
        lines.append("")
        lines.append(f"- Category: {element['category']}")
        lines.append(f"- FamilyName: {element['family_name']}")
        lines.append(f"- TypeName: {element['type_name']}")
        lines.append(f"- QualityScore: {quality['quality_score']}")
        lines.append(f"- FixPriority: {quality['fix_priority']}")
        lines.append(f"- RuleViolationCount: {quality['rule_violation_count']}")
        lines.append(f"- AIReadinessScore: {ai_readiness['ai_readiness_score']}")
        lines.append(f"- AIReadinessLevel: {ai_readiness['ai_readiness_level']}")
        lines.append(
            f"- AIReadinessPenaltyTotal: {ai_readiness['ai_readiness_penalty_total']}"
        )
        lines.append(
            f"- BlockingRuleIds: {', '.join(ai_readiness['blocking_rule_ids'])}"
        )
        lines.append(
            f"- HumanReviewRequired: {ai_readiness['human_review_required']}"
        )
        lines.append("")

        lines.append("| RuleId | RuleName | Severity | ParameterName | FixGuide |")
        lines.append("|---|---|---|---|---|")

        for violation in item["violations"]:
            lines.append(
                f"| {violation['rule_id']} | {violation['rule_name']} | {violation['severity']} | {violation['parameter_name']} | {violation['fix_guide']} |"
            )

        lines.append("")

    lines.append("## Limitations")
    lines.append("")

    for limitation in context["limitations"]:
        lines.append(f"- {limitation}")

    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")


# =========================================
# Main process
# =========================================

def main() -> None:
    print("AI context generation started.")

    validate_input_files()

    print(f"Check results file: {CHECK_RESULTS_CSV}")
    print(f"Features file: {FEATURES_CSV}")
    print(f"AI readiness file: {AI_READINESS_CSV}")

    check_results_df, features_df, ai_readiness_df = load_data()

    print(f"Check results shape: {check_results_df.shape}")
    print(f"Features shape: {features_df.shape}")
    print(f"AI readiness shape: {ai_readiness_df.shape}")

    summary_context = build_summary_context(
        check_results_df,
        features_df,
        ai_readiness_df,
    )
    element_contexts = build_element_context(
        check_results_df,
        features_df,
        ai_readiness_df,
    )

    context = {
        **summary_context,
        "elements": element_contexts,
    }

    save_json_context(context)
    save_markdown_context(context)

    print(f"Element contexts: {len(element_contexts)}")
    print(f"JSON output file: {OUTPUT_JSON}")
    print(f"Markdown output file: {OUTPUT_MD}")
    print("AI context generation completed.")


if __name__ == "__main__":
    main()