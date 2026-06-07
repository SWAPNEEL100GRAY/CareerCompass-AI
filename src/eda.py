"""Exploratory data analysis for the student placement career success dataset."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

DATA_FILENAME = "student_placement_career_success_dataset_2026.csv"
HISTOGRAM_COLUMNS = [
    "CGPA",
    "DSA_Problems_Solved",
    "Internships",
    "Projects_Count",
    "Resume_Score",
    "Salary_LPA",
]


def get_project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).resolve().parent.parent


def get_data_path() -> Path:
    """Return the path to the placement dataset CSV."""
    return get_project_root() / "data" / DATA_FILENAME


def get_reports_dir() -> Path:
    """Return the reports output directory, creating it if needed."""
    reports_dir = get_project_root() / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    return reports_dir


def load_dataset(data_path: Path | None = None) -> pd.DataFrame:
    """Load and return the student placement dataset."""
    path = data_path or get_data_path()
    return pd.read_csv(path)


def print_section(title: str) -> None:
    """Print a formatted section header."""
    print("=" * 60)
    print(title)
    print("=" * 60)


def print_dataset_overview(df: pd.DataFrame) -> None:
    """Print shape, column names, missing values, and descriptive statistics."""
    print_section("DATASET SHAPE")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    print()

    print_section("COLUMN NAMES")
    print(df.columns.tolist())
    print()

    print_section("MISSING VALUES")
    missing = df.isna().sum()
    missing = missing[missing > 0]
    if missing.empty:
        print("No missing values found.")
    else:
        print(missing.to_string())
    print()

    print_section("DESCRIPTIVE STATISTICS")
    print(df.describe(include="all"))


def plot_placement_status_distribution(df: pd.DataFrame, reports_dir: Path) -> None:
    """Plot and save the distribution of Placement_Status."""
    status_counts = df["Placement_Status"].value_counts().sort_index()

    print_section("PLACEMENT STATUS DISTRIBUTION")
    print(status_counts.to_string())
    print()

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(
        data=df,
        x="Placement_Status",
        hue="Placement_Status",
        ax=ax,
        palette="viridis",
        legend=False,
    )
    ax.set_title("Distribution of Placement Status")
    ax.set_xlabel("Placement Status")
    ax.set_ylabel("Count")

    output_path = reports_dir / "placement_status_distribution.png"
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Saved plot: {output_path}")


def plot_correlation_heatmap(df: pd.DataFrame, reports_dir: Path) -> None:
    """Plot and save a correlation heatmap for numerical features."""
    numeric_df = df.select_dtypes(include="number")
    correlation = numeric_df.corr()

    fig, ax = plt.subplots(figsize=(14, 12))
    sns.heatmap(
        correlation,
        annot=False,
        cmap="coolwarm",
        center=0,
        linewidths=0.5,
        ax=ax,
    )
    ax.set_title("Correlation Heatmap (Numerical Features)")

    output_path = reports_dir / "correlation_heatmap.png"
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Saved plot: {output_path}")


def plot_feature_histograms(df: pd.DataFrame, reports_dir: Path) -> None:
    """Plot and save histograms for selected numerical features."""
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    axes = axes.flatten()

    for ax, column in zip(axes, HISTOGRAM_COLUMNS):
        sns.histplot(df[column], kde=True, ax=ax, color="steelblue")
        ax.set_title(f"Distribution of {column}")
        ax.set_xlabel(column)
        ax.set_ylabel("Frequency")

    fig.suptitle("Feature Histograms", fontsize=14, y=1.02)

    output_path = reports_dir / "feature_histograms.png"
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved plot: {output_path}")


def run_eda(df: pd.DataFrame, reports_dir: Path) -> None:
    """Run the full exploratory data analysis workflow."""
    print_dataset_overview(df)
    plot_placement_status_distribution(df, reports_dir)
    plot_correlation_heatmap(df, reports_dir)
    plot_feature_histograms(df, reports_dir)


def main() -> None:
    sns.set_theme(style="whitegrid")
    df = load_dataset()
    reports_dir = get_reports_dir()
    run_eda(df, reports_dir)


if __name__ == "__main__":
    main()
