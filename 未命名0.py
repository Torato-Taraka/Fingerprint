import numpy as np
import matplotlib.pyplot as plt
"""
x = np.array([61.5, 34, 25, 20, 12.6, 5, 0, 0, 0])
y = np.array([0, 0, 0, 0, 15.5, 91.1, 98.3, 100, 100])
i = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])

plt.scatter(i, x, 8, 'red')
plt.plot(i, x, ':', color = 'red', label = 'FRR')
plt.xlabel("threshold")
plt.scatter(i, y, 8, 'blue')
plt.plot(i, y, linewidth = 0.7, linestyle = '--', color = 'blue', label = 'FAR')
plt.ylabel("rate")
plt.legend(loc = 'best')
plt.title("FVC2004 1a Database")
plt.show()
"""

x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
y1 = np.array([0.14, 0.14, 0.13, 0.17, 0.21, 0.13, 0.18, 0.17, 0.19, 0.24])
y2 = np.array([0.669, 0.706, 0.598, 0.807, 0.874, 0.619, 0.857, 0.934, 0.788, 1.097])
y2 = y2 + y1

plt.bar(x, y2, label="模板加密用时", color='orange')
plt.bar(x, y1, label="模板生成用时", color='green')

plt.xticks(np.arange(len(x)), x, rotation=0, fontsize=10)  # 数量多可以采用270度，数量少可以采用340度，得到更好的视图
plt.legend(loc="upper left")  # 防止label和图像重合显示不出来
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.ylabel('时间')
plt.xlabel('模板编号')
plt.rcParams['figure.figsize'] = (12, 8)  # 尺寸
plt.title("指纹模板加密时间开销")
plt.show()