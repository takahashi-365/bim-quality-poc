# このファイルの目的：
# BIM特徴量データセットを読み込み、FixPriorityを分類する
# scikit-learnプロトタイプを実行する。
#
# 注意：
# 本スクリプトは実務用の完成モデルではなく、PoC用の分類フロー確認です。
# FixPriorityは実務の正解ラベルではなく、QualityScoreやHigh違反件数をもとにした仮ラベルです。

from pathlib import Path

import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split


# =========================================
# Path settings
# =========================================

BASE_DIR = Path(__file__).resolve().parents[1]

FEATURES_CSV = BASE_DIR / "04_output_csv" / "bim_features_v001.csv"
OUTPUT_DIR = BASE_DIR / "04_output_csv"

CLASSIFICATION_REPORT_CSV = OUTPUT_DIR / "fix_priority_classification_report_v001.csv"
CONFUSION_MATRIX_CSV = OUTPUT_DIR / "fix_priority_confusion_matrix_v001.csv"
FEATURE_IMPORTANCE_CSV = OUTPUT_DIR / "fix_priority_feature_importance_v001.csv"
PREDICTIONS_CSV = OUTPUT_DIR / "fix_priority_predictions_v001.csv"


# =========================================
# Helper functions
# =========================================

def validate_input_file() -> None:
    """Validate that the input feature CSV exists."""
    if not FEATURES_CSV.exists():
        raise FileNotFoundError(f"Features CSV not found: {FEATURES_CSV}")


def load_features() -> pd.DataFrame:
    """Load BIM feature dataset."""
    return pd.read_csv(FEATURES_CSV, encoding="utf-8-sig")


def prepare_dataset(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Prepare X and y for model training."""

    target_column = "FixPriority"

    if target_column not in df.columns:
        raise ValueError(f"Target column not found: {target_column}")

    feature_columns = [
        "RuleViolationCount",
        "MissingFieldCount",
        "HighViolationCount",
        "MediumViolationCount",
        "LowViolationCount",
        "HasClassificationCode",
        "FamilyNameValid",
        "SeverityScore",
        "QualityScore",
    ]

    missing_columns = [col for col in feature_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Feature columns not found: {missing_columns}")

    X = df[feature_columns].copy()
    y = df[target_column].copy()

    # Convert boolean-like columns to numeric if needed.
    for col in X.columns:
        X[col] = pd.to_numeric(X[col], errors="coerce").fillna(0)

    return X, y


def save_classification_report(y_true: pd.Series, y_pred: list[str]) -> None:
    """Save classification report as CSV."""
    report_dict = classification_report(
        y_true,
        y_pred,
        zero_division=0,
        output_dict=True,
    )

    report_df = pd.DataFrame(report_dict).transpose()
    report_df.to_csv(CLASSIFICATION_REPORT_CSV, encoding="utf-8-sig")


def save_confusion_matrix(y_true: pd.Series, y_pred: list[str]) -> None:
    """Save confusion matrix as CSV."""
    labels = sorted(y_true.unique())

    matrix = confusion_matrix(y_true, y_pred, labels=labels)

    matrix_df = pd.DataFrame(
        matrix,
        index=[f"Actual_{label}" for label in labels],
        columns=[f"Predicted_{label}" for label in labels],
    )

    matrix_df.to_csv(CONFUSION_MATRIX_CSV, encoding="utf-8-sig")


def save_feature_importance(model: RandomForestClassifier, feature_names: list[str]) -> None:
    """Save feature importance as CSV."""
    importance_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": model.feature_importances_,
    }).sort_values("Importance", ascending=False)

    importance_df.to_csv(FEATURE_IMPORTANCE_CSV, index=False, encoding="utf-8-sig")


def save_predictions(
    original_df: pd.DataFrame,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    y_pred: list[str],
) -> None:
    """Save prediction results as CSV."""
    predictions_df = original_df.loc[X_test.index].copy()
    predictions_df["ActualFixPriority"] = y_test.values
    predictions_df["PredictedFixPriority"] = y_pred

    predictions_df.to_csv(PREDICTIONS_CSV, index=False, encoding="utf-8-sig")


# =========================================
# Main process
# =========================================

def main() -> None:
    print("Fix priority model training started.")

    validate_input_file()

    print(f"Input file: {FEATURES_CSV}")

    df = load_features()
    print(f"Input data shape: {df.shape}")

    if df.empty:
        raise ValueError("Features CSV is empty.")

    if "FixPriority" not in df.columns:
        raise ValueError("FixPriority column not found.")

    print("FixPriority counts:")
    print(df["FixPriority"].value_counts())

    X, y = prepare_dataset(df)

    unique_labels = y.nunique()

    # 現在のデータでは FixPriority が High だけの可能性がある。
    # その場合、通常の分類モデルは評価できないため、DummyClassifierで動作確認に留める。
    if unique_labels < 2:
        print("")
        print("WARNING:")
        print("Only one FixPriority class exists in the dataset.")
        print("This is not enough for real classification evaluation.")
        print("A DummyClassifier will be used only to verify the ML workflow.")

        model = DummyClassifier(strategy="most_frequent")
        model.fit(X, y)
        y_pred = model.predict(X)

        save_classification_report(y, y_pred)
        save_confusion_matrix(y, y_pred)

        predictions_df = df.copy()
        predictions_df["ActualFixPriority"] = y.values
        predictions_df["PredictedFixPriority"] = y_pred
        predictions_df.to_csv(PREDICTIONS_CSV, index=False, encoding="utf-8-sig")

        print(f"Classification report output: {CLASSIFICATION_REPORT_CSV}")
        print(f"Confusion matrix output: {CONFUSION_MATRIX_CSV}")
        print(f"Predictions output: {PREDICTIONS_CSV}")
        print("Feature importance output was skipped because DummyClassifier was used.")
        print("Fix priority model training completed.")
        return

    stratify = y if y.value_counts().min() >= 2 else None

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.3,
        random_state=42,
        stratify=stratify,
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced",
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    save_classification_report(y_test, y_pred)
    save_confusion_matrix(y_test, y_pred)
    save_feature_importance(model, list(X.columns))
    save_predictions(df, X_test, y_test, y_pred)

    print(f"Train shape: {X_train.shape}")
    print(f"Test shape: {X_test.shape}")
    print(f"Classification report output: {CLASSIFICATION_REPORT_CSV}")
    print(f"Confusion matrix output: {CONFUSION_MATRIX_CSV}")
    print(f"Feature importance output: {FEATURE_IMPORTANCE_CSV}")
    print(f"Predictions output: {PREDICTIONS_CSV}")
    print("Fix priority model training completed.")


if __name__ == "__main__":
    main()