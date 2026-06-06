from pathlib import Path
import json

import pandas as pd
import streamlit as st


# =========================================
# Path settings
# =========================================

BASE_DIR = Path(__file__).resolve().parents[1]

QUALITY_METRICS_CSV = BASE_DIR / "04_output_csv" / "quality_metrics_v001.csv"
RULE_SUMMARY_CSV = BASE_DIR / "04_output_csv" / "rule_summary_v001.csv"
CATEGORY_SUMMARY_CSV = BASE_DIR / "04_output_csv" / "category_summary_v001.csv"
ELEMENT_SUMMARY_CSV = BASE_DIR / "04_output_csv" / "element_summary_v001.csv"
FEATURES_CSV = BASE_DIR / "04_output_csv" / "bim_features_v001.csv"
CHECK_RESULTS_CSV = BASE_DIR / "04_output_csv" / "check_results_revit_v002.csv"

CLASSIFICATION_REPORT_CSV = BASE_DIR / "04_output_csv" / "fix_priority_classification_report_v001.csv"
CONFUSION_MATRIX_CSV = BASE_DIR / "04_output_csv" / "fix_priority_confusion_matrix_v001.csv"
PREDICTIONS_CSV = BASE_DIR / "04_output_csv" / "fix_priority_predictions_v001.csv"
FEATURE_IMPORTANCE_CSV = BASE_DIR / "04_output_csv" / "fix_priority_feature_importance_v001.csv"

AI_READINESS_CSV = BASE_DIR / "04_output_csv" / "ai_readiness_scores_v001.csv"
AI_CONTEXT_JSON = BASE_DIR / "04_output_csv" / "ai_context_v002.json"
AI_CONTEXT_MD = BASE_DIR / "04_output_csv" / "ai_context_v002.md"
FIX_GUIDES_MD = BASE_DIR / "04_output_csv" / "fix_guides_v001.md"


# =========================================
# Helper functions
# =========================================

@st.cache_data
def load_csv(path: Path) -> pd.DataFrame:
    """Load CSV file if it exists."""
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, encoding="utf-8-sig")


def read_text_file(path: Path) -> str:
    """Read a text file if it exists."""
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def read_json_file(path: Path) -> dict:
    """Read a JSON file if it exists."""
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def relative_posix_path(path: Path) -> str:
    """Return a project-relative path using forward slashes."""
    return path.relative_to(BASE_DIR).as_posix()


def show_missing_file_warning(label: str, path: Path) -> None:
    """Show warning when an expected output file does not exist."""
    st.warning(f"{label} が見つかりません: `{relative_posix_path(path)}`")


def dataframe_download_button(
    df: pd.DataFrame,
    file_name: str,
    label: str,
    key: str,
) -> None:
    """Show CSV download button for a dataframe."""
    if df.empty:
        return

    csv_bytes = df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")

    st.download_button(
        label=label,
        data=csv_bytes,
        file_name=file_name,
        mime="text/csv",
        key=key,
    )


def normalize_element_id_series(series: pd.Series) -> pd.Series:
    """Normalize ElementId values such as 101.0 to 101."""
    return (
        pd.to_numeric(series, errors="coerce")
        .astype("Int64")
        .astype(str)
        .replace("<NA>", "")
    )


