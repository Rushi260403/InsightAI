import pandas as pd

from app.services.data_processor import get_eda_summary


data = {
    "Name": [
        "Rahul",
        "Amit",
        "Sneha",
        "Priya"
    ],

    "Age": [
        22,
        25,
        23,
        28
    ],

    "City": [
        "Pune",
        "Mumbai",
        "Kolhapur",
        "Pune"
    ],

    "Salary": [
        30000,
        40000,
        35000,
        50000
    ]
}


dataframe = pd.DataFrame(data)


summary = get_eda_summary(dataframe)


print("EDA Summary:")
print(summary)


print("\nTotal Rows:")
print(summary["total_rows"])


print("\nTotal Columns:")
print(summary["total_columns"])


print("\nNumeric Columns:")
print(summary["numeric_columns"])


print("\nCategorical Columns:")
print(summary["categorical_columns"])


print("\nColumn Details:")

for column in summary["columns"]:
    print(column)