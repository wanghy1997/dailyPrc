import os
import pydicom
import numpy as np
import cv2
import imageio
import imageio.v2 as imageio_v2


def read_dicom_info(dcm_path):
    ds = pydicom.dcmread(dcm_path)

    print("=" * 80)
    print("File:", dcm_path)

    # --- 基本身份信息 ---
    print("Modality:", getattr(ds, "Modality", "N/A"))
    print("SOPClassUID:", getattr(ds, "SOPClassUID", "N/A"))
    print("SeriesDescription:", getattr(ds, "SeriesDescription", "N/A"))
    print("ImageType:", getattr(ds, "ImageType", "N/A"))
    print("Manufacturer:", getattr(ds, "Manufacturer", "N/A"))

    # --- 是否多帧 ---
    print("NumberOfFrames:", getattr(ds, "NumberOfFrames", 1))

    # --- 是否派生数据 ---
    print("DerivationDescription:", getattr(ds, "DerivationDescription", "N/A"))

    # --- 是否 SEG ---
    print("Has SegmentSequence:", hasattr(ds, "SegmentSequence"))

    # --- 像素检查 ---
    if hasattr(ds, "PixelData"):
        arr = ds.pixel_array
        print("Pixel shape:", arr.shape)
        print("Pixel dtype:", arr.dtype)
        uniq = np.unique(arr)
        print("Unique values (first 20):", uniq[:20])
        print("Unique value count:", len(uniq))
    else:
        print("No PixelData")

    print("=" * 80)


def viz_dicom(dcm_path):
    import pydicom
    import matplotlib.pyplot as plt

    ds = pydicom.dcmread(dcm_path)
    img = ds.pixel_array  # (H, W, 3)

    plt.figure(figsize=(5, 5))
    plt.imshow(img)
    plt.axis("off")
    plt.title("Secondary Capture RGB")
    plt.show()


# -------------------------------
# 工具 1：读取一个 series 目录中的所有 DICOM
# -------------------------------
def load_dicom_series(series_dir):
    """
    读取一个 series 目录下的所有 DICOM 文件
    返回：
        dcm_files: 排序后的 dcm 文件路径列表
        images:    对应的像素数组列表 [(H,W), ...]
    """
    dcm_files = sorted([
        os.path.join(series_dir, f)
        for f in os.listdir(series_dir)
        if f.lower().endswith(".dcm")
    ])

    images = []
    for f in dcm_files:
        ds = pydicom.dcmread(f)
        images.append(ds.pixel_array)

    return dcm_files, images


# -------------------------------
# 工具 2：将 uint16 / 原始灰度映射到 uint8（适合可视化）
# -------------------------------
def normalize_to_uint8(img, p_low=1, p_high=99):
    """
    对单张图像做稳健归一化（percentile）
    """
    img = img.astype(np.float32)
    lo, hi = np.percentile(img, (p_low, p_high))
    img = np.clip(img, lo, hi)
    img = (img - lo) / (hi - lo + 1e-6)
    img = (img * 255).astype(np.uint8)
    return img


# -------------------------------
# 工具 3：保存 PNG（文件名与 DICOM 对齐）
# -------------------------------
def save_png_series(
    dcm_files,
    images,
    out_img_dir,
    ext=".jpg",          # ".jpg" or ".png"
    start_idx=0,
    zero_pad=5           # 00000.jpg
):
    """
    将一组 DICOM 图像保存为连续编号的 PNG/JPG
    """
    os.makedirs(out_img_dir, exist_ok=True)

    png_images = []

    # 为了时间序列一致性，统一用整个 series 的统计量
    stack = np.stack(images, axis=0)
    p1, p99 = np.percentile(stack, (1, 99))

    for i, img in enumerate(images):
        img_u8 = img.astype(np.float32)
        img_u8 = np.clip(img_u8, p1, p99)
        img_u8 = (img_u8 - p1) / (p99 - p1 + 1e-6)
        img_u8 = (img_u8 * 255).astype(np.uint8)

        frame_id = start_idx + i
        name = str(frame_id).zfill(zero_pad)
        out_path = os.path.join(out_img_dir, name + ext)

        if ext.lower() == ".jpg":
            cv2.imwrite(out_path, img_u8, [cv2.IMWRITE_JPEG_QUALITY, 95])
        else:
            cv2.imwrite(out_path, img_u8)

        png_images.append(img_u8)

    return png_images


# -------------------------------
# 工具 4：根据 PNG 序列生成 GIF
# -------------------------------
def save_gif_from_images(images, gif_path, fps=10):
    """
    根据图像序列生成 GIF
    imageio 新版本已弃用 fps，需使用 duration（ms）
    """
    duration = int(1000 / fps)
    imageio.mimsave(gif_path, images, duration=duration)


