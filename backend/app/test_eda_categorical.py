import pandas as pd

from app.services.data_processor import (
    get_eda_categorical_analysis
)


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


analysis = get_eda_categorical_analysis(
    dataframe
)


print("Categorical Analysis:")

for column in analysis:
    print(column)