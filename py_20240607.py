import numpy as np
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# 生成100个3D数据样例
np.random.seed(42)
data = np.random.randn(100, 3)

# 使用K-means聚类，假设聚类数为10
kmeans = KMeans(n_clusters=10, random_state=42)
labels = kmeans.fit_predict(data)
cluster_centers = kmeans.cluster_centers_

# 将数据和簇中心点合并
data_with_centers = np.vstack([data, cluster_centers])
print(data_with_centers.__sizeof__())
# 使用t-SNE降维到2D
tsne = TSNE(n_components=2, random_state=42)
data_2d = tsne.fit_transform(data_with_centers)

# 分离降维后的数据点和簇中心点
data_points_2d = data_2d[:100]
cluster_centers_2d = data_2d[100:]

# 创建颜色映射
colors = plt.cm.get_cmap("tab10", 10)

# 可视化结果，带有簇标签的颜色
plt.figure(figsize=(10, 8))
for i in range(10):
    indices = labels == i
    plt.scatter(data_points_2d[indices, 0], data_points_2d[indices, 1], s=100, color=colors(i), label=f'Cluster {i}')

# 绘制簇中心
plt.scatter(cluster_centers_2d[:, 0], cluster_centers_2d[:, 1], s=300, c='black', marker='X', label='Cluster Centers')
plt.title("t-SNE Visualization of 100 3D Data Samples with K-means Clustering")
plt.xlabel("t-SNE Dimension 1")
plt.ylabel("t-SNE Dimension 2")
plt.legend()
plt.show()
