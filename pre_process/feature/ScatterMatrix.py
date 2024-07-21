import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def ScatterMatrix(data, n):
    """
    绘制一个n*n的散点图矩阵，每个格子表示n个变量之间的散点图。

    参数:
    data -- 一个二维数组或pandas DataFrame，其中每一列是一个变量
    n -- 变量的数量，也是格子矩阵的大小
    """
    # 确保数据是numpy数组格式
    if isinstance(data, pd.DataFrame):
        data = data.values
    # 创建一个n*n的子图网格
    fig, axes = plt.subplots(nrows=n, ncols=n, figsize=(15, 15))
    # 填充每个格子
    for i in range(n):
        for j in range(n):
            ax = axes[i, j]
            # 如果是主对角线上的格子，绘制直方图
            if i == j:
                ax.hist(data[:, i], bins=10)
                ax.set_xticks([])
                ax.set_yticks([])
                # 在左上角的格子上添加标签
                if i == 0:
                    # TODO 标题名字设为变量名或列名
                    ax.set_ylabel('Frequency')
            else:
                # 绘制散点图
                ax.scatter(data[:, j], data[:, i], alpha=0.5)
                ax.set_xticks([])
                ax.set_yticks([])
                # 在最左侧和最下侧格子边上添加标签 + y轴刻度
                if j == 0:
                    # TODO 标题名字设为变量名或列名，刻度根据数据范围动态设置
                    ax.set_ylabel(f'Variable {i}')
                    ax.set_yticks([])
                if i == n - 1:
                    ax.set_xlabel(f'Variable {j}')
                    ax.set_xticks([])

    # 调整布局
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # 示例数据
    np.random.seed(0)
    data = np.random.rand(100, 5)  # 生成一个100x5的随机数据矩阵

    # 假设我们想要5个变量之间的散点图矩阵
    ScatterMatrix(data, 5)
