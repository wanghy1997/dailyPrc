import os
import numpy as np
import cv2
from tqdm import tqdm


def npy_mask_to_rgb(input_dir, output_dir, colormap=None):
    """
    将npy格式的mask转换为可视化RGB图像
    参数：
        input_dir: 包含.npy文件的输入目录
        output_dir: 输出RGB图像的保存目录
        colormap: 自定义颜色映射表，格式为 {类别id: (R,G,B)}
    """
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 默认PASCAL VOC调色板（21类）
    default_colormap = [
        (0, 0, 0),  # background
        (128, 0, 0),  # aeroplane
        (0, 128, 0),  # bicycle
        (128, 128, 0),  # bird
        (0, 0, 128),  # boat
        (128, 0, 128),  # bottle
        (0, 128, 128),  # bus
        (128, 128, 128),  # car
        (64, 0, 0),  # cat
        (192, 0, 0),  # chair
        (64, 128, 0),  # cow
        (192, 128, 0),  # dining table
        (64, 0, 128),  # dog
        (192, 0, 128),  # horse
        (64, 128, 128),  # motorbike
        (192, 128, 128),  # person
        (0, 64, 0),  # potted plant
        (128, 64, 0),  # sheep
        (0, 192, 0),  # sofa
        (128, 192, 0),  # train
        (0, 64, 128)  # tv/monitor
    ]

    # 使用自定义或默认颜色映射
    if colormap is None:
        colormap = default_colormap
    else:
        # 确保颜色值在0-255范围
        colormap = {k: tuple(int(c) for c in v) for k, v in colormap.items()}

    # 获取所有npy文件
    npy_files = [f for f in os.listdir(input_dir) if f.endswith('.npy')]

    for filename in tqdm(npy_files, desc='Processing masks'):
        # 加载npy文件
        mask_path = os.path.join(input_dir, filename)
        mask = np.load(mask_path)

        # 验证mask维度
        if mask.ndim != 2:
            raise ValueError(f"Mask {filename} 应为二维数组，实际维度为 {mask.ndim}")

        # 初始化RGB图像
        h, w = mask.shape
        rgb_image = np.zeros((h, w, 3), dtype=np.uint8)

        # 应用颜色映射
        if isinstance(colormap, list):
            # 列表式颜色映射（索引访问）
            for class_id, color in enumerate(colormap):
                rgb_image[mask == class_id] = color
        elif isinstance(colormap, dict):
            # 字典式颜色映射（非连续类别）
            for class_id, color in colormap.items():
                rgb_image[mask == class_id] = color
        else:
            raise TypeError("colormap应为列表或字典类型")

        # 处理未定义类别（黑色填充）
        undefined_mask = ~np.isin(mask, list(colormap.keys()) if isinstance(colormap, dict) else range(len(colormap)))
        rgb_image[undefined_mask] = (0, 0, 0)

        # 保存图像
        output_path = os.path.join(output_dir, filename.replace('.npy', '.png'))
        cv2.imwrite(output_path, cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR))


if __name__ == '__main__':
    # 使用示例
    input_directory = '/Users/wanghongyi/Experiment/ADA_MMWHS/mask/mask'
    output_directory = '/Users/wanghongyi/Experiment/ADA_MMWHS/mask/rgb'

    # 可选自定义颜色映射（示例）
    custom_colormap = {
        0: (255, 0, 0),  # 类别0 -> 红色
        1: (0, 255, 0),  # 类别1 -> 绿色
        2: (0, 0, 255)  # 类别2 -> 蓝色
    }

    npy_mask_to_rgb(
        input_dir=input_directory,
        output_dir=output_directory,
        colormap=custom_colormap  # 使用None则默认PASCAL调色板
    )