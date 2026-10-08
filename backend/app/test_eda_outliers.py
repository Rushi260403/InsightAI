import pandas as pd

from app.services.data_processor import (
    get_eda_outlier_analysis
)


data = {
    "Name": [
        "Rahul",
        "Amit",
        "Sneha",
        "Priya",
        "Rohit"
    ],

    "Age": [
        22,
        25,
        23,
        28,
        100
    ],

    "Salary": [
        30000,
        40000,
        35000,
        50000,
        500000
    ]
}


dataframe = pd.DataFrame(data)


outliers = get_eda_outlier_analysis(
    dataframe
)


print("Outlier Analysis:")

for outlier in outliers:
    print(outlier)