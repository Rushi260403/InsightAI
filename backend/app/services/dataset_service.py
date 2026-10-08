import os

from sqlalchemy.orm import Session

from app.models import Dataset

from app.services.data_processor import (
    read_dataset,
    validate_dataset,
    get_dataset_profile,
    get_numeric_statistics,
    get_eda_summary,
    get_eda_numeric_analysis,
    get_eda_categorical_analysis,
    get_eda_correlation_analysis,
    get_eda_outlier_analysis
)

from app.services.data_cleaner import (
    clean_column_names,
    handle_missing_values,
    remove_duplicate_rows,
    fix_basic_data_types
)

def load_user_dataset(
    dataset_id: int,
    user_id: int,
    db: Session
):
    """
    Find a dataset belonging to the logged-in user,
    load it using Pandas, and validate it.
    """

    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.user_id == user_id
    ).first()

    if not dataset:
        raise ValueError("Dataset not found")

    if not os.path.exists(dataset.file_path):
        raise ValueError("Dataset file not found")

    dataframe = read_dataset(
        dataset.file_path,
        dataset.file_type
    )

    validation = validate_dataset(dataframe)

    if not validation["is_valid"]:
        raise ValueError(
            "; ".join(validation["errors"])
        )

    return dataset, dataframe


def generate_dataset_profile(
    dataset_id: int,
    user_id: int,
    db: Session
):
    """
    Load and generate a complete profile
    for the user's dataset.
    """

    dataset, dataframe = load_user_dataset(
        dataset_id,
        user_id,
        db
    )

    profile = get_dataset_profile(dataframe)

    numeric_statistics = get_numeric_statistics(
        dataframe
    )

    return {
        "dataset_id": dataset.id,
        "dataset_name": dataset.dataset_name,
        "file_name": dataset.file_name,
        "profile": profile,
        "numeric_statistics": numeric_statistics
    }

def clean_user_dataset(
    dataset_id: int,
    user_id: int,
    db: Session,
    missing_value_strategy: str = "median"
):
    """
    Load a user's dataset and perform basic cleaning.
    """

    # Load dataset
    dataset, dataframe = load_user_dataset(
        dataset_id,
        user_id,
        db
    )

    # Store original information
    original_rows = len(dataframe)
    original_columns = len(dataframe.columns)

    # Step 1: Clean column names
    dataframe = clean_column_names(dataframe)

    # Step 2: Handle missing values
    dataframe = handle_missing_values(
        dataframe,
        missing_value_strategy
    )

    # Step 3: Remove duplicate rows
    dataframe, duplicate_count = remove_duplicate_rows(
        dataframe
    )

    # Step 4: Fix basic data types
    dataframe = fix_basic_data_types(
        dataframe
    )

    return {
        "dataset_id": dataset.id,
        "dataset_name": dataset.dataset_name,
        "original_rows": original_rows,
        "original_columns": original_columns,
        "cleaned_rows": len(dataframe),
        "cleaned_columns": len(dataframe.columns),
        "duplicates_removed": duplicate_count,
        "missing_value_strategy": missing_value_strategy,
        "data": dataframe
    }

def generate_eda_report(
    dataset_id: int,
    user_id: int,
    db: Session
):
    """
    Generate a complete EDA report
    for a user's dataset.
    """

    dataset, dataframe = load_user_dataset(
        dataset_id,
        user_id,
        db
    )

    eda_summary = get_eda_summary(
        dataframe
    )

    numeric_analysis = get_eda_numeric_analysis(
        dataframe
    )

    categorical_analysis = get_eda_categorical_analysis(
        dataframe
    )

    correlation_analysis = get_eda_correlation_analysis(
        dataframe
    )

    outlier_analysis = get_eda_outlier_analysis(
        dataframe
    )

    return {
        "dataset_id": dataset.id,
        "dataset_name": dataset.dataset_name,
        "summary": eda_summary,
        "numeric_analysis": numeric_analysis,
        "categorical_analysis": categorical_analysis,
        "correlation_analysis": correlation_analysis,
        "outlier_analysis": outlier_analysis
    }