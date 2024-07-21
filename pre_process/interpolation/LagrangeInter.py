import pandas as pd
from scipy.interpolate import lagrange


def LagrangeInter(df: pd.DataFrame, column: str, x: float) -> float:
    """
    Perform Lagrange interpolation on a specified column of a pandas DataFrame.

    Parameters:
    - df: pandas DataFrame
    - column: the name of the column to interpolate
    - x: the value at which to evaluate the interpolation

    Returns:
    - Interpolated value at x
    """
    y = df[column].values
    x_points = df.index.values
    poly = lagrange(x_points, y)
    return poly(x)


if __name__ == "__main__":
    # Example DataFrame
    df_example = pd.DataFrame({
        'Values': [1, 2, 3, 4, 5]
    }, index=[0, 1, 2, 3, 4])
    interpolated_lagrange = LagrangeInter(df_example, 'Values', 2)
    print(interpolated_lagrange)
