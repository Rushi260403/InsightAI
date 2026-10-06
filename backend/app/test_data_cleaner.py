import pandas as pd

from app.services.data_cleaner import (
    clean_column_names,
    detect_missing_values,
    handle_missing_values,
    remove_duplicate_rows,
    fix_basic_data_types
)


data = {
    " Customer Name! ": ["Rahul", "Amit"],
    " Age ": [22, 25],
    "City Name@": ["Pune", "Mumbai"],
    "Salary ($)": [30000, 40000]
}


dataframe = pd.DataFrame(data)


print("Original Dataset:")
print(dataframe)


cleaned_dataframe = clean_column_names(
    dataframe
)


print("\nAfter Column Name Cleaning:")
print(cleaned_dataframe)


print("\nMissing Values Before Handling:")

missing_details = detect_missing_values(
    cleaned_dataframe
)

for column in missing_details:
    print(column)


print("\nHandling Missing Values:")

filled_dataframe = handle_missing_values(
    cleaned_dataframe,
    "mode"
)


print(filled_dataframe)


print("\nMissing Values After Handling:")

missing_after = detect_missing_values(
    filled_dataframe
)

for column in missing_after:
    print(column)

print("\nDuplicate Row Removal:")

duplicate_cleaned_dataframe, duplicate_count = (
    remove_duplicate_rows(
        cleaned_dataframe
    )
)

print(
    "Duplicate rows found:",
    duplicate_count
)

print("\nDataset after duplicate removal:")

print(duplicate_cleaned_dataframe)

print("\nData Type Detection/Fixing:")

type_data = {
    "Customer_Name": ["Rahul", "Amit", "Sneha"],
    "Age": ["22", "25", "23"],
    "Salary": ["30000", "40000", "35000"],
    "City": ["Pune", "Mumbai", "Kolhapur"]
}

type_dataframe = pd.DataFrame(type_data)

print("\nBefore fixing:")
print(type_dataframe.dtypes)

fixed_dataframe = fix_basic_data_types(
    type_dataframe
)

print("\nAfter fixing:")
print(fixed_dataframe.dtypes)

print("\nFixed Dataset:")
print(fixed_dataframe)