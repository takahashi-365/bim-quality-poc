from pathlib import Path
import json

import pandas as pd


ROOM_DATA_PATH = Path("03_input_csv/cleaned_room_data_v001.csv")
CHECK_RESULTS_PATH = Path("04_output_csv/check_results_room_v001.csv")
AI_READINESS_PATH = Path("04_output_csv/room_ai_readiness_scores_v001.csv")

OUTPUT_JSON = Path("04_output_csv/room_ai_context_v001.json")
OUTPUT_MD = Path("04_output_csv/room_ai_context_v001.md")


def safe_value(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value)


def validate_columns(df: pd.DataFrame, required_columns: list[str], file_label: str) -> None:
    missing_columns = [column for column in required_columns if column not in df.columns]

    if missing_columns:
        raise ValueError(f"{file_label} is missing required columns: {missing_columns}")


def build_rule_context(check_results: pd.DataFrame) -> dict[str, list[dict[str, str]]]:
    rule_context: dict[str, list[dict[str, str]]] = {}

    for _, row in check_results.iterrows():
        element_id = safe_value(row.get("ElementId", ""))

        rule_context.setdefault(element_id, []).append(
            {
                "RuleId": safe_value(row.get("RuleId", "")),
                "RuleName": safe_value(row.get("RuleName", "")),
                "Severity": safe_value(row.get("Severity", "")),
                "TargetField": safe_value(row.get("TargetField", "")),
                "CheckResult": safe_value(row.get("CheckResult", "")),
                "BusinessImpact": safe_value(row.get("BusinessImpact", "")),
                "AIUseImpact": safe_value(row.get("AIUseImpact", "")),
                "FixGuide": safe_value(row.get("FixGuide", "")),
            }
        )

    return rule_context


def generate_room_ai_context(
    room_data_path: Path = ROOM_DATA_PATH,
    check_results_path: Path = CHECK_RESULTS_PATH,
    ai_readiness_path: Path = AI_READINESS_PATH,
) -> list[dict[str, object]]:
    room_data = pd.read_csv(room_data_path, dtype=str, encoding="utf-8-sig").fillna("")
    check_results = pd.read_csv(check_results_path, dtype=str, encoding="utf-8-sig").fillna("")
    ai_readiness = pd.read_csv(ai_readiness_path, dtype=str, encoding="utf-8-sig").fillna("")

    validate_columns(
        room_data,
        [
            "ElementId",
            "Category",
            "Level",
            "RoomName",
            "RoomNumber",
            "AreaRaw",
            "Area",
        ],
        "cleaned_room_data_v001.csv",
    )

    validate_columns(
        ai_readiness,
        [
            "ElementId",
            "AIReadinessScore",
            "AIReadinessLevel",
            "HumanReviewRequired",
            "BlockingRuleIds",
        ],
        "room_ai_readiness_scores_v001.csv",
    )

    validate_columns(
        check_results,
        [
            "ElementId",
            "RuleId",
            "RuleName",
            "Severity",
            "TargetField",
            "CheckResult",
            "BusinessImpact",
            "AIUseImpact",
            "FixGuide",
        ],
        "check_results_room_v001.csv",
    )

    rule_context = build_rule_context(check_results)

    merged = room_data.merge(
        ai_readiness[
            [
                "ElementId",
                "RuleViolationCount",
                "AIReadinessPenaltyTotal",
                "BlockingRuleIds",
                "AIReadinessScore",
                "AIReadinessLevel",
                "HumanReviewRequired",
            ]
        ],
        on="ElementId",
        how="left",
    ).fillna("")

    contexts: list[dict[str, object]] = []

    for _, row in merged.iterrows():
        element_id = safe_value(row.get("ElementId", ""))

        contexts.append(
            {
                "ElementId": element_id,
                "Category": safe_value(row.get("Category", "")),
                "Room": {
                    "Level": safe_value(row.get("Level", "")),
                    "RoomName": safe_value(row.get("RoomName", "")),
                    "RoomNumber": safe_value(row.get("RoomNumber", "")),
                    "RoomAlias": safe_value(row.get("RoomAlias", "")),
                    "RoomGroupName": safe_value(row.get("RoomGroupName", "")),
                    "RoomGroupNumber": safe_value(row.get("RoomGroupNumber", "")),
                    "AreaRaw": safe_value(row.get("AreaRaw", "")),
                    "Area": safe_value(row.get("Area", "")),
                    "CH": safe_value(row.get("CH", "")),
                    "FloorFinish": safe_value(row.get("FloorFinish", "")),
                    "WallFinish": safe_value(row.get("WallFinish", "")),
                    "CeilingFinish": safe_value(row.get("CeilingFinish", "")),
                    "Notes": safe_value(row.get("Notes", "")),
                },
                "QualityCheck": {
                    "RuleViolationCount": safe_value(row.get("RuleViolationCount", "0")),
                    "BlockingRuleIds": safe_value(row.get("BlockingRuleIds", "")),
                    "RuleResults": rule_context.get(element_id, []),
                },
                "AIReadiness": {
                    "AIReadinessScore": safe_value(row.get("AIReadinessScore", "")),
                    "AIReadinessLevel": safe_value(row.get("AIReadinessLevel", "")),
                    "AIReadinessPenaltyTotal": safe_value(
                        row.get("AIReadinessPenaltyTotal", "")
                    ),
                    "HumanReviewRequired": safe_value(row.get("HumanReviewRequired", "")),
                },
                "NotesForAIUse": [
                    "This context is generated from Revit Room Schedule data for PoC purposes.",
                    "Room ElementId is a temporary PoC identifier, not Revit internal ElementId or UniqueId.",
                    "The output does not make design or construction decisions.",
                    "Final judgment must be made by BIM personnel.",
                ],
            }
        )

    return contexts


