import os
from pdf2image import convert_from_path

# ========== 参数设置 ==========
pdf_dir = "/Users/wanghongyi/Documents/a_6________写作/active_learning__1/IJBHI投稿相关文件--投稿中/W1__IJBHI_TumorAL/images/vis_BraTS_all_methods"     # PDF 文件所在文件夹
png_dir = "/Users/wanghongyi/Documents/a_6________写作/active_learning__1/IJBHI投稿相关文件--投稿中/W1__IJBHI_TumorAL/images/vis_BraTS_all_methods_png"  # 输出 PNG 文件夹
dpi = 600                           # 分辨率，300 已经很清晰，600 为超高清
fmt = "png"                         # 输出格式，可改为 'jpeg'、'tiff' 等
poppler_path = "/usr/local/bin"     # 若你是 Windows 用户且装了 Poppler，需要指定其 bin 路径

# ========== 主体逻辑 ==========
os.makedirs(png_dir, exist_ok=True)

for filename in os.listdir(pdf_dir):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(pdf_dir, filename)
        base_name = os.path.splitext(filename)[0]

        # 将 PDF 转换为图像（每页都会得到一个 Image 对象）
        images = convert_from_path(
            pdf_path,
            dpi=dpi,
            fmt=fmt,
            poppler_path=poppler_path if os.name == "nt" else None
        )

        # 保存每页为 PNG 文件
        for i, image in enumerate(images):
            output_path = os.path.join(png_dir, f"{base_name}_page_{i+1}.png")
            image.save(output_path, fmt.upper())
            print(f"✅ 已保存: {output_path}")

print("🎉 所有 PDF 已成功转换为 PNG！")