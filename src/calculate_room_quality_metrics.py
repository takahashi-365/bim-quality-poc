from pathlib import Path

import pandas as pd


ROOM_DATA_PATH = Path("03_input_csv/cleaned_room_data_v001.csv")
CHECK_RESULTS_PATH = Path("04_output_csv/check_results_room_v001.csv")

OUTPUT_QUALITY_METRICS = Path("04_output_csv/room_quality_metrics_v001.csv")
OUTPUT_RULE_SUMMARY = Path("04_output_csv/room_rule_summary_v001.csv")
OUTPUT_CATEGORY_SUMMARY = Path("04_output_csv/room_category_summary_v001.csv")
OUTPUT_ELEMENT_SUMMARY = Path("04_output_csv/room_element_summary_v001.csv")


SEVERITY_SCORE_MAP = {
    "High": 10,
    "Medium": 5,
    "Low": 1,
}


def calculate_penalty(severity: object) -> int:
    return SEVERITY_SCORE_MAP.get(str(severity).strip(), 0)


def validate_columns(df: pd.DataFrame, required_columns: list[str], file_label: str) -> None:
    missing_columns = [column for column in required_columns if column not in df.columns]

    if missing_columns:
        raise ValueError(f"{file_label} is missing required columns: {missing_columns}")


def calculate_room_quality_metrics(
    room_data_path: Path = ROOM_DATA_PATH,
    check_results_path: Path = CHECK_RESULTS_PATH,
) -> dict[str, pd.DataFrame]:
    if not room_data_path.exists():
        raise FileNotFoundError(f"Room data CSV not found: {room_data_path}")

    if not check_results_path.exists():
        raise FileNotFoundError(f"Check results CSV not found: {check_results_path}")

    room_data = pd.read_csv(room_data_path, dtype=str, encoding="utf-8-sig").fillna("")
    check_results = pd.read_csv(check_results_path, dtype=str, encoding="utf-8-sig").fillna("")

    validate_columns(
        room_data,
        ["ElementId", "Category"],
        "cleaned_room_data_v001.csv",
    )

    validate_columns(
        check_results,
        ["ElementId", "Category", "RuleId", "RuleName", "Severity"],
        "check_results_room_v001.csv",
    )

    room_data = room_data[room_data["Category"] == "Room"].copy()
    check_results = check_results[check_results["Category"] == "Room"].copy()

    total_element_count = room_data["ElementId"].nunique()

    check_results["Penalty"] = check_results["Severity"].apply(calculate_penalty)

    rule_summary = (
        check_results.groupby(["RuleId", "RuleName", "Severity"], dropna=False)
        .size()
        .reset_index(name="ViolationCount")
        .sort_values(["RuleId"])
    )

    category_summary = (
        check_results.groupby(["Category"], dropna=False)
        .size()
        .reset_index(name="ViolationCount")
        .sort_values(["ViolationCount"], ascending=False)
    )

    element_summary = (
        check_results.groupby(["ElementId", "Category"], dropna=False)
        .agg(
            ViolationCount=("RuleId", "count"),
            PenaltyTotal=("Penalty", "sum"),
            HighViolationCount=("Severity", lambda x: (x == "High").sum()),
            MediumViolationCount=("Severity", lambda x: (x == "Medium").sum()),
            LowViolationCount=("Severity", lambda x: (x == "Low").sum()),
            RuleIds=("RuleId", lambda x: ", ".join(sorted(set(x.dropna().astype(str))))),
        )
        .reset_index()
    )

    element_summary["QualityScore"] = 100 - element_summary["PenaltyTotal"]
    element_summary["QualityScore"] = element_summary["QualityScore"].clip(lower=0)

    violated_element_count = element_summary["ElementId"].nunique()
    clean_element_count = total_element_count - violated_element_count

    quality_scores_for_all_rooms = room_data[["ElementId", "Category"]].drop_duplicates().merge(
        element_summary[["ElementId", "ViolationCount", "PenaltyTotal", "QualityScore"]],
        on="ElementId",
        how="left",
    )

    quality_scores_for_all_rooms["ViolationCount"] = quality_scores_for_all_rooms[
        "ViolationCount"
    ].fillna(0).astype(int)

    quality_scores_for_all_rooms["PenaltyTotal"] = quality_scores_for_all_rooms[
        "PenaltyTotal"
    ].fillna(0).astype(int)

    quality_scores_for_all_rooms["QualityScore"] = quality_scores_for_all_rooms[
        "QualityScore"
    ].fillna(100).astype(int)

    quality_metrics = pd.DataFrame(
        [
            {
                "Category": "Room",
                "TotalElementCount": total_element_count,
                "CheckedElementCount": total_element_count,
                "ViolationCount": len(check_results),
                "ViolatedElementCount": violated_element_count,
                "CleanElementCount": clean_element_count,
                "AverageQualityScore": round(
                    quality_scores_for_all_rooms["QualityScore"].mean(),
                    2,
                ),
                "MinQualityScore": quality_scores_for_all_rooms["QualityScore"].min(),
                "MaxQualityScore": quality_scores_for_all_rooms["QualityScore"].max(),
            }
        ]
    )

    return {
        "quality_metrics": quality_metrics,
        "rule_summary": rule_summary,
        "category_summary": category_summary,
        "element_summary": element_summary,
    }


def main() -> None:
    outputs = calculate_room_quality_metrics()

    OUTPUT_QUALITY_METRICS.parent.mkdir(parents=True, exist_ok=True)

    outputs["quality_metrics"].to_csv(
        OUTPUT_QUALITY_METRICS,
        index=False,
        encoding="utf-8-sig",
    )

    outputs["rule_summary"].to_csv(
        OUTPUT_RULE_SUMMARY,
        index=False,
        encoding="utf-8-sig",
    )

    outputs["category_summary"].to_csv(
        OUTPUT_CATEGORY_SUMMARY,
        index=False,
        encoding="utf-8-sig",
    )

    outputs["element_summary"].to_csv(
        OUTPUT_ELEMENT_SUMMARY,
        index=False,
        encoding="utf-8-sig",
    )

    print(f"Output: {OUTPUT_QUALITY_METRICS}")
    print(f"Output: {OUTPUT_RULE_SUMMARY}")
    print(f"Output: {OUTPUT_CATEGORY_SUMMARY}")
    print(f"Output: {OUTPUT_ELEMENT_SUMMARY}")
    print(outputs["quality_metrics"].to_string(index=False))


if __name__ == "__main__":
    main()