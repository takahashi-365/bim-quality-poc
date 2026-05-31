# このファイルの目的：
# BIM品質チェック結果、品質メトリクス、RuleId別集計、Category別集計、
# ElementId別品質スコア、特徴量データセットをStreamlitで簡易表示する。
#
# この画面は、7月応募可能MVP用の簡易UI。
# 本格的な業務アプリではなく、PoCの処理結果を面接・ポートフォリオで説明しやすくするための画面。

from pathlib import Path

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parents[1]

CHECK_RESULTS_CSV = BASE_DIR / "04_output_csv" / "check_results_revit_v002.csv"
QUALITY_METRICS_CSV = BASE_DIR / "04_output_csv" / "quality_metrics_v001.csv"
RULE_SUMMARY_CSV = BASE_DIR / "04_output_csv" / "rule_summary_v001.csv"
CATEGORY_SUMMARY_CSV = BASE_DIR / "04_output_csv" / "category_summary_v001.csv"
ELEMENT_SUMMARY_CSV = BASE_DIR / "04_output_csv" / "element_summary_v001.csv"
BIM_FEATURES_CSV = BASE_DIR / "04_output_csv" / "bim_features_v001.csv"


st.set_page_config(
    page_title="BIM Data Quality Engineering & AI Analysis PoC",
    layout="wide",
)


def read_csv(path: Path) -> pd.DataFrame:
    """CSVを読み込む。ファイルがない場合は空DataFrameを返す。"""
    if not path.exists():
        st.warning(f"File not found: {path}")
        return pd.DataFrame()

    return pd.read_csv(path, encoding="utf-8-sig")


def get_metric_value(metrics_df: pd.DataFrame, metric_name: str, default_value=0):
    """quality_metrics_v001.csv から指定MetricNameの値を取得する。"""
    if metrics_df.empty:
        return default_value

    target = metrics_df[metrics_df["MetricName"] == metric_name]

    if target.empty:
        return default_value

    return target.iloc[0]["MetricValue"]


def convert_df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    """DataFrameをCSVダウンロード用のbytesに変換する。"""
    return df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")


