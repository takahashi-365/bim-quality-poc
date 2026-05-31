# このファイルの目的：
# BIM品質チェック結果CSVとElementId別集計CSVを読み込み、
# 機械学習や分析に使える特徴量データセットを作成する。
#
# このスクリプトは、7月応募可能MVPの中核成果物。
#
# 入力：
# - 04_output_csv/check_results_revit_v002.csv
# - 04_output_csv/element_summary_v001.csv
#
# 出力：
# - 04_output_csv/bim_features_v001.csv
#
# 現時点の注意：
# - FixPriorityはまだ本格的な教師ラベルではない
# - QualityScoreはPoC用の簡易スコア
# - 実務適用には修正履歴、修正工数、担当者判断などの教師データが必要

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

CHECK_RESULTS_CSV = BASE_DIR / "04_output_csv" / "check_results_revit_v002.csv"
ELEMENT_SUMMARY_CSV = BASE_DIR / "04_output_csv" / "element_summary_v001.csv"

OUTPUT_FEATURES_CSV = BASE_DIR / "04_output_csv" / "bim_features_v001.csv"


REQUIRED_PARAMETER_FIELDS = [
    "BIM_ModelRole",
    "BIM_Zone",
    "BIM_ClassificationCode",
]


def read_csv_file(path: Path, label: str) -> pd.DataFrame:
    """CSVを読み込む。"""
    if not path.exists():
        raise FileNotFoundError(f"{label} not found: {path}")

    return pd.read_csv(path, encoding="utf-8-sig")


def create_missing_field_count(check_results_df: pd.DataFrame) -> pd.DataFrame:
    """
    ElementIdごとの未入力項目数を作成する。

    対象：
    - BIM_ModelRole
    - BIM_Zone
    - BIM_ClassificationCode
    """
    target_df = check_results_df[
        check_results_df["ParameterName"].isin(REQUIRED_PARAMETER_FIELDS)
    ].copy()

    summary = (
        target_df.groupby("ElementId", dropna=False)
        .size()
        .reset_index(name="MissingFieldCount")
    )

    return summary


def create_rule_violation_flags(check_results_df: pd.DataFrame) -> pd.DataFrame:
    """
    ElementIdごとのRuleId別違反有無を作成する。

    例：
    - HasR001Violation
    - HasR002Violation
    - HasR003Violation
    """
    work_df = check_results_df.copy()

    work_df["HasViolation"] = 1

    pivot_df = (
        work_df.pivot_table(
            index="ElementId",
            columns="RuleId",
            values="HasViolation",
            aggfunc="max",
            fill_value=0,
        )
        .reset_index()
    )

    rename_map = {
        "R-001": "HasR001Violation",
        "R-002": "HasR002Violation",
        "R-003": "HasR003Violation",
    }

    pivot_df = pivot_df.rename(columns=rename_map)

    for column in ["HasR001Violation", "HasR002Violation", "HasR003Violation"]:
        if column not in pivot_df.columns:
            pivot_df[column] = 0

    return pivot_df[
        [
            "ElementId",
            "HasR001Violation",
            "HasR002Violation",
            "HasR003Violation",
        ]
    ]


def create_severity_counts(check_results_df: pd.DataFrame) -> pd.DataFrame:
    """
    ElementIdごとの重大度別違反件数を作成する。

    出力：
    - HighViolationCount
    - MediumViolationCount
    - LowViolationCount
    """
    work_df = check_results_df.copy()
    work_df["Count"] = 1

    pivot_df = (
        work_df.pivot_table(
            index="ElementId",
            columns="Severity",
            values="Count",
            aggfunc="sum",
            fill_value=0,
        )
        .reset_index()
    )

    rename_map = {
        "High": "HighViolationCount",
        "Medium": "MediumViolationCount",
        "Low": "LowViolationCount",
    }

    pivot_df = pivot_df.rename(columns=rename_map)

    for column in ["HighViolationCount", "MediumViolationCount", "LowViolationCount"]:
        if column not in pivot_df.columns:
            pivot_df[column] = 0

    return pivot_df[
        [
            "ElementId",
            "HighViolationCount",
            "MediumViolationCount",
            "LowViolationCount",
        ]
    ]


