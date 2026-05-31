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

AI_CONTEXT_JSON = BASE_DIR / "04_output_csv" / "ai_context_v001.json"
AI_CONTEXT_MD = BASE_DIR / "04_output_csv" / "ai_context_v001.md"


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


def show_missing_file_warning(label: str, path: Path) -> None:
    """Show warning when an expected output file does not exist."""
    st.warning(f"{label} が見つかりません: `{path.relative_to(BASE_DIR)}`")


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


# =========================================
# Main app
# =========================================

st.set_page_config(
    page_title="BIM Data Quality Engineering & AI Analysis PoC",
    layout="wide",
)

st.title("BIM Data Quality Engineering & AI Analysis PoC")

st.write(
    "Revit/BIMデータを対象に、Pythonによる品質チェック、品質メトリクス作成、"
    "特徴量データセット作成、修正優先度分類プロトタイプ、生成AI向け構造化コンテキスト生成を確認する簡易画面です。"
)

st.info(
    "この画面はPoC用の簡易UIです。QualityScoreやFixPriorityは実務上の正式な品質評価・正解ラベルではなく、"
    "検証用の簡易指標・仮ラベルです。"
)


# =========================================
# Load data
# =========================================

quality_metrics_df = load_csv(QUALITY_METRICS_CSV)
rule_summary_df = load_csv(RULE_SUMMARY_CSV)
category_summary_df = load_csv(CATEGORY_SUMMARY_CSV)
element_summary_df = load_csv(ELEMENT_SUMMARY_CSV)
features_df = load_csv(FEATURES_CSV)
check_results_df = load_csv(CHECK_RESULTS_CSV)

classification_report_df = load_csv(CLASSIFICATION_REPORT_CSV)
confusion_matrix_df = load_csv(CONFUSION_MATRIX_CSV)
predictions_df = load_csv(PREDICTIONS_CSV)
feature_importance_df = load_csv(FEATURE_IMPORTANCE_CSV)

ai_context_json = read_json_file(AI_CONTEXT_JSON)
ai_context_md = read_text_file(AI_CONTEXT_MD)


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
# 7. FixPriority model prototype
# =========================================

st.header("7. 修正優先度分類プロトタイプ結果")

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
        key="download_fix_priority_predictions_from_section_7",
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
# 8. AI context generation
# =========================================

st.header("8. 生成AI向け構造化コンテキスト")

st.write(
    "BIM品質チェック結果と特徴量データセットをもとに、生成AIへ渡すための参照情報をJSON / Markdown形式で整理しています。"
    "現時点では生成AI APIは呼び出しておらず、AIに渡す前段階の構造化コンテキスト生成として位置づけています。"
)

if not ai_context_json:
    show_missing_file_warning("AI Context JSON", AI_CONTEXT_JSON)
else:
    summary = ai_context_json.get("summary", {})
    project = ai_context_json.get("project", {})

    st.subheader("AI Context Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Violations", summary.get("total_violations", 0))
    col2.metric("Total Elements", summary.get("total_elements", 0))
    col3.metric("Element Contexts", len(ai_context_json.get("elements", [])))

    st.write(f"Project: {project.get('name', '')}")
    st.write(f"Purpose: {project.get('purpose', '')}")

    st.subheader("Sample Element Context")

    elements = ai_context_json.get("elements", [])

    if elements:
        element_options = [
            item.get("element", {}).get("element_id", "")
            for item in elements
        ]

        selected_element_id = st.selectbox(
            "ElementIdを選択",
            options=element_options,
        )

        selected_context = next(
            (
                item for item in elements
                if item.get("element", {}).get("element_id", "") == selected_element_id
            ),
            None,
        )

        if selected_context:
            st.caption(
                "選択したElementIdについて、要素情報、品質スコア、検出された違反、AI向け指示条件をJSON形式で表示しています。"
            )
            st.json(selected_context)


if ai_context_md:
    st.subheader("Markdown Context Preview")
    with st.expander("ai_context_v001.md を表示"):
        st.markdown(ai_context_md)

if AI_CONTEXT_JSON.exists():
    json_bytes = AI_CONTEXT_JSON.read_bytes()
    st.download_button(
        label="AI Context JSONをダウンロード",
        data=json_bytes,
        file_name="ai_context_v001.json",
        mime="application/json",
        key="download_ai_context_json",
    )

if AI_CONTEXT_MD.exists():
    md_bytes = AI_CONTEXT_MD.read_bytes()
    st.download_button(
        label="AI Context Markdownをダウンロード",
        data=md_bytes,
        file_name="ai_context_v001.md",
        mime="text/markdown",
        key="download_ai_context_md",
    )


# =========================================
# 9. Download section
# =========================================

st.header("9. 出力ファイルダウンロード")

st.write("主要な出力CSVをダウンロードできます。")

download_targets = [
    ("品質チェック結果CSV", CHECK_RESULTS_CSV, "check_results_revit_v002.csv", "text/csv"),
    ("品質メトリクスCSV", QUALITY_METRICS_CSV, "quality_metrics_v001.csv", "text/csv"),
    ("RuleId別集計CSV", RULE_SUMMARY_CSV, "rule_summary_v001.csv", "text/csv"),
    ("ElementId別集計CSV", ELEMENT_SUMMARY_CSV, "element_summary_v001.csv", "text/csv"),
    ("特徴量データセットCSV", FEATURES_CSV, "bim_features_v001.csv", "text/csv"),
    ("修正優先度予測結果CSV", PREDICTIONS_CSV, "fix_priority_predictions_v001.csv", "text/csv"),
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
# 10. Limitations
# =========================================

st.header("10. 現時点の注意点")

st.markdown(
    """
- この画面はPoC用の簡易UIです。
- `QualityScore` はPoC用の簡易指標であり、正式な実務品質評価基準ではありません。
- `FixPriority` は実務の正解ラベルではなく、仮ラベルです。
- 現在のデータでは `FixPriority` が `High` のみであり、本格的な分類精度評価はできません。
- 生成AI APIは呼び出していません。
- 生成AI向け構造化コンテキストは、AIに渡す前段階の参照情報整理です。
- Revit API / pyRevit連携は未実装です。
- BIMモデルの自動修正は対象外です。
- 最終的な設計判断・モデル修正判断は人間が行う前提です。
"""
)