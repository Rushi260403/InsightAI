import os

from sqlalchemy.orm import Session

from app.models import Dataset

from app.services.data_processor import (
    read_dataset,
    validate_dataset,
    get_dataset_profile,
    get_numeric_statistics
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