"""
Feature engineering module for the student placement dataset.

Creates four composite scores and saves the enriched dataset to
data/engineered_data.csv.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA_FILENAME = "student_placement_career_success_dataset_2026.csv"
OUTPUT_FILENAME = "engineered_data.csv"

# Weights for each composite score (must sum to 1.0 within each group)
EMPLOYABILITY_WEIGHTS = {
    "CGPA": 0.20,
    "DSA_Problems_Solved": 0.15,
    "Internships": 0.15,
    "Certifications": 0.10,
    "Projects_Count": 0.10,
    "Resume_Score": 0.15,
    "Mock_Interview_Score": 0.15,
}

TECHNICAL_STRENGTH_WEIGHTS = {
    "DSA_Problems_Solved": 0.25,
    "LeetCode_Rating": 0.25,
    "GitHub_Contributions": 0.15,
    "AI_ML_Skill_Level": 0.175,
    "System_Design_Knowledge": 0.175,
}

PROFESSIONAL_READINESS_WEIGHTS = {
    "Communication_Skills": 0.25,
    "Resume_Score": 0.25,
    "Mock_Interview_Score": 0.30,
    "Internships": 0.20,
}

ACTIVITY_WEIGHTS = {
    "Projects_Count": 0.40,
    "Hackathons_Participated": 0.30,
    "GitHub_Contributions": 0.30,
}


def get_project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).resolve().parent.parent


def get_data_path() -> Path:
    """Return the path to the source dataset CSV file."""
    return get_project_root() / "data" / DATA_FILENAME


def get_output_path() -> Path:
    """Return the path where the engineered dataset will be saved."""
    return get_project_root() / "data" / OUTPUT_FILENAME


def load_dataset(data_path: Path | None = None) -> pd.DataFrame:
    """Load the raw student placement dataset."""
    return pd.read_csv(data_path or get_data_path())


def min_max_scale(series: pd.Series) -> pd.Series:
    """
    Scale a numeric column to a 0-100 range.

    This puts every feature on the same scale before combining them
    into a weighted score.
    """
    min_value = series.min()
    max_value = series.max()

    if max_value == min_value:
        return pd.Series(50.0, index=series.index)

    return (series - min_value) / (max_value - min_value) * 100


def compute_weighted_score(
    df: pd.DataFrame,
    weights: dict[str, float],
) -> pd.Series:
    """
    Build a weighted score from multiple columns.

    Each column is scaled to 0-100 first, then multiplied by its weight.
    """
    score = pd.Series(0.0, index=df.index)

    for column, weight in weights.items():
        scaled = min_max_scale(df[column])
        score += scaled * weight

    return score.round(2)


def add_employability_score(df: pd.DataFrame) -> pd.DataFrame:
    """Add Employability_Score based on academic and career-prep signals."""
    df = df.copy()
    df["Employability_Score"] = compute_weighted_score(df, EMPLOYABILITY_WEIGHTS)
    return df


def add_technical_strength_score(df: pd.DataFrame) -> pd.DataFrame:
    """Add Technical_Strength_Score based on coding and technical skills."""
    df = df.copy()
    df["Technical_Strength_Score"] = compute_weighted_score(
        df,
        TECHNICAL_STRENGTH_WEIGHTS,
    )
    return df


def add_professional_readiness_score(df: pd.DataFrame) -> pd.DataFrame:
    """Add Professional_Readiness_Score based on soft skills and experience."""
    df = df.copy()
    df["Professional_Readiness_Score"] = compute_weighted_score(
        df,
        PROFESSIONAL_READINESS_WEIGHTS,
    )
    return df


def add_activity_score(df: pd.DataFrame) -> pd.DataFrame:
    """Add Activity_Score based on projects, hackathons, and GitHub activity."""
    df = df.copy()
    df["Activity_Score"] = compute_weighted_score(df, ACTIVITY_WEIGHTS)
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add all derived feature columns to the dataset."""
    engineered = df.copy()
    engineered = add_employability_score(engineered)
    engineered = add_technical_strength_score(engineered)
    engineered = add_professional_readiness_score(engineered)
    engineered = add_activity_score(engineered)
    return engineered


def save_engineered_data(
    df: pd.DataFrame,
    output_path: Path | None = None,
) -> Path:
    """Save the engineered dataset to a CSV file."""
    path = output_path or get_output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path


def run_feature_engineering(
    data_path: Path | None = None,
    output_path: Path | None = None,
) -> pd.DataFrame:
    """
    Load the dataset, create derived features, and save the result.

    Returns the engineered dataframe for use in other scripts.
    """
    df = load_dataset(data_path)
    engineered_df = engineer_features(df)
    saved_path = save_engineered_data(engineered_df, output_path)

    print("=" * 60)
    print("FEATURE ENGINEERING COMPLETE")
    print("=" * 60)
    print(f"Input rows: {len(df)}")
    print(f"New features added: Employability_Score, Technical_Strength_Score,")
    print("                      Professional_Readiness_Score, Activity_Score")
    print(f"Output saved to: {saved_path}")

    return engineered_df


def main() -> None:
    run_feature_engineering()


if __name__ == "__main__":
    main()
