import pandas as pd

def clean_column_names(dataframe):
    """
    Clean column names by:
    - Removing leading/trailing spaces
    - Replacing spaces with underscores
    - Removing special characters
    - Removing repeated underscores
    - Removing underscores at the beginning/end
    """

    dataframe = dataframe.copy()

    dataframe.columns = (
        dataframe.columns
        .astype(str)
        .str.strip()
        .str.replace(" ", "_", regex=False)
        .str.replace(r"[^A-Za-z0-9_]", "", regex=True)
        .str.replace(r"_+", "_", regex=True)
        .str.strip("_")
    )

    return dataframe

def detect_missing_values(dataframe):
    """
    Detect missing values in each column.
    """

    missing_counts = dataframe.isna().sum()

    total_rows = len(dataframe)

    missing_details = []

    for column in dataframe.columns:

        missing_count = int(
            missing_counts[column]
        )

        if total_rows > 0:
            missing_percentage = round(
                (missing_count / total_rows) * 100,
                2
            )
        else:
            missing_percentage = 0.0

        missing_details.append({
            "column_name": str(column),
            "missing_values": missing_count,
            "missing_percentage": missing_percentage
        })

    return missing_details

def handle_missing_values(dataframe, strategy):
    """
    Handle missing values using:
    - mean
    - median
    - mode
    """

    dataframe = dataframe.copy()

    if strategy not in ["mean", "median", "mode"]:
        raise ValueError(
            "Strategy must be mean, median, or mode"
        )

    for column in dataframe.columns:

        # Skip columns that have no missing values
        if not dataframe[column].isna().any():
            continue

        # Numeric columns
        if pd.api.types.is_numeric_dtype(
            dataframe[column]
        ):

            if strategy == "mean":
                value = dataframe[column].mean()

            elif strategy == "median":
                value = dataframe[column].median()

            else:
                mode_values = dataframe[column].mode()

                if len(mode_values) == 0:
                    continue

                value = mode_values.iloc[0]

        # Text / categorical columns
        else:

            if strategy != "mode":
                continue

            mode_values = dataframe[column].mode()

            if len(mode_values) == 0:
                continue

            value = mode_values.iloc[0]

        dataframe[column] = dataframe[column].fillna(value)

    return dataframe

def remove_duplicate_rows(dataframe):
    """
    Remove completely duplicate rows.
    """

    dataframe = dataframe.copy()

    duplicate_count = int(
        dataframe.duplicated().sum()
    )

    cleaned_dataframe = dataframe.drop_duplicates(
        keep="first"
    ).reset_index(drop=True)

    return cleaned_dataframe, duplicate_count

def fix_basic_data_types(dataframe):
    """
    Detect and fix basic data types.

    Converts columns to numeric types when possible.
    Leaves text columns unchanged.
    """

    dataframe = dataframe.copy()

    for column in dataframe.columns:

        # Try converting the column to numeric
        converted_column = pd.to_numeric(
            dataframe[column],
            errors="coerce"
        )

        # Count original non-empty values
        original_values = dataframe[column].notna().sum()

        # Count successfully converted values
        converted_values = converted_column.notna().sum()

        # Convert only if all non-empty values are numeric
        if (
            original_values > 0
            and converted_values == original_values
        ):
            dataframe[column] = converted_column

    return dataframe
