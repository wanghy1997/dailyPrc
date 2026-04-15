import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from keras.models import load_model

# 假设你有一个预训练的3D CNN模型
model = load_model('path_to_pretrained_model.h5')

# 加载数据
num_samples = 10
num_channels = 4
height = 224
width = 224
depth = 144
data = np.random.rand(num_samples, num_channels, height, width, depth)

# 使用模型提取特征
features = model.predict(data)

# 使用t-SNE进行降维
tsne = TSNE(n_components=2, random_state=42)
data_tsne = tsne.fit_transform(features)
print(data_tsne)
# # 可视化
# plt.figure(figsize=(8, 6))
# plt.scatter(data_tsne[:, 0], data_tsne[:, 1])
# plt.title("t-SNE on Extracted Features from 3D CNN")
# plt.xlabel("t-SNE feature 1")
# plt.ylabel("t-SNE feature 2")
# plt.show()
