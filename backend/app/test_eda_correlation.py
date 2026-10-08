import pandas as pd

from app.services.data_processor import (
    get_eda_correlation_analysis
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


correlations = get_eda_correlation_analysis(
    dataframe
)


print("Correlation Analysis:")

for correlation in correlations:
    print(correlation)