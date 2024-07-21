import pandas as pd
import numpy as np


def NewtonInter(df: pd.DataFrame, column: str, x: float):
    """
        Perform Newton interpolation on a specified column of a pandas DataFrame.

        Parameters:
        - df: pandas DataFrame
        - column: the name of the column to interpolate
        - x: the value at which to evaluate the interpolation

        Returns:
        - Interpolated value at x
        """
    y = df[column].values
    x_points = df.index.values
    n = len(x_points)

    # Compute divided differences
    divided_diff = np.zeros((n, n))
    divided_diff[:, 0] = y

    for j in range(1, n):
        for i in range(n - j):
            divided_diff[i][j] = (divided_diff[i + 1][j - 1] - divided_diff[i][j - 1]) / (x_points[i + j] - x_points[i])

    # Compute Newton interpolation polynomial
    result = divided_diff[0, 0]
    prod = 1
    for i in range(1, n):
        prod *= (x - x_points[i - 1])
        result += divided_diff[0, i] * prod

    return result


if __name__ == "__main__":
    # Example DataFrame
    df_example = pd.DataFrame({
        'Values': [1, 2, np.nan, 4, 5]
    }, index=[0, 1, 2, 3, 4])
    interpolated_newton = NewtonInter(df_example.dropna(), 'Values', 2)
    print(interpolated_newton)