# このファイルの目的：
# BIMデータを読み込み、RuleIdに基づいて品質チェックを行い、
# チェック結果をCSVとして出力するための処理。
#
# v0.2の主な改善点：
# 1. 入力CSVを cleaned_bim_data_v001.csv に変更
# 2. 出力CSVを check_results_revit_v002.csv に変更
# 3. 入力件数、検出件数、RuleId別件数を表示
# 4. チェック結果の出力列順を固定
# 5. チェック結果が0件でも空のCSVを出力できるようにする
#
# 注意：
# 現時点のデータは、Revit由来データ対応の初期試作である。
# ElementId は Revit内部ElementId ではなく、建具表上の建具番号を仮IDとして使用している。
# FamilyName は Revitファミリ名ではなく、建具表上の種別記号 SD を仮格納している。
# TypeName は Revitタイプ名ではなく、設置場所・室名に近い列を仮格納している。

from datetime import datetime
from pathlib import Path

import pandas as pd


# =========================================
# Path settings
# =========================================

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_CSV = BASE_DIR / "03_input_csv" / "cleaned_bim_data_v001.csv"
RULE_MASTER_CSV = BASE_DIR / "02_rule_master" / "bim_rule_master_v002.csv"
OUTPUT_CSV = BASE_DIR / "04_output_csv" / "check_results_revit_v002.csv"


OUTPUT_COLUMNS = [
    "CheckId",
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
    "Status",
    "FixGuide",
    "DetectedAt",
    "SourceFile",
    "ModelName",
]


# =========================================
# Helper functions
# =========================================

def is_blank(value) -> bool:
    """Return True if the value is empty, NaN, or only spaces."""
    if pd.isna(value):
        return True
    return str(value).strip() == ""


def read_csv_file(path: Path, label: str) -> pd.DataFrame:
    """Read a CSV file with existence check."""
    if not path.exists():
        raise FileNotFoundError(f"{label} not found: {path}")

    return pd.read_csv(path, encoding="utf-8-sig")


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
    current_value,
) -> None:
    """Add one check result."""
    results.append(
        {
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
            "ModelName": row.get("ModelName", ""),
        }
    )


def create_output_dataframe(results: list) -> pd.DataFrame:
    """
    Create output DataFrame with fixed columns.
    Even if there are no results, output an empty CSV with headers.
    """
    if not results:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)

    output_df = pd.DataFrame(results)

    for column in OUTPUT_COLUMNS:
        if column not in output_df.columns:
            output_df[column] = ""

    return output_df[OUTPUT_COLUMNS].copy()


def print_rule_summary(output_df: pd.DataFrame) -> None:
    """Print issue counts by RuleId."""
    if output_df.empty:
        print("No issues found.")
        return

    print("Issues by RuleId:")

    rule_counts = output_df["RuleId"].value_counts().sort_index()

    for rule_id, count in rule_counts.items():
        print(f"  {rule_id}: {count}")


# =========================================
# Check functions
# =========================================

def check_required_parameters(
    row: pd.Series,
    rule_master: pd.DataFrame,
    results: list,
) -> None:
    """R-001: Required parameter blank check."""
    rule = get_rule(rule_master, "R-001")

    for field in ["BIM_ModelRole", "BIM_Zone"]:
        value = row.get(field, "")

        if is_blank(value):
            add_result(results, row, rule, field, value)


def check_classification_code(
    row: pd.Series,
    rule_master: pd.DataFrame,
    results: list,
) -> None:
    """R-002: Classification code blank check."""
    rule = get_rule(rule_master, "R-002")

    field = "BIM_ClassificationCode"
    value = row.get(field, "")

    if is_blank(value):
        add_result(results, row, rule, field, value)


def check_family_naming(
    row: pd.Series,
    rule_master: pd.DataFrame,
    results: list,
) -> None:
    """R-003: Family name prefix check by category."""
    rule = get_rule(rule_master, "R-003")

    category = str(row.get("Category", "")).strip()
    family_name = str(row.get("FamilyName", "")).strip()

    prefix_rules = {
        "Doors": "DR_",
        "Rooms": "RM_",
        "Walls": "WAL_",
    }

    expected_prefix = prefix_rules.get(category)

    # If the category is not included in the initial rule, skip it.
    if expected_prefix is None:
        return

    if not family_name.startswith(expected_prefix):
        add_result(results, row, rule, "FamilyName", family_name)


def run_quality_checks(
    input_df: pd.DataFrame,
    rule_master_df: pd.DataFrame,
) -> list:
    """Run all quality checks."""
    results = []

    for _, row in input_df.iterrows():
        check_required_parameters(row, rule_master_df, results)
        check_classification_code(row, rule_master_df, results)
        check_family_naming(row, rule_master_df, results)

    return results


def save_results(output_df: pd.DataFrame, output_path: Path) -> None:
    """Save check results to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_df.to_csv(output_path, index=False, encoding="utf-8-sig")


# =========================================
# Main process
# =========================================

def main() -> None:
    print("BIM quality check started.")
    print(f"Input file: {INPUT_CSV}")
    print(f"Rule master file: {RULE_MASTER_CSV}")

    input_df = read_csv_file(INPUT_CSV, "Input CSV")
    rule_master_df = read_csv_file(RULE_MASTER_CSV, "Rule master CSV")

    print(f"Input data shape: {input_df.shape}")
    print(f"Rule master shape: {rule_master_df.shape}")

    results = run_quality_checks(input_df, rule_master_df)

    output_df = create_output_dataframe(results)

    save_results(output_df, OUTPUT_CSV)

    print(f"Check completed. Results: {len(output_df)} issues found.")
    print_rule_summary(output_df)
    print(f"Output file: {OUTPUT_CSV}")
    print("BIM quality check completed.")


if __name__ == "__main__":
    main()