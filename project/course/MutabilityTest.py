import numpy as np
import pandas as pd
import pymannkendall as mk
from scipy.stats import rankdata
from utils import read_data, pre_process_daily, pre_process_monthly
import ruptures as rpt
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt


def segment_mann_kendall(data, change_points):
    change_points = [0] + change_points + [len(data)]
    trends = []
    for i in range(len(change_points) - 1):
        start, end = change_points[i], change_points[i + 1]
        subset = data[start:end]
        result = mk.original_test(subset)
        if result.p < 0.10:  # 仅记录显著性水平小于0.10的趋势
            trends.append((start, end, result.trend, result.p, result.slope))
    return trends


def MannKendall_test(data):
    # 假设data是一个包含时间序列数据的Pandas DataFrame
    # water_flow 是你要检测的列（如水流量）
    mk_result = mk.original_test(data)
    return mk_result


def pettitt_test(data):
    n = len(data)
    r = rankdata(data)
    K = np.zeros(n)
    for i in range(n):
        K[i] = 2 * np.sum(r[:i + 1]) - (i + 1) * (n + 1)
    K_abs = np.abs(K)
    K_max = np.max(K_abs)
    tau = np.where(K_abs == K_max)[0][0]
    p_value = 2 * np.exp((-6 * (K_max ** 2)) / (n ** 3 + n ** 2))
    return tau, p_value


def recursive_pettitt(data, alpha=0.05, min_interval=12):
    change_points = []

    def detect(data, start_idx):
        if len(data) <= min_interval:
            return
        tau, p_value = pettitt_test(data)
        if p_value < alpha:
            change_points.append(start_idx + tau)
            detect(data[:tau], start_idx)
            detect(data[tau + 1:], start_idx + tau + 1)

    detect(data, 0)
    return sorted(change_points)


if __name__ == '__main__':
    raw_data = read_data('files/附件1.xlsx', ['2016', '2017', '2018', '2019', '2020', '2021'])
    data = pre_process_monthly(raw_data)
    target = '流量'

    """
    单点分析
    """
    mk_result = MannKendall_test(data[target])
    tau, p_value = pettitt_test(data[target])

    print("Mann-Kendall Test:")
    print(f"mk_result: {mk_result}")

    print("\nPettitt Test:")
    print(f"Change point at: {tau}")
    print(f"P-value: {p_value}")

    # 获取变点的日期
    change_date = data['日期'][tau]

    # 创建一个新的列表，其中包含Change Point的日期和其他固定间隔的日期
    x_ticks = data['日期'][::12].tolist()  # 这里我们选择每12个月一个标签，你可以根据需要调整
    if change_date not in x_ticks:
        x_ticks.append(change_date)
    x_ticks.sort()

    font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)  # 这里使用了宋体，你可以根据需要更改字体和路径
    plt.figure(figsize=(12, 8))
    plt.plot(data['日期'], data[target], label='平均水流量')
    plt.axvline(x=data['日期'][tau], color='r', linestyle='--', label='突变点')
    plt.title('月均水流量突变性检验', fontproperties=font)
    plt.xlabel('日期', fontproperties=font)
    plt.xticks(x_ticks, x_ticks, rotation=45)
    plt.ylabel(target, fontproperties=font)
    plt.legend(prop=font)
    plt.show()

    # 进行分段Mann-Kendall趋势检验
    # change_points = recursive_pettitt(data['流量'], alpha=0.01, min_interval=1)
    # # 创建并拟合PELT模型
    # # model = rpt.Pelt(model="rbf").fit(data['流量'].values)
    # # change_points = model.predict(pen=200)  # 调整pen值以控制变点数量
    #
    # # PELT方法返回的变点位置索引
    # change_points = change_points[:-1]  # 去掉最后一个元素，它表示序列结束
    #
    # trends = segment_mann_kendall(data['流量'].tolist(), change_points)
    #
    # # 打印结果
    # print("Change Points:", change_points)
    # for trend in trends:
    #     print(f"Segment {trend[0]}-{trend[1]}: Trend={trend[2]}, P-value={trend[3]}, Slope={trend[4]}")
    #
    # # 可视化
    # plt.figure(figsize=(12, 6))
    # plt.plot(data['日期'], data['流量'], label='Water Flow')
    # change_dates = [data['日期'][point] for point in change_points]
    # # 标注变点
    # for i, point in enumerate(change_points):
    #     color = 'r'
    #     # if trends[i][2] == 'increasing':
    #     #     color = 'r'
    #     # elif trends[i][2] == 'decreasing':
    #     #     color = 'g'
    #     if i == 0:
    #         plt.axvline(x=data['日期'][point], color=color, linestyle='--', label='Change Point')
    #     else:
    #         plt.axvline(x=data['日期'][point], color=color, linestyle='--')
    #
    # # 标注趋势段
    # # for trend in trends:
    # #     plt.axvline(x=data['index'][trend[0]] + 200, color='g', linestyle='-', label='Trend Start')
    # #     plt.axvline(x=data['index'][trend[1]] + 150, color='b', linestyle='-', label='Trend End')
    # plt.title('Water Flow Time Series with Trends and Change Points')
    # plt.xlabel('Date')
    # plt.xticks(change_points, change_dates, rotation=45)
    # plt.ylabel('Water Flow')
    # plt.legend()
    # plt.show()
