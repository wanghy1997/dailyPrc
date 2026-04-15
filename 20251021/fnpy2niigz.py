import os
import numpy as np
import nibabel as nib


def restore_label_npy_to_nii(img_id, pred_path, label_npy_path, save_path):
    """
    参数：
    - img_id：样本 ID（如 'amos_0001'）
    - pred_path：预测的 nii.gz 路径（我们用它的 affine）
    - label_npy_path：npy 标签路径
    - save_path：保存生成 nii.gz 的路径
    """
    save_dir = '/Users/wanghongyi/datasets/SSL_dataprocess'
    # 加载标签并确保为整数类型（颜色匹配）
    label = np.load(label_npy_path).astype(np.uint8)

    # 读取已有的预测 nii.gz 文件，获取 affine 信息
    ref_nii = nib.load(pred_path)
    affine = ref_nii.affine

    # 构建新的 NIfTI 图像
    label_nii = nib.Nifti1Image(label, affine)
    nib.save(label_nii, os.path.join(save_path, f'{img_id}_label_restored.nii.gz'))


import os
import numpy as np
import nibabel as nib
from tqdm import tqdm


def convert_npy_label_to_nii(
        npy_dir,  # 存放 label_npy 的文件夹
        pred_nii_dir,  # 存放预测结果 nii 的文件夹（参考方向）
        output_dir,  # 保存输出的 label_nii 的文件夹
        suffix="_label.npy"  # label 文件名的后缀，用于识别
):
    os.makedirs(output_dir, exist_ok=True)

    npy_files = ['/Users/wanghongyi/datasets/SSL_dataprocess/amos_0056_label.npy']

    for file in tqdm(npy_files):
        img_id = '0056'  # 如 'amos_0008'
        label_npy_path = os.path.join(npy_dir, file)
        pred_nii_path = pred_nii_dir
        output_nii_path = os.path.join(output_dir, f"{img_id}_label_restored.nii.gz")

        if not os.path.exists(pred_nii_path):
            print(f"[!] Warning: {pred_nii_path} not found. Skipping.")
            continue

        # ---------- 1. 读取标签（npy） ----------
        label = np.load(label_npy_path)
        label = label.astype(np.uint8)  # 保证标签为整型，用于可视化颜色正确

        # ---------- 2. 读取参考预测 nii ----------
        pred_nii = nib.load(pred_nii_path)
        affine = pred_nii.affine
        header = pred_nii.header

        # ---------- 3. 尺寸检查（可选） ----------
        if label.shape != pred_nii.shape:
            print(f"[!] Size mismatch for {img_id}: label {label.shape}, pred {pred_nii.shape}")

        # ---------- 4. 构造并保存 label NIfTI ----------
        label_nii = nib.Nifti1Image(label, affine, header)
        nib.save(label_nii, output_nii_path)

        print(f"[✓] Saved: {output_nii_path}")


def red_color():
    import nibabel as nib
    import numpy as np

    # 预测标签
    pred = nib.load("/Users/wanghongyi/datasets/SSL_dataprocess/ours_amos_0056.nii.gz").get_fdata()
    pred_values = np.unique(pred)

    # 原始 label（如来自 npy）
    label = nib.load("/Users/wanghongyi/datasets/SSL_dataprocess/0056_label_restored.nii.gz").get_fdata()
    label_values = np.unique(label)

    print("Prediction values:", pred_values)
    print("Label values:", label_values)


def red_color_slicer():
    import slicer
    # 获取预测和标签的 segmentation node
    predNode = slicer.util.getNode('/Users/wanghongyi/datasets/SSL_dataprocess/ours_amos_0056.nii.gz')  # 改成你真实名称
    labelNode = slicer.util.getNode('/Users/wanghongyi/datasets/SSL_dataprocess/0056_label_restored.nii.gz')  # 你的 label segmentation 名称

    # 遍历 prediction 中所有 segment，读取颜色
    predSeg = predNode.GetSegmentation()
    labelSeg = labelNode.GetSegmentation()

    for i in range(predSeg.GetNumberOfSegments()):
        segmentID = predSeg.GetNthSegmentID(i)
        if labelSeg.GetSegment(segmentID):
            color = predSeg.GetSegment(segmentID).GetColor()
            labelSeg.GetSegment(segmentID).SetColor(color)
            print(f"Copied color {np.round(np.array(color) * 255)} to segment {segmentID}")

# if __name__ == '__main__':
#     restore_label_npy_to_nii(img_id='0056', pred_path='/Users/wanghongyi/datasets/SSL_dataprocess/ours_amos_0056.nii.gz', label_npy_path='/Users/wanghongyi/datasets/SSL_dataprocess/amos_0056_label.npy', save_path='/Users/wanghongyi/datasets/SSL_dataprocess')
#
if __name__ == "__main__":
    # convert_npy_label_to_nii(
    #     npy_dir="/Users/wanghongyi/datasets/SSL_dataprocess/amos_0056_label.npy",
    #     pred_nii_dir="/Users/wanghongyi/datasets/SSL_dataprocess/ours_amos_0056.nii.gz",
    #     output_dir="/Users/wanghongyi/datasets/SSL_dataprocess"
    # )
    red_color_slicer()