# -------------------------------
# 工具 5：根据 PNG 序列生成 MP4
# -------------------------------
def save_mp4_from_images(images, mp4_path, fps=10):
    """
    根据图像序列生成 MP4 视频
    """
    writer = imageio_v2.get_writer(
        mp4_path,
        fps=fps,
        codec="libx264",
        quality=8,
        pixelformat="yuv420p"
    )
    for img in images:
        writer.append_data(img)
    writer.close()


# -------------------------------
# 总控函数：series → PNG + GIF
# -------------------------------
def convert_series_to_png_and_gif(
    series_dir,
    out_png_dir,
    out_gif_path,
    out_mp4_path=None,
    fps=10
):
    """
    核心入口函数
    """
    print(f"[INFO] Reading series: {series_dir}")
    dcm_files, images = load_dicom_series(series_dir)

    print(f"[INFO] {len(dcm_files)} DICOM files found")

    print(f"[INFO] Saving PNGs to: {out_png_dir}")
    png_images = save_png_series(dcm_files, images, out_png_dir)

    print(f"[INFO] Creating GIF: {out_gif_path}")
    save_gif_from_images(png_images, out_gif_path, fps=fps)

    print(f"[INFO] Creating MP4: {out_mp4_path}")
    save_mp4_from_images(png_images, out_mp4_path, fps=fps)

    print("[DONE] Series converted successfully")


def is_secondary_capture_series(series_dir):
    """
    判断一个 series 是否是 Secondary Capture（只读一个文件就够）
    """
    for f in os.listdir(series_dir):
        if not f.lower().endswith(".dcm"):
            continue
        try:
            ds = pydicom.dcmread(
                os.path.join(series_dir, f),
                stop_before_pixels=True
            )
            uid = str(getattr(ds, "SOPClassUID", ""))
            desc = str(getattr(ds, "SeriesDescription", ""))
            if uid.startswith("1.2.840.10008.5.1.4.1.1.7") \
               or "SecondaryCapture" in desc \
               or "Workspace" in desc:
                return True
            return False
        except Exception:
            continue
    return True


def convert_patient_all_series(
    patient_dir,
    out_patient_png_dir,
    fps=12
):
    """
    对一个患者目录下的所有 series 批量转 PNG + GIF
    """
    os.makedirs(out_patient_png_dir, exist_ok=True)

    for series_name in sorted(os.listdir(patient_dir)):
        series_dir = os.path.join(patient_dir, series_name)

        if not os.path.isdir(series_dir):
            continue

        print("\n" + "=" * 80)
        print(f"[PATIENT] Processing series: {series_name}")

        # 跳过 Secondary Capture
        if is_secondary_capture_series(series_dir):
            print("[SKIP] Secondary Capture or unsupported series")
            continue

        out_png_dir = os.path.join(out_patient_png_dir, series_name)
        out_gif_path = os.path.join(
            out_patient_png_dir,
            f"{series_name}_cine.gif"
        )
        out_mp4_path = os.path.join(
            out_patient_png_dir,
            f"{series_name}_cine.mp4"
        )
        print(f"[INFO] Output PNG dir: {out_png_dir}")
        print(f"[INFO] Output GIF path: {out_gif_path}")
        print(f"[INFO] Output MP4 path: {out_mp4_path}")
        try:
            convert_series_to_png_and_gif(
                series_dir=series_dir,
                out_png_dir=out_png_dir,
                out_gif_path=out_gif_path,
                out_mp4_path=out_mp4_path,
                fps=fps
            )
        except Exception as e:
            print(f"[ERROR] Failed on series {series_name}: {e}")


if __name__ == "__main__":

    # dcm_path = '/Users/wanghongyi/Desktop/test imaging/test imaging/yang_xian_min_012Y/series10058-unknown/img0001-unknown.dcm'
    # dcm_path = '/Users/wanghongyi/Desktop/test imaging/test imaging/guo_ning_qi_012Y/series0007-Body/img0002-26.5462.dcm'
    # read_dicom_info(dcm_path)  # 读取 dcm 文件的基本信息
    # viz_dicom(dcm_path)  # 可视化 RGB 图像

    """批量转换某患者所有 series"""
    # patient_dir = "/Users/wanghongyi/Desktop/test imaging/test imaging/guo_ning_qi_012Y"  # guo_ning_qi_012Y
    # out_patient_png_dir = "/Users/wanghongyi/Desktop/test imaging/test imaging/guo_ning_qi_012Y_png"  

    patient_dir = '/Users/wanghongyi/datasets/test_imaging/test_imaging/guo_ning_qi_012Y'  # yang_xian_min_012Y
    out_patient_png_dir = "/Users/wanghongyi/datasets/test_imaging/test_imaging/guo_ning_qi_012Y_transfer"  

    convert_patient_all_series(
        patient_dir=patient_dir,
        out_patient_png_dir=out_patient_png_dir,
        fps=12
    )
