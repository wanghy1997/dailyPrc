import torch
from torch import nn
from PIL import Image
import matplotlib.pyplot as plt
from torchvision import transforms
from torchvision.models import resnet50
from captum.attr import LayerIntegratedGradients, visualization

# 加载预训练的ResNet模型
model = resnet50(pretrained=True)
model.eval()

# 加载图像并进行预处理
def preprocess_image(image_path):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    image = Image.open(image_path).convert("RGB")
    input_image = transform(image).unsqueeze(0)
    return input_image

# 显示原始图像
def show_original_image(image_path):
    image = Image.open(image_path).convert("RGB")
    plt.imshow(image)
    plt.title('Original Image')
    plt.show()

# 定义带有注意力机制的ResNet模型
class ResNetWithAttention(nn.Module):
    def __init__(self, base_model):
        super(ResNetWithAttention, self).__init__()
        self.base_model = nn.Sequential(*list(base_model.children())[:-2])
        self.attention_layer = nn.MultiheadAttention(embed_dim=2048, num_heads=1)

    def forward(self, x):
        x = self.base_model(x)  # 1 2048 7 7
        x = x.flatten(2).permute(2, 0, 1)  # 49 1 2048
        attn_output, _ = self.attention_layer(x, x, x)
        attn_output = attn_output.permute(1, 2, 0).view(1, 2048, 7, 7)
        return attn_output

# 创建带有注意力机制的ResNet模型
resnet_with_attention = ResNetWithAttention(model)

# 加载图像
# 输入图像路径
image_path = "D://图片//壁纸//微信图片_20230813153508.png"

input_image = preprocess_image(image_path)

# 生成注意力图
attr_layer = LayerIntegratedGradients(resnet_with_attention, resnet_with_attention.base_model[0])
attribution = attr_layer.attribute(input_image, target=0)

# 可视化注意力图
show_original_image(image_path)
visualization.visualize_image_attr_multiple(attribution[0].numpy(), original_image=input_image[0].numpy(), methods=["original_image"], signs=['all'], titles=["Attribution Map"])
plt.show()