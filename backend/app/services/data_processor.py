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

def get_eda_summary(dataframe):
    """
    Generate a basic EDA summary of the dataset.
    """

    summary = {
        "total_rows": len(dataframe),
        "total_columns": len(dataframe.columns),
        "columns": [],
        "numeric_columns": [],
        "categorical_columns": []
    }

    for column in dataframe.columns:

        column_info = {
            "column_name": str(column),
            "data_type": str(dataframe[column].dtype),
            "missing_values": int(
                dataframe[column].isna().sum()
            ),
            "unique_values": int(
                dataframe[column].nunique()
            )
        }

        summary["columns"].append(column_info)

        # Identify numeric columns
        if pd.api.types.is_numeric_dtype(
            dataframe[column]
        ):
            summary["numeric_columns"].append(
                str(column)
            )

        # Identify categorical/text columns
        else:
            summary["categorical_columns"].append(
                str(column)
            )

    return summary

def get_eda_numeric_analysis(dataframe):
    """
    Generate statistical analysis for numeric columns.
    """

    numeric_dataframe = dataframe.select_dtypes(
        include="number"
    )

    analysis = []

    for column in numeric_dataframe.columns:

        analysis.append({
            "column_name": str(column),

            "count": int(
                numeric_dataframe[column].count()
            ),

            "mean": round(
                float(
                    numeric_dataframe[column].mean()
                ),
                2
            ),

            "median": round(
                float(
                    numeric_dataframe[column].median()
                ),
                2
            ),

            "minimum": float(
                numeric_dataframe[column].min()
            ),

            "maximum": float(
                numeric_dataframe[column].max()
            ),

            "standard_deviation": round(
                float(
                    numeric_dataframe[column].std()
                ),
                2
            )
        })

    return analysis

def get_eda_categorical_analysis(dataframe):
    """
    Generate analysis for categorical columns.

    Only the top 10 most frequent values
    are returned to keep the response lightweight.
    """

    categorical_dataframe = dataframe.select_dtypes(
        exclude="number"
    )

    analysis = []

    for column in categorical_dataframe.columns:

        value_counts = (
            categorical_dataframe[column]
            .value_counts(dropna=False)
        )

        top_values = value_counts.head(10)

        frequencies = []

        for value, count in top_values.items():

            if pd.isna(value):
                value = None
            else:
                value = str(value)

            frequencies.append({
                "value": value,
                "count": int(count)
            })

        if len(value_counts) > 0:

            most_frequent_value = value_counts.index[0]

            if pd.isna(most_frequent_value):
                most_frequent_value = None
            else:
                most_frequent_value = str(
                    most_frequent_value
                )

        else:
            most_frequent_value = None

        analysis.append({
            "column_name": str(column),

            "unique_values": int(
                categorical_dataframe[column].nunique(
                    dropna=True
                )
            ),

            "most_frequent_value":
                most_frequent_value,

            "frequencies": frequencies
        })

    return analysis

def get_eda_correlation_analysis(dataframe):
    """
    Generate correlation analysis
    between numeric columns.
    """

    numeric_dataframe = dataframe.select_dtypes(
        include="number"
    )

    # Need at least two numeric columns
    if len(numeric_dataframe.columns) < 2:
        return []

    correlation_matrix = (
        numeric_dataframe.corr()
    )

    correlations = []

    columns = list(
        correlation_matrix.columns
    )

    for i in range(len(columns)):

        for j in range(i + 1, len(columns)):

            column_1 = columns[i]
            column_2 = columns[j]

            correlation_value = (
                correlation_matrix
                .loc[column_1, column_2]
            )

            if pd.isna(correlation_value):
                continue

            correlations.append({
                "column_1": str(column_1),
                "column_2": str(column_2),
                "correlation": round(
                    float(correlation_value),
                    2
                )
            })

    return correlations

def get_eda_outlier_analysis(dataframe):
    """
    Detect outliers in numeric columns
    using the IQR method.
    """

    numeric_dataframe = dataframe.select_dtypes(
        include="number"
    )

    outliers = []

    for column in numeric_dataframe.columns:

        q1 = numeric_dataframe[column].quantile(0.25)
        q3 = numeric_dataframe[column].quantile(0.75)

        iqr = q3 - q1

        lower_limit = q1 - (1.5 * iqr)
        upper_limit = q3 + (1.5 * iqr)

        outlier_values = numeric_dataframe[
            (numeric_dataframe[column] < lower_limit)
            | (numeric_dataframe[column] > upper_limit)
        ][column]

        outliers.append({
            "column_name": str(column),
            "q1": round(float(q1), 2),
            "q3": round(float(q3), 2),
            "iqr": round(float(iqr), 2),
            "lower_limit": round(
                float(lower_limit),
                2
            ),
            "upper_limit": round(
                float(upper_limit),
                2
            ),
            "outlier_count": int(
                len(outlier_values)
            ),
            "outlier_values": [
                float(value)
                for value in outlier_values
            ]
        })

    return outliers