def write_json(contexts: list[dict[str, object]], output_path: Path = OUTPUT_JSON) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(contexts, file, ensure_ascii=False, indent=2)


def write_markdown(contexts: list[dict[str, object]], output_path: Path = OUTPUT_MD) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    lines.append("# Room AI Context v001")
    lines.append("")
    lines.append("This file summarizes Room data quality and AI Readiness context for Phase 3B.")
    lines.append("")
    lines.append("> This context is reference information for BIM data review. Final judgment must be made by BIM personnel.")
    lines.append("")

    for context in contexts:
        room = context["Room"]
        quality = context["QualityCheck"]
        ai_readiness = context["AIReadiness"]

        lines.append(f"## ElementId: {context['ElementId']}")
        lines.append("")
        lines.append(f"- Category: {context['Category']}")
        lines.append(f"- Level: {room['Level']}")
        lines.append(f"- RoomName: {room['RoomName']}")
        lines.append(f"- RoomNumber: {room['RoomNumber']}")
        lines.append(f"- Area: {room['Area']}")
        lines.append(f"- AIReadinessScore: {ai_readiness['AIReadinessScore']}")
        lines.append(f"- AIReadinessLevel: {ai_readiness['AIReadinessLevel']}")
        lines.append(f"- HumanReviewRequired: {ai_readiness['HumanReviewRequired']}")
        lines.append(f"- BlockingRuleIds: {quality['BlockingRuleIds']}")
        lines.append("")

        rule_results = quality["RuleResults"]

        if rule_results:
            lines.append("### Rule Results")
            lines.append("")
            for rule in rule_results:
                lines.append(
                    f"- {rule['RuleId']} {rule['RuleName']} "
                    f"({rule['Severity']}): {rule['FixGuide']}"
                )
            lines.append("")
        else:
            lines.append("### Rule Results")
            lines.append("")
            lines.append("- No rule violations detected.")
            lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    contexts = generate_room_ai_context()
    write_json(contexts)
    write_markdown(contexts)

    print(f"Contexts: {len(contexts)}")
    print(f"Output: {OUTPUT_JSON}")
    print(f"Output: {OUTPUT_MD}")


if __name__ == "__main__":
    main()