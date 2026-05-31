# このファイルの目的：
# BIM品質チェック結果、品質メトリクス、特徴量データセットをもとに、
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

OUTPUT_JSON = BASE_DIR / "04_output_csv" / "ai_context_v001.json"
OUTPUT_MD = BASE_DIR / "04_output_csv" / "ai_context_v001.md"


# =========================================
# Helper functions
# =========================================

def validate_input_files() -> None:
    """Validate that required input files exist."""
    if not CHECK_RESULTS_CSV.exists():
        raise FileNotFoundError(f"Check results CSV not found: {CHECK_RESULTS_CSV}")

    if not FEATURES_CSV.exists():
        raise FileNotFoundError(f"Features CSV not found: {FEATURES_CSV}")


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load check results and feature dataset."""
    check_results_df = pd.read_csv(CHECK_RESULTS_CSV, encoding="utf-8-sig")
    features_df = pd.read_csv(FEATURES_CSV, encoding="utf-8-sig")

    return check_results_df, features_df


def safe_value(value) -> str:
    """Convert NaN to empty string and return a JSON-safe value."""
    if pd.isna(value):
        return ""
    return value


def build_element_context(
    check_results_df: pd.DataFrame,
    features_df: pd.DataFrame,
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

    missing_check_columns = [
        col for col in required_check_columns if col not in check_results_df.columns
    ]
    if missing_check_columns:
        raise ValueError(f"Missing columns in check results: {missing_check_columns}")

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

    missing_feature_columns = [
        col for col in required_feature_columns if col not in features_df.columns
    ]
    if missing_feature_columns:
        raise ValueError(f"Missing columns in features: {missing_feature_columns}")

    contexts = []

    for _, feature_row in features_df.iterrows():
        element_id = feature_row["ElementId"]

        element_checks = check_results_df[
            check_results_df["ElementId"] == element_id
        ].copy()

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
                "rule_violation_count": int(feature_row.get("RuleViolationCount", 0)),
                "missing_field_count": int(feature_row.get("MissingFieldCount", 0)),
                "high_violation_count": int(feature_row.get("HighViolationCount", 0)),
                "medium_violation_count": int(feature_row.get("MediumViolationCount", 0)),
                "low_violation_count": int(feature_row.get("LowViolationCount", 0)),
                "severity_score": int(feature_row.get("SeverityScore", 0)),
                "quality_score": int(feature_row.get("QualityScore", 0)),
                "fix_priority": safe_value(feature_row.get("FixPriority", "")),
            },
            "violations": violations,
            "ai_instruction": {
                "role": "BIM data quality assistant",
                "task": "Explain detected BIM data quality issues and suggest human-review-oriented fix actions.",
                "constraints": [
                    "Do not assume information that is not included in the context.",
                    "Do not claim that the model can be automatically fixed.",
                    "Use RuleId, Severity, FixGuide, QualityScore, and FixPriority as the primary reference information.",
                    "Explain that final design or model correction decisions should be made by a human reviewer.",
                ],
            },
        }

        contexts.append(context)

    return contexts


def build_summary_context(
    check_results_df: pd.DataFrame,
    features_df: pd.DataFrame,
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

    return {
        "project": {
            "name": "BIM Data Quality Engineering & AI Analysis PoC",
            "purpose": "Prepare BIM quality check results as structured context for generative AI usage.",
            "note": "This context is generated for PoC purposes. It is not a production AI system.",
        },
        "input_files": {
            "check_results_csv": str(CHECK_RESULTS_CSV.relative_to(BASE_DIR)),
            "features_csv": str(FEATURES_CSV.relative_to(BASE_DIR)),
        },
        "summary": {
            "total_violations": int(len(check_results_df)),
            "total_elements": int(features_df["ElementId"].nunique()),
            "rule_summary": rule_summary.to_dict(orient="records"),
            "fix_priority_summary": fix_priority_summary.to_dict(orient="records"),
        },
        "limitations": [
            "QualityScore is a simple PoC metric, not an official business quality standard.",
            "FixPriority is a provisional label, not a verified business ground truth.",
            "The generated context is intended to support human review, not automate BIM model correction.",
            "Revit API and pyRevit integration are not implemented in this stage.",
        ],
    }


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

    lines.append("# AI Context v001")
    lines.append("")
    lines.append("## Project")
    lines.append("")
    lines.append(f"- Name: {project['name']}")
    lines.append(f"- Purpose: {project['purpose']}")
    lines.append(f"- Note: {project['note']}")
    lines.append("")
    lines.append("## Input Files")
    lines.append("")
    lines.append(f"- Check results CSV: `{context['input_files']['check_results_csv']}`")
    lines.append(f"- Features CSV: `{context['input_files']['features_csv']}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total violations: {summary['total_violations']}")
    lines.append(f"- Total elements: {summary['total_elements']}")
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
    lines.append("## Sample Element Context")
    lines.append("")

    sample_elements = context["elements"][:3]

    for item in sample_elements:
        element = item["element"]
        quality = item["quality_summary"]

        lines.append(f"### ElementId: {element['element_id']}")
        lines.append("")
        lines.append(f"- Category: {element['category']}")
        lines.append(f"- FamilyName: {element['family_name']}")
        lines.append(f"- TypeName: {element['type_name']}")
        lines.append(f"- QualityScore: {quality['quality_score']}")
        lines.append(f"- FixPriority: {quality['fix_priority']}")
        lines.append(f"- RuleViolationCount: {quality['rule_violation_count']}")
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

    check_results_df, features_df = load_data()

    print(f"Check results shape: {check_results_df.shape}")
    print(f"Features shape: {features_df.shape}")

    summary_context = build_summary_context(check_results_df, features_df)
    element_contexts = build_element_context(check_results_df, features_df)

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