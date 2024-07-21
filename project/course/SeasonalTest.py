import pandas as pd
from utils import read_data, pre_process_daily, pre_process_monthly
from statsmodels.tsa.seasonal import seasonal_decompose
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt


font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
plt.rcParams['font.sans-serif'] = [font.get_name()]
plt.rcParams['axes.unicode_minus'] = False
# 加载数据
raw_data = read_data('files/附件1.xlsx', ['2016', '2017', '2018', '2019', '2020', '2021'])
data = pre_process_monthly(raw_data)

# 将列转换为datetime对象，并将其设置为索引
data['日期'] = pd.to_datetime(data['日期'])
data.set_index('日期', inplace=True)

# 对列进行时间序列分解
result = seasonal_decompose(data['水沙通量'], model='additive')

# 绘制结果
result.plot()
plt.figure(figsize=(12, 8))
plt.title('月均水沙通量时间序列分析', fontproperties=font)
plt.show()
