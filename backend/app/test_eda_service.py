from app.database import SessionLocal
from app.services.dataset_service import generate_eda_report


db = SessionLocal()

try:
    report = generate_eda_report(
        dataset_id=4,
        user_id=3,
        db=db
    )

    print("EDA Service successful!")

    print("\nDataset:")
    print(report["dataset_name"])

    print("\nSummary:")
    print(report["summary"])

    print("\nNumeric Analysis:")
    print(report["numeric_analysis"])

    print("\nCategorical Analysis:")
    print(report["categorical_analysis"])

    print("\nCorrelation Analysis:")
    print(report["correlation_analysis"])

    print("\nOutlier Analysis:")
    print(report["outlier_analysis"])

finally:
    db.close()