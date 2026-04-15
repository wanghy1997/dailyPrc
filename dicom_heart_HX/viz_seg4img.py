import os
import numpy as np
from PIL import Image

# ======================
# paths
# ======================
img_dir = "/Users/wanghongyi/datasets/test_imaging/test_imaging/guo_ning_qi_012Y_png/series0014-Body"
mask_dir = "/Users/wanghongyi/datasets/test_imaging/test_imaging/guo_ning_qi_012Y_segmentation/series0014-Body"
out_dir = "/Users/wanghongyi/datasets/test_imaging/test_imaging/guo_ning_qi_012Y_overlay"
os.makedirs(out_dir, exist_ok=True)

# ======================
# overlay settings
# ======================
alpha = 0.4   # 👈 覆盖透明度（0=不显示，1=完全覆盖）

# label → color（RGB）
COLOR_MAP = {
    1: (255, 0, 0),     # label 1 - red
    2: (0, 255, 0),     # label 2 - green
    3: (0, 0, 255),     # label 3 - blue
    4: (255, 255, 0),   # label 4 - yellow
    5: (255, 0, 255),   # label 5 - magenta
}

# ======================
# process
# ======================
for name in sorted(os.listdir(img_dir)):
    if not name.lower().endswith((".jpg", ".png")):
        continue

    img_path = os.path.join(img_dir, name)
    mask_path = os.path.join(mask_dir, name.replace(".jpg", ".png"))

    if not os.path.exists(mask_path):
        continue

    # load image
    img = Image.open(img_path).convert("RGB")
    img_np = np.array(img)

    # load mask
    mask = Image.open(mask_path)
    mask_np = np.array(mask)
    # normalize grayscale visualization masks if needed
    if mask_np.max() > 10:
        unique_vals = np.unique(mask_np)
        val_map = {v: i for i, v in enumerate(unique_vals) if v != 0}
        for v, i in val_map.items():
            mask_np[mask_np == v] = i

    # create color mask
    color_mask = np.zeros_like(img_np)
    for label, color in COLOR_MAP.items():
        color_mask[mask_np == label] = color

    # alpha blend
    overlay = img_np.copy()
    idx = mask_np > 0
    overlay[idx] = (
        (1 - alpha) * img_np[idx] + alpha * color_mask[idx]
    ).astype(np.uint8)

    # save
    out_img = Image.fromarray(overlay)

    out_name = os.path.splitext(name)[0] + ".png"  # always save as PNG to avoid compression
    out_path = os.path.join(out_dir, out_name)

    out_img.save(
        out_path,
        format="PNG",
        compress_level=0,   # no compression → preserve pixel fidelity
        optimize=False
    )

print("✅ Overlay images saved to:", out_dir)