def main() -> None:
    st.title("BIM Data Quality Engineering & AI Analysis PoC")

    st.write(
        "Revit/BIMデータをPythonで処理し、RuleIdベースの品質チェック、"
        "品質メトリクス作成、特徴量データセット作成へ接続する個人開発PoCです。"
    )

    st.info(
        "このStreamlit画面は、PoCの処理結果を確認するための簡易UIです。"
        "本格的な業務アプリではなく、面接・ポートフォリオ説明用のMVPとして位置づけます。"
    )

    check_results_df = read_csv(CHECK_RESULTS_CSV)
    quality_metrics_df = read_csv(QUALITY_METRICS_CSV)
    rule_summary_df = read_csv(RULE_SUMMARY_CSV)
    category_summary_df = read_csv(CATEGORY_SUMMARY_CSV)
    element_summary_df = read_csv(ELEMENT_SUMMARY_CSV)
    bim_features_df = read_csv(BIM_FEATURES_CSV)

    st.header("1. 品質メトリクス概要")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "総違反件数",
        get_metric_value(quality_metrics_df, "TotalIssues"),
    )
    col2.metric(
        "違反要素数",
        get_metric_value(quality_metrics_df, "TotalElementsWithIssues"),
    )
    col3.metric(
        "要素あたり平均違反件数",
        get_metric_value(quality_metrics_df, "AverageViolationsPerElement"),
    )
    col4.metric(
        "平均QualityScore",
        get_metric_value(quality_metrics_df, "AverageQualityScore"),
    )

    col5, col6, col7 = st.columns(3)

    col5.metric(
        "High違反件数",
        get_metric_value(quality_metrics_df, "HighSeverityCount"),
    )
    col6.metric(
        "Medium違反件数",
        get_metric_value(quality_metrics_df, "MediumSeverityCount"),
    )
    col7.metric(
        "Low違反件数",
        get_metric_value(quality_metrics_df, "LowSeverityCount"),
    )

    st.header("2. RuleId別違反件数")

    if not rule_summary_df.empty:
        st.dataframe(rule_summary_df, width="stretch")

        chart_df = rule_summary_df.set_index("RuleId")["ViolationCount"]
        st.bar_chart(chart_df)
    else:
        st.warning("RuleId別集計CSVが読み込めません。")

    st.header("3. Category別違反件数")

    if not category_summary_df.empty:
        st.dataframe(category_summary_df, width="stretch")

        chart_df = category_summary_df.set_index("Category")["ViolationCount"]
        st.bar_chart(chart_df)
    else:
        st.warning("Category別集計CSVが読み込めません。")

    st.header("4. ElementId別品質スコア")

    if not element_summary_df.empty:
        st.dataframe(element_summary_df, width="stretch")

        if "ElementId" in element_summary_df.columns and "QualityScore" in element_summary_df.columns:
            score_df = element_summary_df.set_index("ElementId")["QualityScore"]
            st.bar_chart(score_df)
    else:
        st.warning("ElementId別集計CSVが読み込めません。")

    st.header("5. 特徴量データセット")

    if not bim_features_df.empty:
        st.dataframe(bim_features_df, width="stretch")

        if "FixPriority" in bim_features_df.columns:
            st.subheader("FixPriority件数")
            st.dataframe(
                bim_features_df["FixPriority"].value_counts().reset_index(),
                width="stretch",
            )
    else:
        st.warning("特徴量データセットCSVが読み込めません。")

    st.header("6. 品質チェック結果一覧")

    if not check_results_df.empty:
        filter_col1, filter_col2, filter_col3 = st.columns(3)

        rule_ids = ["All"] + sorted(check_results_df["RuleId"].dropna().unique().tolist())
        severities = ["All"] + sorted(check_results_df["Severity"].dropna().unique().tolist())
        categories = ["All"] + sorted(check_results_df["Category"].dropna().unique().tolist())

        selected_rule_id = filter_col1.selectbox("RuleId", rule_ids)
        selected_severity = filter_col2.selectbox("Severity", severities)
        selected_category = filter_col3.selectbox("Category", categories)

        filtered_df = check_results_df.copy()

        if selected_rule_id != "All":
            filtered_df = filtered_df[filtered_df["RuleId"] == selected_rule_id]

        if selected_severity != "All":
            filtered_df = filtered_df[filtered_df["Severity"] == selected_severity]

        if selected_category != "All":
            filtered_df = filtered_df[filtered_df["Category"] == selected_category]

        st.dataframe(filtered_df, width="stretch")
    else:
        st.warning("品質チェック結果CSVが読み込めません。")

    st.header("7. CSVダウンロード")

    download_items = [
        ("品質チェック結果CSV", check_results_df, "check_results_revit_v002.csv"),
        ("品質メトリクスCSV", quality_metrics_df, "quality_metrics_v001.csv"),
        ("RuleId別集計CSV", rule_summary_df, "rule_summary_v001.csv"),
        ("Category別集計CSV", category_summary_df, "category_summary_v001.csv"),
        ("ElementId別集計CSV", element_summary_df, "element_summary_v001.csv"),
        ("特徴量データセットCSV", bim_features_df, "bim_features_v001.csv"),
    ]

    for label, df, filename in download_items:
        if not df.empty:
            st.download_button(
                label=f"{label}をダウンロード",
                data=convert_df_to_csv_bytes(df),
                file_name=filename,
                mime="text/csv",
            )

    st.header("8. 現時点の注意点")

    st.write("- この画面は7月応募可能MVP用の簡易UIです。")
    st.write("- QualityScoreはPoC用の簡易指標であり、実務上の正式な品質評価基準ではありません。")
    st.write("- FixPriorityは実務の正解ラベルではなく、QualityScoreとHigh違反件数をもとにした仮ラベルです。")
    st.write("- Revit APIやpyRevitとの直接連携、自動修正、生成AI API連携は現時点では未実装です。")


if __name__ == "__main__":
    main()