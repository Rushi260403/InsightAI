from app.services.data_processor import (
    read_dataset,
    get_basic_info,
    validate_dataset,
    get_dataset_profile,
    get_numeric_statistics
)


file_path = r"D:\InsightAI\datasets\uploads\user_1_Chocolate_Sales.csv"

dataframe = read_dataset(
    file_path,
    ".csv"
)

print("Dataset loaded successfully!")

print("\nDataset:")
print(dataframe)

print("\nBasic Information:")

info = get_basic_info(dataframe)

print("Rows:", info["rows"])
print("Columns:", info["columns"])
print("Column Names:", info["column_names"])


print("\nDataset Validation:")

validation = validate_dataset(dataframe)

print("Valid:", validation["is_valid"])
print("Errors:", validation["errors"])
print("Warnings:", validation["warnings"])

print("\nDataset Profile:")

profile = get_dataset_profile(dataframe)

print("Total Rows:", profile["total_rows"])
print("Total Columns:", profile["total_columns"])

print("\nColumn Details:")

for column in profile["columns"]:
    print(column)

print("\nDuplicate Rows:", profile["duplicate_rows"])
print(
    "Duplicate Percentage:",
    profile["duplicate_percentage"]
)

print("\nNumeric Statistics:")

statistics = get_numeric_statistics(dataframe)

for column in statistics:
    print(column)