import os
from PIL import Image
import matplotlib.pyplot as plt

def crop_image(img_path, crop_box, square_size=512):
    img = Image.open(img_path)
    img_size = img.size
    print(img_size)
    cropped = img.crop(crop_box)
    # resize cropped image to square_size x square_size
    square = cropped.resize((square_size, square_size), Image.LANCZOS)
    return square


def concat_with_gap(images, gap=40, gap_color=(255, 255, 255), square_size=512):
    """横向拼接多张图片，在图片之间加入 gap。"""
    widths = [img.width for img in images]
    # heights = [img.height for img in images]

    total_width = sum(widths) + gap * (len(images) - 1)
    max_height = square_size

    new_img = Image.new("RGB", (total_width, max_height), gap_color)

    x = 0
    for img in images:
        new_img.paste(img, (x, 0))
        x += img.width + gap

    return new_img


def make_comparison_row(
    folder,
    case_id,
    type_suffix,
    crop_box,
    output_name,
    gap=40,
    square_size=512
):
    """
    folder: 图片目录
    case_id: e.g., '0039'
    type_suffix: 'A', 'C', 'S', ''   （此处你要'S'）
    crop_box: (x1, y1, x2, y2)
    output_name: 输出文件名
    gap: 图像之间的间隔像素
    """

    # 你要求的顺序（固定死，无需再排序）
    order = [
        f"label_{case_id}_{type_suffix}.png",
        f"dhc_{case_id}_{type_suffix}.png",
        f"diffusion_{case_id}_{type_suffix}.png",
        f"ours1_{case_id}_{type_suffix}.png",
    ]

    # 裁剪后的图像列表
    imgs = []
    for fname in order:
        path = os.path.join(folder, fname)
        if not os.path.exists(path):
            raise FileNotFoundError(f"找不到图片: {path}")
        imgs.append(crop_image(path, crop_box, square_size=square_size))

    # 拼接
    result = concat_with_gap(imgs, gap=gap, square_size=square_size)

    # ★★★★★ 保存结果 ★★★★★
    # save_path = os.path.join(folder, output_name)
    # result.save(save_path)
    # print("已保存:", save_path)

    # ★★★★★ 直接显示 ★★★★★
    plt.figure(figsize=(12, 3))
    plt.imshow(result)
    plt.axis('off')
    plt.gca().set_position([0, 0, 1, 1])  # 让图片撑满画布
    plt.show()

    return result  # 如果你想之后再保存或继续处理，可以返回


# =============================== #
#           使用示例              #
# =============================== #
if __name__ == '__main__':

    folder = "/Users/wanghongyi/Experiment/SSL_result/Synapse/itk"
    case_id = "0039"

    # 你需要手动量一个裁剪框（随便哪张图上量一次即可）
    crop_box = (150, 160, 540, 434)

    # 只做 S 类型（按你给的需求）
    make_comparison_row(
        folder=folder,
        case_id=case_id,
        type_suffix="A",
        crop_box=crop_box,
        output_name="compare_0039_S.png",
        gap=50,   # 白色间隔（论文推荐 30~60）
        square_size=512,
    )