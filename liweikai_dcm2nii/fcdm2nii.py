# -*- coding: utf-8 -*-
import shutil
import re
import os
import subprocess


# 1️⃣ 根目录（包含 S1~S8）
root_dir = "/Users/wanghongyi/datasets/tangfuyuan"

# 2️⃣ nii 输出目录
nii_out_dir = '/Users/wanghongyi/datasets/tangfuyuan_nii'
os.makedirs(nii_out_dir, exist_ok=True)

# 3️⃣ 遍历 S1 ~ S8
for i in range(1, 9):
    s_dir = os.path.join(root_dir, f"S{i}")
    if not os.path.isdir(s_dir):
        print(f"⚠️ 跳过：{s_dir} 不存在")
        continue

    out_prefix = f"S{i}"

    cmd = [
        "/Users/wanghongyi/codes/dcm2niix",
        "-z", "y",          # 压缩成 .nii.gz（推荐）
        "-f", out_prefix,   # 输出文件名
        "-o", nii_out_dir,  # 输出目录
        s_dir               # 输入 dcm 目录
    ]

    print("🚀 执行:", " ".join(cmd))
    subprocess.run(cmd, check=True)

print("✅ S1~S8 已全部转换为 NIfTI")