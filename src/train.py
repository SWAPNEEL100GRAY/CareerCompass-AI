"""
Train career readiness models and save the best one.

This script:
1. Loads and cleans the dataset
2. Encodes categorical columns
3. Splits data into train and test sets
4. Trains Logistic Regression and Random Forest models
5. Compares accuracy and saves the best model
"""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DATA_FILENAME = "student_placement_career_success_dataset_2026.csv"
TARGET_COLUMN = "Placement_Status"
MODEL_FILENAME = "placement_model.joblib"

# Columns that are not used as model inputs
COLUMNS_TO_DROP = [TARGET_COLUMN, "Salary_LPA"]

# Categorical columns that need encoding before training
CATEGORICAL_COLUMNS = ["Gender", "College_Tier", "Specialization"]

# Reproducible random split and model training
RANDOM_STATE = 42
TEST_SIZE = 0.2


def get_project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).resolve().parent.parent


def get_data_path() -> Path:
    """Return the path to the dataset CSV file."""
    return get_project_root() / "data" / DATA_FILENAME


def get_models_dir() -> Path:
    """Return the models folder, creating it if it does not exist."""
    models_dir = get_project_root() / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    return models_dir


def load_data() -> pd.DataFrame:
    """Load the raw dataset from the data folder."""
    return pd.read_csv(get_data_path())


def create_placement_target(df: pd.DataFrame) -> pd.DataFrame:
    """
    Make sure the target column has two classes for training.

    In this dataset, every student has the same placement label. A classifier
    cannot learn from a single label, so we build a career readiness
    score from employability features and label students above the
    median score as 1 and others as 0.
    """
    if df[TARGET_COLUMN].nunique() > 1:
        return df

    print(
        "Note: All rows share the same Placement_Status value. "
        "Creating a career readiness label for model training."
    )

    readiness_score = (
        df["CGPA"] * 10 * 0.25
        + df["Mock_Interview_Score"] * 0.25
        + df["Resume_Score"] * 0.25
        + df["Communication_Skills"] * 0.25
    )

    df = df.copy()
    df[TARGET_COLUMN] = (readiness_score >= readiness_score.median()).astype(int)
    print(f"New target distribution:\n{df[TARGET_COLUMN].value_counts()}\n")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the dataset by removing duplicates and missing values.

    Salary_LPA is not used as a feature because salary is recorded after
    placement. Using it would leak future information into the model.
    """
    cleaned = df.copy()

    # Remove duplicate rows
    cleaned = cleaned.drop_duplicates()

    # Remove rows with missing values (this dataset has none, but this is good practice)
    cleaned = cleaned.dropna()

    # Ensure the target column is usable for classification
    cleaned = create_placement_target(cleaned)

    return cleaned


def split_features_and_target(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Separate feature columns (X) from the target column (y)."""
    X = df.drop(columns=COLUMNS_TO_DROP)
    y = df[TARGET_COLUMN]
    return X, y


def encode_categorical_features(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, list[str]]:
    """
    Convert categorical text columns into numeric columns.

    One-hot encoding creates a new column for each category.
    We fit the encoding on the training set and apply the same columns to the test set.
    """
    X_train_encoded = pd.get_dummies(
        X_train,
        columns=CATEGORICAL_COLUMNS,
        drop_first=True,
    )
    X_test_encoded = pd.get_dummies(
        X_test,
        columns=CATEGORICAL_COLUMNS,
        drop_first=True,
    )

    # Make sure the test set has the same columns as the training set
    X_test_encoded = X_test_encoded.reindex(
        columns=X_train_encoded.columns,
        fill_value=0,
    )

    feature_columns = X_train_encoded.columns.tolist()
    return X_train_encoded, X_test_encoded, feature_columns


def train_logistic_regression(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> tuple[LogisticRegression, StandardScaler, float]:
    """
    Train a Logistic Regression model.

    Logistic Regression works best when numeric features are on a similar scale,
    so we apply StandardScaler before training.
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)
    model.fit(X_train_scaled, y_train)

    predictions = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, predictions)

    return model, scaler, accuracy


def train_random_forest(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> tuple[RandomForestClassifier, float]:
    """
    Train a Random Forest model.

    Random Forest does not require feature scaling, so we train directly
    on the encoded feature matrix.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    return model, accuracy


def save_best_model(
    best_model_name: str,
    model,
    scaler: StandardScaler | None,
    feature_columns: list[str],
) -> Path:
    """Save the winning model and everything needed for prediction."""
    model_bundle = {
        "model_name": best_model_name,
        "model": model,
        "scaler": scaler,
        "feature_columns": feature_columns,
        "categorical_columns": CATEGORICAL_COLUMNS,
        "target_column": TARGET_COLUMN,
    }

    model_path = get_models_dir() / MODEL_FILENAME
    joblib.dump(model_bundle, model_path)
    return model_path


def main() -> None:
    print("=" * 60)
    print("CAREER READINESS & RECOMMENDATION SYSTEM MODEL TRAINING")
    print("=" * 60)

    # Step 1: Load and clean the dataset
    print("\n[1/5] Loading and cleaning data...")
    df = load_data()
    df = clean_data(df)
    print(f"Dataset shape after cleaning: {df.shape}")

    # Step 2: Split features and target
    print("\n[2/5] Preparing features and target...")
    X, y = split_features_and_target(df)

    # Step 3: Split into train and test sets
    print("\n[3/5] Splitting into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")

    # Step 4: Encode categorical columns
    print("\n[4/5] Encoding categorical columns...")
    X_train_encoded, X_test_encoded, feature_columns = encode_categorical_features(
        X_train,
        X_test,
    )
    print(f"Total features after encoding: {len(feature_columns)}")

    # Step 5: Train and compare models
    print("\n[5/5] Training models...")
    lr_model, lr_scaler, lr_accuracy = train_logistic_regression(
        X_train_encoded,
        y_train,
        X_test_encoded,
        y_test,
    )
    rf_model, rf_accuracy = train_random_forest(
        X_train_encoded,
        y_train,
        X_test_encoded,
        y_test,
    )

    print("\n" + "=" * 60)
    print("MODEL COMPARISON")
    print("=" * 60)
    print(f"Logistic Regression accuracy: {lr_accuracy:.4f}")
    print(f"Random Forest accuracy:       {rf_accuracy:.4f}")

    # Pick the model with higher accuracy.
    # If both are equal, Random Forest is saved as the default choice.
    if rf_accuracy >= lr_accuracy:
        best_model_name = "Random Forest"
        best_model = rf_model
        best_scaler = None
        best_accuracy = rf_accuracy
    else:
        best_model_name = "Logistic Regression"
        best_model = lr_model
        best_scaler = lr_scaler
        best_accuracy = lr_accuracy

    model_path = save_best_model(
        best_model_name,
        best_model,
        best_scaler,
        feature_columns,
    )

    print("\n" + "=" * 60)
    print("TRAINING COMPLETE")
    print("=" * 60)
    print(f"Best model: {best_model_name}")
    print(f"Best accuracy: {best_accuracy:.4f}")
    print(f"Saved to: {model_path}")


if __name__ == "__main__":
    main()
