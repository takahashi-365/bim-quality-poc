# このファイルの目的：
# BIM品質チェック結果CSVを読み込み、
# 品質メトリクス、RuleId別集計、Category別集計、ElementId別集計を作成する。
#
# このスクリプトは、7月成果物である
# 「品質メトリクス作成」「特徴量データセット作成」へつなげるための前倒し試作。
#
# 入力：
# - 04_output_csv/check_results_revit_v002.csv
#
# 出力：
# - 04_output_csv/quality_metrics_v001.csv
# - 04_output_csv/rule_summary_v001.csv
# - 04_output_csv/category_summary_v001.csv
# - 04_output_csv/element_summary_v001.csv

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_CSV = BASE_DIR / "04_output_csv" / "check_results_revit_v002.csv"

OUTPUT_QUALITY_METRICS = BASE_DIR / "04_output_csv" / "quality_metrics_v001.csv"
OUTPUT_RULE_SUMMARY = BASE_DIR / "04_output_csv" / "rule_summary_v001.csv"
OUTPUT_CATEGORY_SUMMARY = BASE_DIR / "04_output_csv" / "category_summary_v001.csv"
OUTPUT_ELEMENT_SUMMARY = BASE_DIR / "04_output_csv" / "element_summary_v001.csv"


SEVERITY_SCORE_MAP = {
    "High": 10,
    "Medium": 5,
    "Low": 1,
}


def read_check_results(input_path: Path) -> pd.DataFrame:
    """品質チェック結果CSVを読み込む。"""
    if not input_path.exists():
        raise FileNotFoundError(f"Input CSV not found: {input_path}")

    return pd.read_csv(input_path, encoding="utf-8-sig")


def create_rule_summary(df: pd.DataFrame) -> pd.DataFrame:
    """RuleId別の違反件数を集計する。"""
    summary = (
        df.groupby(["RuleId", "RuleName", "Severity"], dropna=False)
        .size()
        .reset_index(name="ViolationCount")
        .sort_values(["RuleId"])
    )

    return summary


def create_category_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Category別の違反件数を集計する。"""
    summary = (
        df.groupby(["Category"], dropna=False)
        .size()
        .reset_index(name="ViolationCount")
        .sort_values(["ViolationCount"], ascending=False)
    )

    return summary


def create_element_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    ElementId別の違反件数、重大度スコア、簡易QualityScoreを作成する。

    QualityScoreの初期方針：
    - 初期値100点
    - High違反：10点減点
    - Medium違反：5点減点
    - Low違反：1点減点
    - 最低値は0点
    """
    work_df = df.copy()

    work_df["SeverityScore"] = work_df["Severity"].map(SEVERITY_SCORE_MAP).fillna(0)

    summary = (
        work_df.groupby(
            ["ElementId", "Category", "FamilyName", "TypeName", "SourceFile", "ModelName"],
            dropna=False,
        )
        .agg(
            RuleViolationCount=("RuleId", "count"),
            SeverityScore=("SeverityScore", "sum"),
        )
        .reset_index()
    )

    summary["QualityScore"] = 100 - summary["SeverityScore"]
    summary["QualityScore"] = summary["QualityScore"].clip(lower=0, upper=100)

    return summary


def create_quality_metrics(df: pd.DataFrame, element_summary: pd.DataFrame) -> pd.DataFrame:
    """PoC全体の品質メトリクスを作成する。"""
    total_issues = len(df)
    total_elements = element_summary["ElementId"].nunique()
    average_violations_per_element = (
        total_issues / total_elements if total_elements > 0 else 0
    )
    average_quality_score = (
        element_summary["QualityScore"].mean() if not element_summary.empty else 0
    )

    severity_counts = df["Severity"].value_counts().to_dict()
    rule_counts = df["RuleId"].value_counts().to_dict()

    metrics = [
        {
            "MetricName": "TotalIssues",
            "MetricValue": total_issues,
            "Description": "品質チェックで検出された総違反件数",
        },
        {
            "MetricName": "TotalElementsWithIssues",
            "MetricValue": total_elements,
            "Description": "違反が検出された要素数",
        },
        {
            "MetricName": "AverageViolationsPerElement",
            "MetricValue": round(average_violations_per_element, 2),
            "Description": "要素あたり平均違反件数",
        },
        {
            "MetricName": "AverageQualityScore",
            "MetricValue": round(average_quality_score, 2),
            "Description": "要素単位の平均品質スコア",
        },
        {
            "MetricName": "HighSeverityCount",
            "MetricValue": severity_counts.get("High", 0),
            "Description": "High重大度の違反件数",
        },
        {
            "MetricName": "MediumSeverityCount",
            "MetricValue": severity_counts.get("Medium", 0),
            "Description": "Medium重大度の違反件数",
        },
        {
            "MetricName": "LowSeverityCount",
            "MetricValue": severity_counts.get("Low", 0),
            "Description": "Low重大度の違反件数",
        },
        {
            "MetricName": "R001Count",
            "MetricValue": rule_counts.get("R-001", 0),
            "Description": "R-001 必須パラメータ未入力の違反件数",
        },
        {
            "MetricName": "R002Count",
            "MetricValue": rule_counts.get("R-002", 0),
            "Description": "R-002 分類コード未入力の違反件数",
        },
        {
            "MetricName": "R003Count",
            "MetricValue": rule_counts.get("R-003", 0),
            "Description": "R-003 ファミリ命名規則違反の違反件数",
        },
    ]

    return pd.DataFrame(metrics)


def save_csv(df: pd.DataFrame, output_path: Path) -> None:
    """CSVを出力する。"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")


def main() -> None:
    print("Quality metrics calculation started.")
    print(f"Input file: {INPUT_CSV}")

    check_results_df = read_check_results(INPUT_CSV)

    print(f"Input data shape: {check_results_df.shape}")

    rule_summary_df = create_rule_summary(check_results_df)
    category_summary_df = create_category_summary(check_results_df)
    element_summary_df = create_element_summary(check_results_df)
    quality_metrics_df = create_quality_metrics(check_results_df, element_summary_df)

    save_csv(quality_metrics_df, OUTPUT_QUALITY_METRICS)
    save_csv(rule_summary_df, OUTPUT_RULE_SUMMARY)
    save_csv(category_summary_df, OUTPUT_CATEGORY_SUMMARY)
    save_csv(element_summary_df, OUTPUT_ELEMENT_SUMMARY)

    print(f"Quality metrics output: {OUTPUT_QUALITY_METRICS}")
    print(f"Rule summary output: {OUTPUT_RULE_SUMMARY}")
    print(f"Category summary output: {OUTPUT_CATEGORY_SUMMARY}")
    print(f"Element summary output: {OUTPUT_ELEMENT_SUMMARY}")

    print(f"Rule summary shape: {rule_summary_df.shape}")
    print(f"Category summary shape: {category_summary_df.shape}")
    print(f"Element summary shape: {element_summary_df.shape}")
    print(f"Quality metrics shape: {quality_metrics_df.shape}")

    print("Quality metrics calculation completed.")


if __name__ == "__main__":
    main()