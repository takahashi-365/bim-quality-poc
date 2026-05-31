# このファイルの目的：
# BIMデータを読み込み、RuleIdに基づいて品質チェックを行い、
# チェック結果をCSVとして出力するための処理。
#
# 主な処理フロー：
# 1. 入力データを読み込む
# 2. BIM品質ルールマスターを読み込み、RuleIdに対応するルールを取得する
# 3. 各データに対して品質チェックを行う
# 4. 違反内容やRuleIdを整理する
# 5. チェック結果をCSVとして出力する

import pandas as pd
from datetime import datetime
from pathlib import Path


# =========================================
# Path settings
# =========================================

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_CSV = BASE_DIR / "03_input_csv" / "door_schedule_converted_v001.csv"
RULE_MASTER_CSV = BASE_DIR / "02_rule_master" / "bim_rule_master_v001.csv"
OUTPUT_CSV = BASE_DIR / "04_output_csv" / "check_results_revit_v001.csv"


# =========================================
# Helper functions
# =========================================

def is_blank(value) -> bool:
    """Return True if the value is empty or NaN."""
    if pd.isna(value):
        return True
    return str(value).strip() == ""


def get_rule(rule_master: pd.DataFrame, rule_id: str) -> dict:
    """Get a rule row from the rule master."""
    rule = rule_master[rule_master["RuleId"] == rule_id]
    if rule.empty:
        raise ValueError(f"RuleId not found in rule master: {rule_id}")
    return rule.iloc[0].to_dict()


def add_result(
    results: list,
    row: pd.Series,
    rule: dict,
    parameter_name: str,
    current_value
) -> None:
    """Add one check result."""
    results.append({
        "CheckId": f"CHK-{len(results) + 1:04d}",
        "ElementId": row.get("ElementId", ""),
        "Category": row.get("Category", ""),
        "FamilyName": row.get("FamilyName", ""),
        "TypeName": row.get("TypeName", ""),
        "Level": row.get("Level", ""),
        "ParameterName": parameter_name,
        "CurrentValue": "" if pd.isna(current_value) else current_value,
        "RuleId": rule.get("RuleId", ""),
        "RuleName": rule.get("RuleName", ""),
        "Severity": rule.get("Severity", ""),
        "Status": "Open",
        "FixGuide": rule.get("FixGuide", ""),
        "DetectedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "SourceFile": row.get("SourceFile", ""),
        "ModelName": row.get("ModelName", "")
    })


# =========================================
# Check functions
# =========================================

def check_required_parameters(row: pd.Series, rule_master: pd.DataFrame, results: list) -> None:
    """R-001: Required parameter blank check."""
    rule = get_rule(rule_master, "R-001")

    for field in ["BIM_ModelRole", "BIM_Zone"]:
        value = row.get(field, "")
        if is_blank(value):
            add_result(results, row, rule, field, value)


def check_classification_code(row: pd.Series, rule_master: pd.DataFrame, results: list) -> None:
    """R-002: Classification code blank check."""
    rule = get_rule(rule_master, "R-002")

    field = "BIM_ClassificationCode"
    value = row.get(field, "")

    if is_blank(value):
        add_result(results, row, rule, field, value)


def check_family_naming(row: pd.Series, rule_master: pd.DataFrame, results: list) -> None:
    """R-003: Family name prefix check by category."""
    rule = get_rule(rule_master, "R-003")

    category = str(row.get("Category", "")).strip()
    family_name = str(row.get("FamilyName", "")).strip()

    prefix_rules = {
        "Doors": "DR_",
        "Rooms": "RM_",
        "Walls": "WAL_"
    }

    expected_prefix = prefix_rules.get(category)

    # If the category is not included in the initial rule, skip it.
    if expected_prefix is None:
        return

    if not family_name.startswith(expected_prefix):
        add_result(results, row, rule, "FamilyName", family_name)


# =========================================
# Main process
# =========================================

def main() -> None:
    print("BIM quality check started.")

    if not INPUT_CSV.exists():
        raise FileNotFoundError(f"Input CSV not found: {INPUT_CSV}")

    if not RULE_MASTER_CSV.exists():
        raise FileNotFoundError(f"Rule master CSV not found: {RULE_MASTER_CSV}")

    input_df = pd.read_csv(INPUT_CSV, encoding="utf-8-sig")
    rule_master_df = pd.read_csv(RULE_MASTER_CSV, encoding="utf-8-sig")

    results = []

    for _, row in input_df.iterrows():
        check_required_parameters(row, rule_master_df, results)
        check_classification_code(row, rule_master_df, results)
        check_family_naming(row, rule_master_df, results)

    output_df = pd.DataFrame(results)

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    output_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    print(f"Check completed. Results: {len(output_df)} issues found.")
    print(f"Output file: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()