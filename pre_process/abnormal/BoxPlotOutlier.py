import pandas as pd


def BoxPlotOutlier(data: pd.DataFrame, column):
    """
    This function takes a dataframe and a column name as input and returns a list of outliers in the column.

    Parameters:
    - data: pandas DataFrame
    - column: str, the name of the column to find outliers in

    Returns:
    - outliers: pandas DataFrame, a DataFrame containing the outliers in the column
    """
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound  = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
    return outliers


if __name__ == "__main__":
    # Example DataFrame
    df_example = pd.DataFrame({
        'Values': [1, 2, 3, 4, 5, 100]
    })
    outliers = BoxPlotOutlier(df_example, 'Values')
    print(outliers)