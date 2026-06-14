from pathlib import Path

import pandas as pd


ROOM_DATA_PATH = Path("03_input_csv/cleaned_room_data_v001.csv")
CHECK_RESULTS_PATH = Path("04_output_csv/check_results_room_v001.csv")
OUTPUT_PATH = Path("04_output_csv/room_ai_readiness_scores_v001.csv")


def classify_ai_readiness_level(score: float) -> str:
    if score >= 80:
        return "High"
    if score >= 60:
        return "Medium"
    return "Low"


def validate_columns(df: pd.DataFrame, required_columns: list[str], file_label: str) -> None:
    missing_columns = [column for column in required_columns if column not in df.columns]

    if missing_columns:
        raise ValueError(f"{file_label} is missing required columns: {missing_columns}")


def calculate_room_ai_readiness_score(
    room_data_path: Path = ROOM_DATA_PATH,
    check_results_path: Path = CHECK_RESULTS_PATH,
    output_path: Path = OUTPUT_PATH,
) -> pd.DataFrame:
    room_data = pd.read_csv(room_data_path, dtype=str, encoding="utf-8-sig").fillna("")
    check_results = pd.read_csv(check_results_path, dtype=str, encoding="utf-8-sig").fillna("")

    validate_columns(
        room_data,
        ["ElementId", "Category", "Level", "RoomName", "RoomNumber", "Area"],
        "cleaned_room_data_v001.csv",
    )

    validate_columns(
        check_results,
        ["ElementId", "RuleId", "AIReadinessImpact", "AIReadinessPenalty"],
        "check_results_room_v001.csv",
    )

    room_data = room_data[room_data["Category"] == "Room"].copy()

    check_results["AIReadinessPenalty"] = pd.to_numeric(
        check_results["AIReadinessPenalty"],
        errors="coerce",
    ).fillna(0)

    grouped = (
        check_results.groupby("ElementId", dropna=False)
        .agg(
            RuleViolationCount=("RuleId", "count"),
            AIReadinessPenaltyTotal=("AIReadinessPenalty", "sum"),
            BlockingRuleIds=("RuleId", lambda x: ", ".join(sorted(set(x.dropna().astype(str))))),
            HighImpactRuleCount=("AIReadinessImpact", lambda x: (x == "High").sum()),
            MediumImpactRuleCount=("AIReadinessImpact", lambda x: (x == "Medium").sum()),
        )
        .reset_index()
    )

    output = room_data[
        ["ElementId", "Category", "Level", "RoomName", "RoomNumber", "Area"]
    ].merge(
        grouped,
        on="ElementId",
        how="left",
    )

    output["RuleViolationCount"] = output["RuleViolationCount"].fillna(0).astype(int)
    output["AIReadinessPenaltyTotal"] = output["AIReadinessPenaltyTotal"].fillna(0).astype(int)
    output["BlockingRuleIds"] = output["BlockingRuleIds"].fillna("")
    output["HighImpactRuleCount"] = output["HighImpactRuleCount"].fillna(0).astype(int)
    output["MediumImpactRuleCount"] = output["MediumImpactRuleCount"].fillna(0).astype(int)

    output["AIReadinessScore"] = 100 - output["AIReadinessPenaltyTotal"]
    output["AIReadinessScore"] = output["AIReadinessScore"].clip(lower=0)

    output["AIReadinessLevel"] = output["AIReadinessScore"].apply(
        classify_ai_readiness_level
    )

    output["HumanReviewRequired"] = (
        (output["AIReadinessLevel"] == "Low")
        | (output["HighImpactRuleCount"] >= 1)
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(output_path, index=False, encoding="utf-8-sig")

    return output


if __name__ == "__main__":
    result = calculate_room_ai_readiness_score()
    print(f"Output: {OUTPUT_PATH}")
    print(f"Rows: {len(result)}")
    print(result.head(20).to_string(index=False))