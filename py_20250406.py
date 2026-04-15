import matplotlib.pyplot as plt
import numpy as np

# 设置全局字体为 Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'

# 数据
years = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
training_data = [35, 35, 200, 200, 200, 285, 285, 335, 369, 1251]
testing_data = [15, 25, 38, 53, 191, 146, 191, 166, 166, 570]

# 计算总数据
total_data = [tr + te for tr, te in zip(training_data, testing_data)]

# 绘制柱状图
fig, ax = plt.subplots(figsize=(10, 6))

# 设置柱状图背景颜色
ax.set_facecolor('#e6f7ff')  # Light blue background for the axes

# 使用更自然的颜色
bar1 = ax.bar(years, training_data, label='Training Data', color='#F19025')
bar2 = ax.bar(years, testing_data, bottom=training_data, label='Testing Data', color='#EFE22C')

# 添加折线图表示总数据
ax.plot(years, total_data, marker='o', color='#D7487A', linewidth=2, label='Total Data Line', markersize=5)

# 设置标签和标题
ax.set_xlabel('Year', fontsize=14)
ax.set_ylabel('Data Count', fontsize=14)
ax.set_title('Visualization of changes in the number of BraTS DataSets', fontsize=16)

# 确保所有年份都显示在横轴上
ax.set_xticks(years)  # Set x-ticks to be the years
ax.set_xticklabels(years)  # Ensure labels are displayed

# 添加图例
ax.legend(fontsize=12)

# 设置网格
ax.yaxis.grid(True, linestyle='--', alpha=0.7)

# 优化布局
plt.tight_layout()

# 显示图形
plt.show()
