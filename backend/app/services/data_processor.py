import pandas as pd


def read_dataset(file_path: str, file_type: str):
    """
    Read a CSV or Excel dataset using Pandas.
    """

    if file_type == ".csv":
        dataframe = pd.read_csv(file_path)

    elif file_type in [".xlsx", ".xls"]:
        dataframe = pd.read_excel(file_path)

    else:
        raise ValueError("Unsupported file type")

    return dataframe


def get_basic_info(dataframe):
    """
    Get basic information about the dataset.
    """

    return {
        "rows": len(dataframe),
        "columns": len(dataframe.columns),
        "column_names": list(dataframe.columns)
    }

def validate_dataset(dataframe):
    """
    Perform basic validation on a Pandas DataFrame.
    """

    errors = []
    warnings = []

    # Check if dataset is empty
    if dataframe.empty:
        errors.append("Dataset is empty")

    # Check if dataset has columns
    if len(dataframe.columns) == 0:
        errors.append("Dataset has no columns")

    # Check column names
    for column in dataframe.columns:
        if str(column).strip() == "":
            errors.append("Dataset contains an empty column name")

    # Check completely empty columns
    empty_columns = []

    for column in dataframe.columns:
        if dataframe[column].isna().all():
            empty_columns.append(str(column))

    if empty_columns:
        warnings.append(
            f"Completely empty columns: {empty_columns}"
        )

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }

def get_dataset_profile(dataframe):
    """
    Generate a basic profile of the dataset.
    """

    total_rows = len(dataframe)
    total_columns = len(dataframe.columns)

    # Missing values
    missing_values = dataframe.isna().sum()

    # Missing percentage
    if total_rows > 0:
        missing_percentage = (
            missing_values / total_rows * 100
        ).round(2)
    else:
        missing_percentage = missing_values

    # Duplicate rows
    duplicate_rows = dataframe.duplicated().sum()

    if total_rows > 0:
        duplicate_percentage = round(
            (duplicate_rows / total_rows) * 100,
            2
        )
    else:
        duplicate_percentage = 0

    # Column information
    columns = []

    for column in dataframe.columns:
        columns.append({
            "column_name": str(column),
            "data_type": str(dataframe[column].dtype),
            "missing_values": int(missing_values[column]),
            "missing_percentage": float(
                missing_percentage[column]
            )
        })

    return {
        "total_rows": total_rows,
        "total_columns": total_columns,
        "columns": columns,
        "duplicate_rows": int(duplicate_rows),
        "duplicate_percentage": duplicate_percentage
    }

def get_numeric_statistics(dataframe):
    """
    Generate basic statistics for numeric columns.
    """

    numeric_dataframe = dataframe.select_dtypes(
        include="number"
    )

    statistics = []

    for column in numeric_dataframe.columns:

        statistics.append({
            "column_name": str(column),
            "count": int(numeric_dataframe[column].count()),
            "mean": round(
                float(numeric_dataframe[column].mean()),
                2
            ),
            "median": round(
                float(numeric_dataframe[column].median()),
                2
            ),
            "minimum": float(
                numeric_dataframe[column].min()
            ),
            "maximum": float(
                numeric_dataframe[column].max()
            ),
            "standard_deviation": round(
                float(numeric_dataframe[column].std()),
                2
            )
        })

    return statistics