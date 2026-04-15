import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from sklearn.manifold import TSNE

# 创建画布和布局
fig = plt.figure(figsize=(12, 6), dpi=150)
gs = GridSpec(2, 3, width_ratios=[1, 0.05, 1], height_ratios=[1, 0.6])
ax1 = fig.add_subplot(gs[0, 0])  # 传统方法
ax2 = fig.add_subplot(gs[0, 2])  # TumorAL
ax3 = fig.add_subplot(gs[1, :])  # t-SNE对比

# ========== 传统方法流程 ==========
# 流程箭头
ax1.annotate('', xy=(0.8, 0.5), xytext=(0.1, 0.5),
             arrowprops=dict(arrowstyle='->', lw=2, color='#FF6B6B'))

# 模块标注
modules = [
    (0.1, 0.5, 'Input Image\n(MRI)'),
    (0.4, 0.5, 'Deterministic Model\n(e.g. U-Net)'),
    (0.7, 0.5, 'Entropy Calculation\n(Uncertainty Map)')
]
for x, y, text in modules:
    ax1.text(x, y, text, ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='#FF6B6B', boxstyle='round'))

# 冗余样本可视化
np.random.seed(42)
ax1.scatter(np.random.normal(0.7, 0.05, 100),
           np.random.normal(0.3, 0.1, 100),
           s=50, c='#FF6B6B', alpha=0.6, edgecolors='white')

# 单峰分布
x = np.linspace(-3, 3, 100)
ax1.plot(x*0.1 + 0.4, np.exp(-x**2)*0.2 + 0.7,
        color='#FF6B6B', lw=2)
ax1.text(0.4, 0.9, 'Single-Modal\nDistribution',
        ha='center', color='#FF6B6B')

# ========== TumorAL流程 ==========
# 流程箭头
ax2.annotate('', xy=(0.8, 0.5), xytext=(0.1, 0.5),
             arrowprops=dict(arrowstyle='->', lw=2, color='#4ECDC4'))

# EUL模块
x_multi = np.concatenate([np.linspace(-2, 0, 50), np.linspace(1, 3, 50)])
y_multi = np.exp(-(x_multi-1)**2) + np.exp(-(x_multi+1)**2)
ax2.plot(x_multi*0.1 + 0.4, y_multi*0.2 + 0.7,
        color='#4ECDC4', lw=2)
ax2.text(0.4, 0.9, 'Multi-Modal\nDistribution',
        ha='center', color='#4ECDC4')

# 多样性采样
ax2.scatter(np.random.uniform(0.6, 0.9, 30),
           np.random.uniform(0.1, 0.5, 30),
           s=50, c='#4ECDC4', alpha=0.6, edgecolors='white',
           marker='s')

# ========== t-SNE对比 ==========
# 生成模拟数据
np.random.seed(42)
X_traditional = np.random.multivariate_normal([0,0], [[1,0.9],[0.9,1]], 200)
X_tumoral = np.concatenate([
    np.random.multivariate_normal([2,2], [[1,-0.5],[-0.5,1]], 100),
    np.random.multivariate_normal([-2,3], [[1,0.2],[0.2,1]], 100)
])

# t-SNE可视化
tsne = TSNE(n_components=2, perplexity=30)
X_tsne = tsne.fit_transform(np.vstack([X_traditional, X_tumoral]))

ax3.scatter(X_tsne[:200,0], X_tsne[:200,1],
           c='#FF6B6B', alpha=0.6, label='Traditional')
ax3.scatter(X_tsne[200:,0], X_tsne[200:,1],
           c='#4ECDC4', alpha=0.6, marker='s', label='TumorAL')
ax3.set_title('Feature Space Distribution (t-SNE)', fontsize=10)
ax3.legend(loc='upper right')

# ========== 通用设置 ==========
for ax in [ax1, ax2]:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

# 添加标注
annotations = [
    (ax1, 0.15, 0.15, '#FF6B6B', '① Over-confidence\n   in single mode'),
    (ax1, 0.75, 0.2, '#FF6B6B', '② Feature clustering\n    causes redundancy'),
    (ax2, 0.15, 0.15, '#4ECDC4', '① Multi-modal reflects\n    epistemic uncertainty'),
    (ax2, 0.75, 0.2, '#4ECDC4', '② Max-margin sampling\n    ensures diversity')
]
for ax, x, y, color, text in annotations:
    ax.text(x, y, text, color=color, fontsize=8,
           bbox=dict(facecolor='white', alpha=0.8))

# 添加标题
fig.suptitle('Comparison of Active Learning Pipelines', y=0.95,
            fontsize=14, fontweight='bold')
fig.text(0.23, 0.85, 'Traditional Method', ha='center',
        color='#FF6B6B', fontsize=12)
fig.text(0.77, 0.85, 'TumorAL (Proposed)', ha='center',
        color='#4ECDC4', fontsize=12)

plt.tight_layout()
plt.savefig('Pipeline_Comparison.png', bbox_inches='tight', dpi=300)
plt.show()