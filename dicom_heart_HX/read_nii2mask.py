import SimpleITK as sitk
import numpy as np
import imageio
import os


nii_path = "/Users/wanghongyi/datasets/test_imaging/test_imaging/guo_ning_qi_012Y_segmentation/Segmentation.nii"
out_dir = "/Users/wanghongyi/datasets/test_imaging/test_imaging/guo_ning_qi_012Y_segmentation"

# ======================
# paths
# ======================
os.makedirs(out_dir, exist_ok=True)

# ======================
# load nifti
# ======================
img = sitk.ReadImage(nii_path)
arr = sitk.GetArrayFromImage(img)   # shape: (Z, H, W)

print("Segmentation shape:", arr.shape)
labels = np.unique(arr)
print("Unique labels:", labels)

# ======================
# build gray mapping
# ======================
# 去掉 background
fg_labels = labels[labels > 0]

if len(fg_labels) == 0:
    raise RuntimeError("No foreground labels found.")

# 把前景标签均匀映射到 128~255
gray_values = np.linspace(128, 255, len(fg_labels)).astype(np.uint8)
label_to_gray = {int(l): int(g) for l, g in zip(fg_labels, gray_values)}

print("Label → Gray mapping:", label_to_gray)

# ======================
# convert each slice
# ======================
for z in range(arr.shape[0]):
    mask = arr[z]

    # 初始化黑底
    vis = np.zeros_like(mask, dtype=np.uint8)

    for label, gray in label_to_gray.items():
        vis[mask == label] = gray

    out_path = os.path.join(out_dir, f"mask_gray_{z:03d}.png")
    imageio.imwrite(out_path, vis)

print("Saved gray PNGs to:", out_dir)