import time

from app.database import SessionLocal
from app.services.dataset_service import load_user_dataset
from app.services.data_processor import (
    get_eda_summary,
    get_eda_numeric_analysis,
    get_eda_categorical_analysis,
    get_eda_correlation_analysis,
    get_eda_outlier_analysis
)


# Change these if required
DATASET_ID = 2
USER_ID = 1


db = SessionLocal()

try:
    print("Starting EDA performance test...")
    print()

    # Load dataset
    start = time.perf_counter()

    dataset, dataframe = load_user_dataset(
        DATASET_ID,
        USER_ID,
        db
    )

    end = time.perf_counter()

    print("Dataset:", dataset.dataset_name)
    print("Rows:", len(dataframe))
    print("Columns:", len(dataframe.columns))
    print("File type:", dataset.file_type)
    print(
        "Load time:",
        round(end - start, 3),
        "seconds"
    )

    print()

    # Summary
    start = time.perf_counter()

    get_eda_summary(dataframe)

    end = time.perf_counter()

    print(
        "EDA Summary:",
        round(end - start, 3),
        "seconds"
    )

    # Numeric analysis
    start = time.perf_counter()

    get_eda_numeric_analysis(dataframe)

    end = time.perf_counter()

    print(
        "Numeric Analysis:",
        round(end - start, 3),
        "seconds"
    )

    # Categorical analysis
    start = time.perf_counter()

    get_eda_categorical_analysis(dataframe)

    end = time.perf_counter()

    print(
        "Categorical Analysis:",
        round(end - start, 3),
        "seconds"
    )

    # Correlation
    start = time.perf_counter()

    get_eda_correlation_analysis(dataframe)

    end = time.perf_counter()

    print(
        "Correlation Analysis:",
        round(end - start, 3),
        "seconds"
    )

    # Outlier detection
    start = time.perf_counter()

    get_eda_outlier_analysis(dataframe)

    end = time.perf_counter()

    print(
        "Outlier Analysis:",
        round(end - start, 3),
        "seconds"
    )

    print()
    print("Performance test completed!")

finally:
    db.close()