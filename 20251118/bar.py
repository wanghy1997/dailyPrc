import numpy as np
import matplotlib.pyplot as plt

# 类别顺序
categories = ['Sp', 'RK', 'LK', 'Ga', 'Es', 'Li', 'St', 'Ao', 'IVC', 'Pa', 'RAG', 'LAG', 'Du', 'Bl', 'P/U']

# 假阳性数据
ours_fp = np.array([974.6, 1483.3, 2114.8, 400.3, 116.5, 5950.4, 4928.5, 251.5, 284.8, 3684.6,
                    72.5, 38.5, 775., 2222.4, 249.7])
baseline_fp = np.array([1408., 1021.9, 936.8, 455.4, 121.4, 5011.5, 2601.9, 396.1, 436.8, 960.7,
                        77.3, 74.2, 1117.8, 2389.1, 124.3])

# 绘图设置
x = np.arange(len(categories))
width = 0.35

fig, ax = plt.subplots(figsize=(14, 5))
bars1 = ax.bar(x - width/2, baseline_fp, width, label='Baseline', color='#D9534F')
bars2 = ax.bar(x + width/2, ours_fp, width, label='Ours (HyCoStruct)', color='#5CB85C')

# 添加标签
ax.set_ylabel('False Positives (voxel count)')
ax.set_title('Per-class False Positives Comparison')
ax.set_xticks(x)
ax.set_xticklabels(categories, rotation=30)
ax.legend()

# 添加数值标注（可选）
for bar in bars1 + bars2:
    height = bar.get_height()
    ax.annotate(f'{height:.0f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 2),  # 垂直偏移
                textcoords="offset points",
                ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.4)
plt.show()