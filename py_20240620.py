import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.models as models
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Dataset
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image

# 定义自定义数据集
class MRIDataset(Dataset):
    def __init__(self, image_paths, labels, transform=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image = Image.open(self.image_paths[idx])
        label = self.labels[idx]
        if self.transform:
            image = self.transform(image)
        return image, label

# 图像预处理
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# 假设有3种MRI序列，每种序列包含3张2D切片
image_paths = [
    'path_to_mri_sequence1_slice1.jpg',
    'path_to_mri_sequence1_slice2.jpg',
    'path_to_mri_sequence1_slice3.jpg',
    'path_to_mri_sequence2_slice1.jpg',
    'path_to_mri_sequence2_slice2.jpg',
    'path_to_mri_sequence2_slice3.jpg',
    'path_to_mri_sequence3_slice1.jpg',
    'path_to_mri_sequence3_slice2.jpg',
    'path_to_mri_sequence3_slice3.jpg',
]
labels = [0, 0, 0, 1, 1, 1, 0, 0, 0]  # 假设标签

# 创建数据集和数据加载器
dataset = MRIDataset(image_paths, labels, transform)
dataloader = DataLoader(dataset, batch_size=1, shuffle=False)

# 加载预训练的ResNet-50模型
resnet50 = models.resnet50(pretrained=True)
resnet50 = nn.Sequential(*list(resnet50.children())[:-1])  # 移除最后的分类层
resnet50.eval()

# 定义融合模型
class FusionModel(nn.Module):
    def __init__(self):
        super(FusionModel, self).__init__()
        self.fc = nn.Linear(3 * 2048, 2)  # 3个ResNet-50特征，每个特征2048维

    def forward(self, x):
        return self.fc(x)

fusion_model = FusionModel()
fusion_model.eval()

# 提取特征并融合
def extract_features_and_fuse(dataloader):
    features = []
    labels = []

    for images, label in dataloader:
        images = images.squeeze()  # 移除batch维度
        sequences = images.view(3, 3, 224, 224)  # 3种序列，每种序列3张2D切片
        seq_features = []

        for seq in sequences:
            seq = seq.unsqueeze(0)  # 添加batch维度
            with torch.no_grad():
                feature = resnet50(seq).view(-1)  # 提取特征并展平
            seq_features.append(feature)

        fused_features = torch.cat(seq_features, dim=0)  # 特征融合
        features.append(fused_features)
        labels.append(label)

    return torch.stack(features), torch.tensor(labels)

features, labels = extract_features_and_fuse(dataloader)

# t-SNE分析
tsne = TSNE(n_components=2)
tsne_results = tsne.fit_transform(features)

plt.figure(figsize=(8, 8))
plt.scatter(tsne_results[:, 0], tsne_results[:, 1], c=labels, cmap='viridis')
plt.colorbar()
plt.title('t-SNE Analysis of MRI Features')
plt.show()

# Grad-CAM实现
class CAMResNet(nn.Module):
    def __init__(self):
        super(CAMResNet, self).__init__()
        self.resnet = resnet50
        self.fusion_fc = fusion_model.fc

    def forward(self, x):
        sequences = x.view(3, 3, 224, 224)
        seq_features = []

        for seq in sequences:
            seq = seq.unsqueeze(0)
            feature = self.resnet(seq).view(-1)
            seq_features.append(feature)

        fused_features = torch.cat(seq_features, dim=0)
        output = self.fusion_fc(fused_features.unsqueeze(0))
        return output, fused_features

cam_resnet = CAMResNet()
cam_resnet.eval()

def generate_cam(input_image, model, target_class=None):
    model.eval()
    sequences = input_image.view(3, 3, 224, 224)
    gradients = []

    def save_gradient(grad):
        gradients.append(grad)

    for seq in sequences:
        seq = seq.unsqueeze(0)
        seq.requires_grad = True
        feature = model.resnet(seq)
        feature.register_hook(save_gradient)

        output = model.fusion_fc(feature.view(1, -1))
        if target_class is None:
            target_class = output.argmax().item()

        model.zero_grad()
        output[0, target_class].backward()

        grad = gradients[0].cpu().data.numpy()
        feature = feature.cpu().data.numpy()

        weights = np.mean(grad, axis=(2, 3))[0, :]
        cam = np.zeros(feature.shape[2:], dtype=np.float32)

        for i, w in enumerate(weights):
            cam += w * feature[0, i, :, :]

        cam = np.maximum(cam, 0)
        cam = cam / cam.max()

        cam = cv2.resize(cam, (224, 224))
        heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
        heatmap = np.float32(heatmap) / 255
        overlay_img = heatmap + np.float32(input_image[0].permute(1, 2, 0).numpy())
        overlay_img = overlay_img / np.max(overlay_img)

        plt.imshow(overlay_img)
        plt.title('Grad-CAM')
        plt.axis('off')
        plt.show()

# 测试Grad-CAM
sample_image, _ = dataset[0]
generate_cam(sample_image, cam_resnet)