def normalize_element_id_for_df(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize ElementId column if it exists."""
    if not df.empty and "ElementId" in df.columns:
        df = df.copy()
        df["ElementId"] = normalize_element_id_series(df["ElementId"])
    return df


def count_blocking_rule_ids(ai_readiness_df: pd.DataFrame) -> pd.DataFrame:
    """Count comma-separated BlockingRuleIds."""
    if ai_readiness_df.empty or "BlockingRuleIds" not in ai_readiness_df.columns:
        return pd.DataFrame(columns=["RuleId", "Count"])

    rule_counts: dict[str, int] = {}

    for value in ai_readiness_df["BlockingRuleIds"].dropna():
        for rule_id in str(value).split(","):
            rule_id = rule_id.strip()
            if rule_id:
                rule_counts[rule_id] = rule_counts.get(rule_id, 0) + 1

    if not rule_counts:
        return pd.DataFrame(columns=["RuleId", "Count"])

    return (
        pd.DataFrame(
            [{"RuleId": rule_id, "Count": count} for rule_id, count in rule_counts.items()]
        )
        .sort_values("Count", ascending=False)
        .reset_index(drop=True)
    )


# =========================================
# Main app
# =========================================

st.set_page_config(
    page_title="BIM Data Quality & AI Readiness Assessment PoC",
    layout="wide",
)

st.title("BIM Data Quality & AI Readiness Assessment PoC")

st.write(
    "Revit/BIMデータを対象に、Pythonによる品質チェック、品質メトリクス作成、"
    "特徴量データセット作成、修正優先度分類プロトタイプ、AI Readiness Score、"
    "生成AI向け構造化コンテキスト生成、Fix Guide Markdown生成を確認する簡易画面です。"
)

st.info(
    "この画面はPoC用の簡易UIです。QualityScore、FixPriority、AIReadinessScoreは"
    "実務上の正式な品質評価・正解ラベル・AI活用準備度基準ではなく、検証用の簡易指標です。"
)


# =========================================
# Load data
# =========================================

quality_metrics_df = load_csv(QUALITY_METRICS_CSV)
rule_summary_df = load_csv(RULE_SUMMARY_CSV)
category_summary_df = load_csv(CATEGORY_SUMMARY_CSV)
element_summary_df = normalize_element_id_for_df(load_csv(ELEMENT_SUMMARY_CSV))
features_df = normalize_element_id_for_df(load_csv(FEATURES_CSV))
check_results_df = normalize_element_id_for_df(load_csv(CHECK_RESULTS_CSV))

classification_report_df = load_csv(CLASSIFICATION_REPORT_CSV)
confusion_matrix_df = load_csv(CONFUSION_MATRIX_CSV)
predictions_df = normalize_element_id_for_df(load_csv(PREDICTIONS_CSV))
feature_importance_df = load_csv(FEATURE_IMPORTANCE_CSV)

ai_readiness_df = normalize_element_id_for_df(load_csv(AI_READINESS_CSV))
ai_context_json = read_json_file(AI_CONTEXT_JSON)
ai_context_md = read_text_file(AI_CONTEXT_MD)
fix_guides_md = read_text_file(FIX_GUIDES_MD)


# =========================================
# 1. Quality metrics overview
# =========================================

st.header("1. 品質メトリクス概要")

if quality_metrics_df.empty:
    show_missing_file_warning("品質メトリクスCSV", QUALITY_METRICS_CSV)
else:
    st.dataframe(quality_metrics_df, width="stretch")


# =========================================
# 2. Rule summary
# =========================================

st.header("2. RuleId別違反件数")

if rule_summary_df.empty:
    show_missing_file_warning("RuleId別集計CSV", RULE_SUMMARY_CSV)
else:
    st.dataframe(rule_summary_df, width="stretch")

    if "RuleId" in rule_summary_df.columns and "ViolationCount" in rule_summary_df.columns:
        chart_df = rule_summary_df.set_index("RuleId")["ViolationCount"]
        st.bar_chart(chart_df)


# =========================================
# 3. Category summary
# =========================================

st.header("3. Category別違反件数")

if category_summary_df.empty:
    show_missing_file_warning("Category別集計CSV", CATEGORY_SUMMARY_CSV)
else:
    st.dataframe(category_summary_df, width="stretch")

    if "Category" in category_summary_df.columns and "ViolationCount" in category_summary_df.columns:
        chart_df = category_summary_df.set_index("Category")["ViolationCount"]
        st.bar_chart(chart_df)


# =========================================
# 4. Element quality score
# =========================================

st.header("4. ElementId別品質スコア")

if element_summary_df.empty:
    show_missing_file_warning("ElementId別集計CSV", ELEMENT_SUMMARY_CSV)
else:
    st.dataframe(element_summary_df, width="stretch")

    if "ElementId" in element_summary_df.columns and "QualityScore" in element_summary_df.columns:
        chart_df = element_summary_df.set_index("ElementId")["QualityScore"]
        st.bar_chart(chart_df)


# =========================================
# 5. Feature dataset
# =========================================

st.header("5. 特徴量データセット")

if features_df.empty:
    show_missing_file_warning("特徴量データセットCSV", FEATURES_CSV)
else:
    st.dataframe(features_df, width="stretch")

    if "FixPriority" in features_df.columns:
        st.subheader("FixPriority件数")
        fix_priority_counts = features_df["FixPriority"].value_counts().reset_index()
        fix_priority_counts.columns = ["FixPriority", "Count"]
        st.dataframe(fix_priority_counts, width="stretch")
        st.bar_chart(fix_priority_counts.set_index("FixPriority")["Count"])


# =========================================
# 6. Check results
# =========================================

st.header("6. 品質チェック結果一覧")

if check_results_df.empty:
    show_missing_file_warning("品質チェック結果CSV", CHECK_RESULTS_CSV)
else:
    filtered_df = check_results_df.copy()

    col1, col2, col3 = st.columns(3)

    with col1:
        if "RuleId" in filtered_df.columns:
            selected_rule_ids = st.multiselect(
                "RuleIdで絞り込み",
                options=sorted(filtered_df["RuleId"].dropna().unique()),
                default=sorted(filtered_df["RuleId"].dropna().unique()),
            )
            filtered_df = filtered_df[filtered_df["RuleId"].isin(selected_rule_ids)]

    with col2:
        if "Severity" in filtered_df.columns:
            selected_severities = st.multiselect(
                "Severityで絞り込み",
                options=sorted(check_results_df["Severity"].dropna().unique()),
                default=sorted(check_results_df["Severity"].dropna().unique()),
            )
            filtered_df = filtered_df[filtered_df["Severity"].isin(selected_severities)]

    with col3:
        if "Category" in filtered_df.columns:
            selected_categories = st.multiselect(
                "Categoryで絞り込み",
                options=sorted(check_results_df["Category"].dropna().unique()),
                default=sorted(check_results_df["Category"].dropna().unique()),
            )
            filtered_df = filtered_df[filtered_df["Category"].isin(selected_categories)]

    st.dataframe(filtered_df, width="stretch")
    dataframe_download_button(
        filtered_df,
        "filtered_check_results.csv",
        "絞り込み後の品質チェック結果CSVをダウンロード",
        key="download_filtered_check_results",
    )


# =========================================
# 7. AI Readiness Assessment
# =========================================

st.header("7. AI Readiness Assessment")

st.write(
    "第2段階で追加したAI活用準備度評価を表示します。"
    "BIMデータをBI、機械学習、生成AI、将来的なRAGに活用する前に、"
    "属性情報・分類コード・命名規則などの整備状況を確認するためのPoC指標です。"
)

if ai_readiness_df.empty:
    show_missing_file_warning("AI Readiness Score CSV", AI_READINESS_CSV)
else:
    required_columns = {
        "ElementId",
        "AIReadinessScore",
        "AIReadinessLevel",
        "HumanReviewRequired",
        "BlockingRuleIds",
    }

    missing_columns = required_columns - set(ai_readiness_df.columns)

    if missing_columns:
        st.error(f"AI Readiness CSVに必要な列が不足しています: {sorted(missing_columns)}")
    else:
        total_elements = ai_readiness_df["ElementId"].nunique()
        average_score = round(float(ai_readiness_df["AIReadinessScore"].mean()), 2)
        human_review_required_count = int(
            ai_readiness_df["HumanReviewRequired"]
            .astype(str)
            .str.lower()
            .eq("true")
            .sum()
        )
        low_count = int((ai_readiness_df["AIReadinessLevel"] == "Low").sum())

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Target Elements", total_elements)
        col2.metric("Average AI Readiness Score", average_score)
        col3.metric("Low Level Count", low_count)
        col4.metric("Human Review Required", human_review_required_count)

        st.subheader("AI Readiness Level別件数")
        level_counts = (
            ai_readiness_df["AIReadinessLevel"]
            .value_counts()
            .reset_index()
        )
        level_counts.columns = ["AIReadinessLevel", "Count"]
        st.dataframe(level_counts, width="stretch")
        st.bar_chart(level_counts.set_index("AIReadinessLevel")["Count"])

        st.subheader("ElementId別 AI Readiness Score")
        st.dataframe(ai_readiness_df, width="stretch")

        if "ElementId" in ai_readiness_df.columns and "AIReadinessScore" in ai_readiness_df.columns:
            score_chart_df = ai_readiness_df.set_index("ElementId")["AIReadinessScore"]
            st.bar_chart(score_chart_df)

        st.subheader("AI活用を阻害しているRuleIdランキング")
        blocking_rule_counts = count_blocking_rule_ids(ai_readiness_df)

        if blocking_rule_counts.empty:
            st.info("BlockingRuleIdsが見つかりません。")
        else:
            st.dataframe(blocking_rule_counts, width="stretch")
            st.bar_chart(blocking_rule_counts.set_index("RuleId")["Count"])

        st.subheader("Element Detail")

        element_options = sorted(
            ai_readiness_df["ElementId"].dropna().unique(),
            key=lambda x: int(x) if str(x).isdigit() else str(x),
        )

        selected_ai_element_id = st.selectbox(
            "AI Readiness詳細を確認するElementIdを選択",
            options=element_options,
            key="selected_ai_readiness_element",
        )

        selected_ai_readiness = ai_readiness_df[
            ai_readiness_df["ElementId"] == selected_ai_element_id
        ]

        if not selected_ai_readiness.empty:
            st.write("AI Readiness Score")
            st.dataframe(selected_ai_readiness, width="stretch")

        if not check_results_df.empty and "ElementId" in check_results_df.columns:
            selected_check_results = check_results_df[
                check_results_df["ElementId"] == selected_ai_element_id
            ]

            st.write("該当する品質チェック結果")

            if selected_check_results.empty:
                st.info("選択したElementIdの品質チェック結果はありません。")
            else:
                st.dataframe(selected_check_results, width="stretch")

        dataframe_download_button(
            ai_readiness_df,
            "ai_readiness_scores_v001.csv",
            "AI Readiness Score CSVをダウンロード",
            key="download_ai_readiness_scores",
        )


# =========================================
# 8. FixPriority model prototype
# =========================================

st.header("8. 修正優先度分類プロトタイプ結果")

st.write(
    "scikit-learnを用いた修正優先度分類プロトタイプの結果を表示します。"
    "現時点のFixPriorityは仮ラベルであり、初期データではHighのみのため、"
    "本格的な分類精度評価ではなく、学習・予測・評価CSV出力の流れを確認する位置づけです。"
)

if classification_report_df.empty:
    show_missing_file_warning("classification_report CSV", CLASSIFICATION_REPORT_CSV)
else:
    st.subheader("Classification Report")
    st.dataframe(classification_report_df, width="stretch")

if confusion_matrix_df.empty:
    show_missing_file_warning("confusion_matrix CSV", CONFUSION_MATRIX_CSV)
else:
    st.subheader("Confusion Matrix")
    st.dataframe(confusion_matrix_df, width="stretch")

if predictions_df.empty:
    show_missing_file_warning("predictions CSV", PREDICTIONS_CSV)
else:
    st.subheader("Prediction Results")
    st.dataframe(predictions_df, width="stretch")
    dataframe_download_button(
        predictions_df,
        "fix_priority_predictions_v001.csv",
        "修正優先度予測結果CSVをダウンロード",
        key="download_fix_priority_predictions_from_section_8",
    )

if feature_importance_df.empty:
    st.info(
        "Feature Importanceは未出力です。現在のデータではFixPriorityが1クラスのみのため、"
        "DummyClassifierでMLフロー確認を行っています。"
    )
else:
    st.subheader("Feature Importance")
    st.dataframe(feature_importance_df, width="stretch")
    if "Feature" in feature_importance_df.columns and "Importance" in feature_importance_df.columns:
        st.bar_chart(feature_importance_df.set_index("Feature")["Importance"])


# =========================================
# 9. AI context generation
# =========================================

st.header("9. 生成AI向け構造化コンテキスト v002")

st.write(
    "BIM品質チェック結果、特徴量データセット、AI Readiness Scoreをもとに、"
    "生成AIへ渡すための参照情報をJSON / Markdown形式で整理しています。"
    "現時点では生成AI APIは呼び出しておらず、AIに渡す前段階の構造化コンテキスト生成として位置づけています。"
)

if not ai_context_json:
    show_missing_file_warning("AI Context JSON v002", AI_CONTEXT_JSON)
else:
    summary = ai_context_json.get("summary", {})
    project = ai_context_json.get("project", {})

    st.subheader("AI Context Summary")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Violations", summary.get("total_violations", 0))
    col2.metric("Total Elements", summary.get("total_elements", 0))
    col3.metric("Avg AI Readiness", summary.get("average_ai_readiness_score", 0))
    col4.metric("Human Review Required", summary.get("human_review_required_count", 0))

    st.write(f"Project: {project.get('name', '')}")
    st.write(f"Previous Name: {project.get('previous_name', '')}")
    st.write(f"Purpose: {project.get('purpose', '')}")

    if "ai_readiness_level_summary" in summary:
        st.subheader("AI Readiness Level Summary")
        st.dataframe(pd.DataFrame(summary["ai_readiness_level_summary"]), width="stretch")

    st.subheader("Element Context Preview")

    elements = ai_context_json.get("elements", [])

    if elements:
        element_options = [
            item.get("element", {}).get("element_id", "")
            for item in elements
        ]

        selected_context_element_id = st.selectbox(
            "AI Contextを確認するElementIdを選択",
            options=element_options,
            key="selected_ai_context_element",
        )

        selected_context = next(
            (
                item for item in elements
                if item.get("element", {}).get("element_id", "") == selected_context_element_id
            ),
            None,
        )

        if selected_context:
            st.caption(
                "選択したElementIdについて、要素情報、品質スコア、AI Readiness、検出された違反、AI向け指示条件をJSON形式で表示しています。"
            )
            st.json(selected_context)

if ai_context_md:
    st.subheader("Markdown Context Preview")
    with st.expander("ai_context_v002.md を表示"):
        st.markdown(ai_context_md)

if AI_CONTEXT_JSON.exists():
    json_bytes = AI_CONTEXT_JSON.read_bytes()
    st.download_button(
        label="AI Context JSON v002をダウンロード",
        data=json_bytes,
        file_name="ai_context_v002.json",
        mime="application/json",
        key="download_ai_context_json_v002",
    )

if AI_CONTEXT_MD.exists():
    md_bytes = AI_CONTEXT_MD.read_bytes()
    st.download_button(
        label="AI Context Markdown v002をダウンロード",
        data=md_bytes,
        file_name="ai_context_v002.md",
        mime="text/markdown",
        key="download_ai_context_md_v002",
    )


# =========================================
# 10. Fix Guide Preview
# =========================================

st.header("10. Fix Guide Markdown Preview")

st.write(
    "品質チェック結果、Rule Master v003、AI Readiness Scoreをもとに生成した"
    "ルールベースの修正ガイドMarkdownを表示します。"
    "生成AI APIは使用していません。"
)

if not fix_guides_md:
    show_missing_file_warning("Fix Guide Markdown", FIX_GUIDES_MD)
else:
    with st.expander("fix_guides_v001.md を表示", expanded=False):
        st.markdown(fix_guides_md)

if FIX_GUIDES_MD.exists():
    st.download_button(
        label="Fix Guide Markdownをダウンロード",
        data=FIX_GUIDES_MD.read_bytes(),
        file_name="fix_guides_v001.md",
        mime="text/markdown",
        key="download_fix_guides_v001",
    )


# =========================================
# 11. Download section
# =========================================

st.header("11. 出力ファイルダウンロード")

st.write("主要な出力ファイルをダウンロードできます。")

download_targets = [
    ("品質チェック結果CSV", CHECK_RESULTS_CSV, "check_results_revit_v002.csv", "text/csv"),
    ("品質メトリクスCSV", QUALITY_METRICS_CSV, "quality_metrics_v001.csv", "text/csv"),
    ("RuleId別集計CSV", RULE_SUMMARY_CSV, "rule_summary_v001.csv", "text/csv"),
    ("ElementId別集計CSV", ELEMENT_SUMMARY_CSV, "element_summary_v001.csv", "text/csv"),
    ("特徴量データセットCSV", FEATURES_CSV, "bim_features_v001.csv", "text/csv"),
    ("修正優先度予測結果CSV", PREDICTIONS_CSV, "fix_priority_predictions_v001.csv", "text/csv"),
    ("AI Readiness Score CSV", AI_READINESS_CSV, "ai_readiness_scores_v001.csv", "text/csv"),
    ("AI Context JSON v002", AI_CONTEXT_JSON, "ai_context_v002.json", "application/json"),
    ("AI Context Markdown v002", AI_CONTEXT_MD, "ai_context_v002.md", "text/markdown"),
    ("Fix Guide Markdown", FIX_GUIDES_MD, "fix_guides_v001.md", "text/markdown"),
]

for index, (label, path, file_name, mime_type) in enumerate(download_targets):
    if path.exists():
        st.download_button(
            label=f"{label}をダウンロード",
            data=path.read_bytes(),
            file_name=file_name,
            mime=mime_type,
            key=f"download_output_file_{index}_{file_name}",
        )


# =========================================
# 12. Limitations
# =========================================

st.header("12. 現時点の注意点")

st.markdown(
    """
- この画面はPoC用の簡易UIです。
- `QualityScore` はPoC用の簡易指標であり、正式な実務品質評価基準ではありません。
- `AIReadinessScore` はPoC用の簡易指標であり、正式なAI活用準備度基準ではありません。
- `FixPriority` は実務の正解ラベルではなく、仮ラベルです。
- 現在のデータでは `FixPriority` が `High` のみであり、本格的な分類精度評価はできません。
- 生成AI APIは呼び出していません。
- 生成AI向け構造化コンテキストは、AIに渡す前段階の参照情報整理です。
- Fix Guide Markdownは生成AI APIではなく、RuleIdベースのテンプレート方式で生成しています。
- Revit API / pyRevit連携は未実装です。
- BIMモデルの自動修正は対象外です。
- 最終的な設計判断・モデル修正判断は人間が行う前提です。
"""
)
