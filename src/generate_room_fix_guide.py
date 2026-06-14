from pathlib import Path

import pandas as pd


CHECK_RESULTS_PATH = Path("04_output_csv/check_results_room_v001.csv")
AI_READINESS_PATH = Path("04_output_csv/room_ai_readiness_scores_v001.csv")
OUTPUT_PATH = Path("04_output_csv/room_fix_guides_v001.md")


def safe_value(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value)


def validate_columns(df: pd.DataFrame, required_columns: list[str], file_label: str) -> None:
    missing_columns = [column for column in required_columns if column not in df.columns]

    if missing_columns:
        raise ValueError(f"{file_label} is missing required columns: {missing_columns}")


def generate_room_fix_guide(
    check_results_path: Path = CHECK_RESULTS_PATH,
    ai_readiness_path: Path = AI_READINESS_PATH,
    output_path: Path = OUTPUT_PATH,
) -> None:
    check_results = pd.read_csv(
        check_results_path,
        dtype=str,
        encoding="utf-8-sig",
    ).fillna("")

    ai_readiness = pd.read_csv(
        ai_readiness_path,
        dtype=str,
        encoding="utf-8-sig",
    ).fillna("")

    validate_columns(
        check_results,
        [
            "ElementId",
            "Category",
            "RuleId",
            "RuleName",
            "Severity",
            "TargetField",
            "BusinessImpact",
            "AIUseImpact",
            "FixGuide",
        ],
        "check_results_room_v001.csv",
    )

    validate_columns(
        ai_readiness,
        [
            "ElementId",
            "Level",
            "RoomName",
            "RoomNumber",
            "Area",
            "AIReadinessScore",
            "AIReadinessLevel",
            "HumanReviewRequired",
        ],
        "room_ai_readiness_scores_v001.csv",
    )

    merged = check_results.merge(
        ai_readiness[
            [
                "ElementId",
                "Level",
                "RoomName",
                "RoomNumber",
                "Area",
                "AIReadinessScore",
                "AIReadinessLevel",
                "HumanReviewRequired",
            ]
        ],
        on="ElementId",
        how="left",
    ).fillna("")

    lines: list[str] = []

    lines.append("# Room Fix Guides v001")
    lines.append("")
    lines.append("This file provides RuleId-based fix guide notes for Room data quality issues in Phase 3B.")
    lines.append("")
    lines.append("> This guide is reference information for BIM data review. It does not make design or construction decisions. Final judgment must be made by BIM personnel.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total violation records: {len(merged)}")
    lines.append(f"- Target category: Room")
    lines.append("")

    if merged.empty:
        lines.append("No Room rule violations were detected.")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("\n".join(lines), encoding="utf-8")
        return

    for element_id, group in merged.groupby("ElementId", sort=True):
        first = group.iloc[0]

        lines.append(f"## ElementId: {safe_value(element_id)}")
        lines.append("")
        lines.append(f"- Category: Room")
        lines.append(f"- Level: {safe_value(first.get('Level', ''))}")
        lines.append(f"- RoomName: {safe_value(first.get('RoomName', ''))}")
        lines.append(f"- RoomNumber: {safe_value(first.get('RoomNumber', ''))}")
        lines.append(f"- Area: {safe_value(first.get('Area', ''))}")
        lines.append(f"- AIReadinessScore: {safe_value(first.get('AIReadinessScore', ''))}")
        lines.append(f"- AIReadinessLevel: {safe_value(first.get('AIReadinessLevel', ''))}")
        lines.append(f"- HumanReviewRequired: {safe_value(first.get('HumanReviewRequired', ''))}")
        lines.append("")
        lines.append("### Fix Guide")
        lines.append("")

        for _, row in group.iterrows():
            lines.append(f"#### {safe_value(row.get('RuleId', ''))} {safe_value(row.get('RuleName', ''))}")
            lines.append("")
            lines.append(f"- Severity: {safe_value(row.get('Severity', ''))}")
            lines.append(f"- TargetField: {safe_value(row.get('TargetField', ''))}")
            lines.append(f"- BusinessImpact: {safe_value(row.get('BusinessImpact', ''))}")
            lines.append(f"- AIUseImpact: {safe_value(row.get('AIUseImpact', ''))}")
            lines.append(f"- RecommendedFix: {safe_value(row.get('FixGuide', ''))}")
            lines.append("")

        lines.append("### Notes")
        lines.append("")
        lines.append("- Room ElementId is a temporary PoC identifier, not Revit internal ElementId or UniqueId.")
        lines.append("- Do not automatically modify the Revit model based on this guide.")
        lines.append("- Final judgment must be made by BIM personnel.")
        lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    generate_room_fix_guide()
    print(f"Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()