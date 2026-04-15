import os
import json
import nibabel as nib
import numpy as np
import torch
from tqdm import tqdm


def load_and_merge_modalities(image_paths, label_path):
    # 加载并合并所有模态
    images = []
    for path in image_paths:
        img = nib.load(path)
        img_data = img.get_fdata()
        images.append(img_data)

    # 将四种模态堆叠成一个多通道的numpy数组
    merged_image = np.stack(images, axis=0)

    # 转换为 PyTorch 张量
    merged_image_tensor = torch.tensor(merged_image, dtype=torch.float32)

    # 加载标签
    label_img = nib.load(label_path)
    label_data = label_img.get_fdata()
    label_tensor = torch.tensor(label_data, dtype=torch.float32)

    return merged_image_tensor, label_tensor


def process_json(input_json_path, output_json_path, data_root):
    if not os.path.exists(input_json_path):
        raise FileNotFoundError(f"Input JSON file not found: {input_json_path}")

    with open(input_json_path, 'r') as f:
        original_data = json.load(f)

    # 创建新的数据结构，保留原有数据
    new_data = {
        "data_root": original_data["data_root"],
        "training": original_data["training"],
        "unlabeled": original_data["unlabeled"],
        "samplepool": [],
        "val": [],
        "all_num": original_data["all_num"],
        "training_num": original_data["training_num"],
        "unlabeled_num": original_data["unlabeled_num"],
        "samplepool_num": original_data["samplepool_num"],
        "val_num": original_data["val_num"],
    }

    for sample in tqdm(original_data["samplepool"], desc="Processing samples"):
        image_paths = [os.path.join(data_root, path) for path in sample["image"]]
        label_path = os.path.join(data_root, sample["label"])
        patient_id = sample["image"][0].split('/')[-2]

        merged_image_tensor, label_tensor = load_and_merge_modalities(image_paths, label_path)

        # 保存合并后的图像和标签
        merged_image_path = f"BraTS2021_{patient_id}.nii.gz"
        merged_label_path = f"BraTS2021_{patient_id}_label.nii.gz"
        output_image_path = os.path.join(data_root, "BraTS2021", patient_id, merged_image_path)
        output_label_path = os.path.join(data_root, "BraTS2021", patient_id, merged_label_path)

        # os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
        # nib.save(nib.Nifti1Image(merged_image_tensor.numpy(), np.eye(4)), output_image_path)
        # nib.save(nib.Nifti1Image(label_tensor.numpy(), np.eye(4)), output_label_path)

        # 更新新的 JSON 数据结构
        new_sample = {
            "image": os.path.join("BraTS2021", patient_id, merged_image_path),
            "label": os.path.join("BraTS2021", patient_id, merged_label_path),
            "Pseudo_label": ""
        }
        new_data["samplepool"].append(new_sample)

    # 将新的samplepool数据插入到原始数据的副本中
    updated_data = original_data.copy()
    updated_data["samplepool"] = new_data["samplepool"]

    with open(output_json_path, 'w') as f:
        json.dump(updated_data, f, indent=4)
    with open(output_json_path, 'r') as f:
        original_data = json.load(f)
    for sample in tqdm(original_data["val"], desc="Processing val"):
        image_paths = [os.path.join(data_root, path) for path in sample["image"]]
        label_path = os.path.join(data_root, sample["label"])
        patient_id = sample["image"][0].split('/')[-2]

        merged_image_tensor, label_tensor = load_and_merge_modalities(image_paths, label_path)

        # 保存合并后的图像和标签
        merged_image_path = f"BraTS2021_{patient_id}.nii.gz"
        merged_label_path = f"BraTS2021_{patient_id}_label.nii.gz"
        output_image_path = os.path.join(data_root, "BraTS2021", patient_id, merged_image_path)
        output_label_path = os.path.join(data_root, "BraTS2021", patient_id, merged_label_path)

        # os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
        # nib.save(nib.Nifti1Image(merged_image_tensor.numpy(), np.eye(4)), output_image_path)
        # nib.save(nib.Nifti1Image(label_tensor.numpy(), np.eye(4)), output_label_path)

        # 更新新的 JSON 数据结构
        new_sample = {
            "image": os.path.join("BraTS2021", patient_id, merged_image_path),
            "label": os.path.join("BraTS2021", patient_id, merged_label_path),
            "Pseudo_label": ""
        }
        new_data["val"].append(new_sample)

    # 将新的samplepool数据插入到原始数据的副本中
    updated_data = original_data.copy()
    updated_data["val"] = new_data["val"]

    with open(output_json_path, 'w') as f:
        json.dump(updated_data, f, indent=4)

if __name__ == '__main__':
    # 示例使用
    input_json_path = r'G:\data\why\seg_result\active_L\initPool_BraTS2021_.json'  # 替换为实际输入 JSON 文件路径
    output_json_path = r'G:\data\why\seg_result\active_L\initPool_BraTS2021.json'  # 替换为实际输出 JSON 文件路径
    data_root = r'G:\Datasets\Seg3D_MRI'  # 替换为实际数据根目录

    process_json(input_json_path, output_json_path, data_root)
