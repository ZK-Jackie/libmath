import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils import read_data, pre_process_daily, pre_process_monthly
from matplotlib.font_manager import FontProperties
import pywt
from pywt import cwt
from scipy.signal import morlet

raw_data = read_data('files/附件1.xlsx', ['2016', '2017', '2018', '2019', '2020', '2021'])
data = pre_process_monthly(raw_data)
target = '水沙通量'
date = '日期'

# 加载数据
flow = data[target].values
dates = data[date].values

# 进行连续小波变换
scales = np.arange(1, 64)
coeffs, frequencies = cwt(flow, scales, 'morl')  # 直接使用小波名称的字符串

# 绘制实部等值线图并填充颜色
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)  # 这里使用了宋体，你可以根据需要更改字体和路径
plt.figure(figsize=(12, 8))
plt.contourf(dates, scales, coeffs.real, cmap='coolwarm')
plt.contour(dates, scales, coeffs.real, colors='k')  # 添加等值线
plt.xlabel('日期', fontproperties=font)
x_ticks = data['日期'][::12].tolist()  # 这里我们选择每12个月一个标签，你可以根据需要调整
plt.xticks(x_ticks, x_ticks, rotation=45)
plt.ylabel('尺度', fontproperties=font)
plt.title('2016-2021年月均水沙通量小波系数实部等值线图', fontproperties=font)
plt.show()
