"""
Use the trained career readiness model to make recommendations for new student data.

Run this script after train.py has saved a model in the models folder.

Example:
    python src/predict.py
    python src/predict.py --input data/new_students.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd

MODEL_FILENAME = "placement_model.joblib"


def get_project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).resolve().parent.parent


def get_model_path() -> Path:
    """Return the path to the saved model file."""
    return get_project_root() / "models" / MODEL_FILENAME


def load_model_bundle() -> dict:
    """Load the saved model and preprocessing details."""
    model_path = get_model_path()
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model not found at {model_path}. Run train.py first."
        )
    return joblib.load(model_path)


def prepare_input_features(df: pd.DataFrame, model_bundle: dict) -> pd.DataFrame:
    """
    Clean and encode new data so it matches the training format.

    The saved model expects the same feature columns that were used during training.
    """
    categorical_columns = model_bundle["categorical_columns"]
    feature_columns = model_bundle["feature_columns"]
    target_column = model_bundle["target_column"]

    # Keep only input columns (ignore target and salary if they are present)
    columns_to_drop = [col for col in [target_column, "Salary_LPA"] if col in df.columns]
    features = df.drop(columns=columns_to_drop)

    # Encode categorical columns the same way as in train.py
    encoded = pd.get_dummies(
        features,
        columns=categorical_columns,
        drop_first=True,
    )

    # Add any missing columns and keep columns in the same order as training
    encoded = encoded.reindex(columns=feature_columns, fill_value=0)
    return encoded


def predict(df: pd.DataFrame, model_bundle: dict) -> pd.Series:
    """Return career readiness predictions for the input dataframe."""
    X = prepare_input_features(df, model_bundle)
    model = model_bundle["model"]
    scaler = model_bundle["scaler"]

    # Logistic Regression uses a scaler; Random Forest does not
    if scaler is not None:
        X = scaler.transform(X)

    return pd.Series(model.predict(X), name="Predicted_Career_Readiness_Status")


def build_sample_input() -> pd.DataFrame:
    """
    Create one example student record for a quick demo prediction.

    You can replace this with your own student data.
    """
    return pd.DataFrame(
        [
            {
                "Age": 21,
                "Gender": "Male",
                "College_Tier": "Tier 2",
                "Specialization": "Computer Science",
                "CGPA": 8.2,
                "DSA_Problems_Solved": 350,
                "Internships": 2,
                "Certifications": 4,
                "Projects_Count": 6,
                "Communication_Skills": 80,
                "Aptitude_Test_Score": 75,
                "LeetCode_Rating": 1600,
                "GitHub_Contributions": 50,
                "Hackathons_Participated": 3,
                "AI_ML_Skill_Level": 7,
                "System_Design_Knowledge": 6,
                "Resume_Score": 85,
                "Mock_Interview_Score": 78,
            }
        ]
    )


def parse_args() -> argparse.Namespace:
    """Read command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Predict student career readiness status using the trained model."
    )
    parser.add_argument(
        "--input",
        type=str,
        default=None,
        help="Optional path to a CSV file containing student records.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    model_bundle = load_model_bundle()

    print("=" * 60)
    print("CAREER READINESS & RECOMMENDATION SYSTEM")
    print("=" * 60)
    print(f"Loaded model: {model_bundle['model_name']}")

    # Load data from CSV if provided, otherwise use a sample student
    if args.input:
        input_path = Path(args.input)
        df = pd.read_csv(input_path)
        print(f"Input file: {input_path}")
    else:
        df = build_sample_input()
        print("Using built-in sample student data.")

    predictions = predict(df, model_bundle)
    results = df.copy()
    results["Predicted_Career_Readiness_Status"] = predictions.values

    print("\nPredictions:")
    print(results)


if __name__ == "__main__":
    main()
