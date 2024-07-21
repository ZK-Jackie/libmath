import numpy as np


def GetCorMatrix(data):
    """
    Get the correlation matrix of the data.
    """
    return np.corrcoef(data, rowvar=False)


if __name__ == "__main__":
    data = np.random.rand(100, 5)
    cov_matrix = GetCorMatrix(data)
    print(cov_matrix)