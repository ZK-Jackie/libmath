import pandas as pd


def ScatterOutlier(threshold=1, **kwargs):
    # 判断输入参数是否合法
    dimension = 0
    if "data_x" in kwargs:
        data_x = kwargs["data_x"]
        dimension += 1
    else:
        raise ValueError("data_x must be provided")
    if "data_y" in kwargs:
        dimension += 1
        data_y = kwargs["data_y"]
    if "data_z" in kwargs:
        data_z = kwargs["data_z"]
        dimension += 1
    # 建立二维或三位的DataFrame
    if dimension == 1:
        data = pd.DataFrame({
            'data_x': data_x
        })
    elif dimension == 2:
        data = pd.DataFrame({
            'data_x': data_x,
            'data_y': data_y
        })
    elif dimension == 3:
        data = pd.DataFrame({
            'data_x': data_x,
            'data_y': data_y,
            'data_z': data_z
        })
    else:
        raise ValueError("Invalid dimension")
    # 计算每个点之间的欧几里得距离
    if dimension == 1:
        data['distance'] = data['data_x'] - data['data_x'].mean()
    elif dimension == 2:
        data['distance'] = ((data['data_x'] - data['data_x'].mean()) ** 2 + (
                data['data_y'] - data['data_y'].mean()) ** 2) ** 0.5
    elif dimension == 3:
        data['distance'] = ((data['data_x'] - data['data_x'].mean()) ** 2 + (
                data['data_y'] - data['data_y'].mean()) ** 2 + (data['data_z'] - data['data_z'].mean()) ** 2) ** 0.5
    # 计算标准差
    std = data['distance'].std()
    # 计算阈值
    threshold = std * threshold
    # 找出异常值
    outliers = data[data['distance'] > threshold]
    # 返回异常值
    return outliers


if __name__ == "__main__":
    # Example DataFrame
    df_example = pd.DataFrame({
        'Values1': [1, 3, 2, 0, 2, 4],
        'Values2': [2, 1, 1, 1, 4, 4],
        'Values3': [0, 4, 5, 6, 3, 2]
    })
    outliers = ScatterOutlier(data_x=df_example['Values1'],
                              data_y=df_example['Values2'],
                              data_z=df_example['Values3'],
                              threshold=3)
    print(outliers)
