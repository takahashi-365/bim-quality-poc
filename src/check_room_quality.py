from pathlib import Path

import pandas as pd


ROOM_DATA_PATH = Path("03_input_csv/cleaned_room_data_v001.csv")
RULE_MASTER_PATH = Path("02_rule_master/bim_rule_master_v003.csv")
OUTPUT_PATH = Path("04_output_csv/check_results_room_v001.csv")


def is_blank(value: object) -> bool:
    if pd.isna(value):
        return True
    return str(value).strip() == ""


def load_room_rules(rule_master_path: Path = RULE_MASTER_PATH) -> pd.DataFrame:
    rules = pd.read_csv(rule_master_path, dtype=str, encoding="utf-8-sig").fillna("")
    return rules[rules["TargetCategory"] == "Room"].copy()


def check_room_quality(
    room_data_path: Path = ROOM_DATA_PATH,
    rule_master_path: Path = RULE_MASTER_PATH,
    output_path: Path = OUTPUT_PATH,
) -> pd.DataFrame:
    rooms = pd.read_csv(room_data_path, dtype=str, encoding="utf-8-sig").fillna("")
    rules = load_room_rules(rule_master_path)

    results = []

    rule_map = {row["RuleId"]: row for _, row in rules.iterrows()}

    for _, room in rooms.iterrows():
        element_id = room.get("ElementId", "")
        category = room.get("Category", "")

        if category != "Room":
            continue

        checks = {
            "R-101": is_blank(room.get("RoomName", "")),
            "R-102": is_blank(room.get("RoomNumber", "")),
            "R-103": is_blank(room.get("Area", "")) or float(room.get("Area", 0) or 0) == 0,
            "R-104": is_blank(room.get("Level", "")),
        }

        for rule_id, is_violation in checks.items():
            if not is_violation:
                continue

            rule = rule_map.get(rule_id)

            if rule is None:
                continue

            results.append(
                {
                    "ElementId": element_id,
                    "Category": category,
                    "RuleId": rule_id,
                    "RuleName": rule.get("RuleName", ""),
                    "Severity": rule.get("Severity", ""),
                    "TargetField": rule.get("TargetField", ""),
                    "CheckResult": "NG",
                    "BusinessImpact": rule.get("BusinessImpact", ""),
                    "AIUseImpact": rule.get("AIUseImpact", ""),
                    "FixGuide": rule.get("FixGuide", ""),
                    "AIReadinessImpact": rule.get("AIReadinessImpact", ""),
                    "AIReadinessPenalty": rule.get("AIReadinessPenalty", ""),
                }
            )

    results_df = pd.DataFrame(results)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    return results_df


if __name__ == "__main__":
    results = check_room_quality()
    print(f"Room quality check results: {len(results)}")
    print(f"Output: {OUTPUT_PATH}")

    if len(results) > 0:
        print(results.head(20).to_string(index=False))