def add_classification_and_family_features(features_df: pd.DataFrame) -> pd.DataFrame:
    """
    分類コード有無、ファミリ名適合有無を特徴量として追加する。

    現時点では、以下のルールで作成する。
    - HasClassificationCode: R-002違反がなければ1、あれば0
    - FamilyNameValid: R-003違反がなければ1、あれば0
    """
    features_df["HasClassificationCode"] = (
        1 - features_df["HasR002Violation"]
    ).clip(lower=0, upper=1)

    features_df["FamilyNameValid"] = (
        1 - features_df["HasR003Violation"]
    ).clip(lower=0, upper=1)

    return features_df


def create_fix_priority_label(features_df: pd.DataFrame) -> pd.DataFrame:
    """
    修正優先度の仮ラベルを作成する。

    現時点では実務の正解ラベルがないため、
    QualityScoreとHighViolationCountをもとにした仮ラベルとする。

    仮ルール：
    - High: QualityScore <= 65 または HighViolationCount >= 3
    - Medium: QualityScore <= 85
    - Low: それ以外
    """
    def assign_priority(row: pd.Series) -> str:
        quality_score = row.get("QualityScore", 100)
        high_count = row.get("HighViolationCount", 0)

        if quality_score <= 65 or high_count >= 3:
            return "High"

        if quality_score <= 85:
            return "Medium"

        return "Low"

    features_df["FixPriority"] = features_df.apply(assign_priority, axis=1)

    return features_df


def create_bim_features(
    check_results_df: pd.DataFrame,
    element_summary_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    BIM特徴量データセットを作成する。
    """
    features_df = element_summary_df.copy()

    missing_count_df = create_missing_field_count(check_results_df)
    rule_flags_df = create_rule_violation_flags(check_results_df)
    severity_counts_df = create_severity_counts(check_results_df)

    features_df = features_df.merge(missing_count_df, on="ElementId", how="left")
    features_df = features_df.merge(rule_flags_df, on="ElementId", how="left")
    features_df = features_df.merge(severity_counts_df, on="ElementId", how="left")

    fill_zero_columns = [
        "MissingFieldCount",
        "HasR001Violation",
        "HasR002Violation",
        "HasR003Violation",
        "HighViolationCount",
        "MediumViolationCount",
        "LowViolationCount",
    ]

    for column in fill_zero_columns:
        if column not in features_df.columns:
            features_df[column] = 0
        features_df[column] = features_df[column].fillna(0).astype(int)

    features_df = add_classification_and_family_features(features_df)
    features_df = create_fix_priority_label(features_df)

    output_columns = [
        "ElementId",
        "Category",
        "FamilyName",
        "TypeName",
        "SourceFile",
        "ModelName",
        "RuleViolationCount",
        "MissingFieldCount",
        "HighViolationCount",
        "MediumViolationCount",
        "LowViolationCount",
        "HasClassificationCode",
        "FamilyNameValid",
        "SeverityScore",
        "QualityScore",
        "FixPriority",
    ]

    for column in output_columns:
        if column not in features_df.columns:
            features_df[column] = ""

    return features_df[output_columns].copy()


def save_csv(df: pd.DataFrame, output_path: Path) -> None:
    """CSVを出力する。"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")


def main() -> None:
    print("BIM feature creation started.")
    print(f"Check results file: {CHECK_RESULTS_CSV}")
    print(f"Element summary file: {ELEMENT_SUMMARY_CSV}")

    check_results_df = read_csv_file(CHECK_RESULTS_CSV, "Check results CSV")
    element_summary_df = read_csv_file(ELEMENT_SUMMARY_CSV, "Element summary CSV")

    print(f"Check results shape: {check_results_df.shape}")
    print(f"Element summary shape: {element_summary_df.shape}")

    features_df = create_bim_features(check_results_df, element_summary_df)

    save_csv(features_df, OUTPUT_FEATURES_CSV)

    print(f"Features shape: {features_df.shape}")
    print(f"Output file: {OUTPUT_FEATURES_CSV}")

    print("FixPriority counts:")
    print(features_df["FixPriority"].value_counts())

    print("BIM feature creation completed.")


if __name__ == "__main__":
    main()