from app.database import SessionLocal
from app.services.dataset_service import clean_user_dataset


db = SessionLocal()

try:

    result = clean_user_dataset(
        dataset_id=4,
        user_id=3,
        db=db
    )

    print("Cleaning successful!")

    print("\nOriginal rows:")
    print(result["original_rows"])

    print("\nCleaned rows:")
    print(result["cleaned_rows"])

    print("\nOriginal columns:")
    print(result["original_columns"])

    print("\nCleaned columns:")
    print(result["cleaned_columns"])

    print("\nDuplicates removed:")
    print(result["duplicates_removed"])

    print("\nMissing value strategy:")
    print(result["missing_value_strategy"])

    print("\nCleaned Dataset:")
    print(result["data"])

finally:
    db.close()
