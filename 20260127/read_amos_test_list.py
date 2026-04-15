import os

def extract_filenames_to_txt(source_folder, output_txt):
    """
    读取文件夹下的所有 .nii.gz 文件，去除后缀后保存到 txt 中。
    """
    # 存储处理后的文件名
    clean_names = []

    # 遍历文件夹
    try:
        files = os.listdir(source_folder)
    except FileNotFoundError:
        print(f"错误：找不到文件夹路径 '{source_folder}'")
        return

    for file in files:
        # 只处理以 .nii.gz 结尾的文件
        if file.endswith('.nii.gz'):
            # 使用 replace 去掉后缀，或者用切片 file[:-7]
            name_no_ext = file.replace('.nii.gz', '')
            clean_names.append(name_no_ext)

    # 排序：让文件名按顺序排列 (例如 amos_0001, amos_0002...)
    clean_names.sort()

    # 写入 txt 文件
    with open(output_txt, 'w', encoding='utf-8') as f:
        for name in clean_names:
            f.write(name + '\n')

    print(f"成功！共提取了 {len(clean_names)} 个文件名。")
    print(f"结果已保存至: {output_txt}")

# --- 配置区域 ---
# 请将下面的路径修改为你图片中 'amos' 文件夹的实际绝对路径
# 例如: '/home/user/data/amos' 或 'D:\\data\\amos'
folder_path = '/Users/wanghongyi/datasets/test_data_amos_flare/flare' 

# 输出 txt 的文件名
output_file = '/Users/wanghongyi/datasets/test_data_amos_flare/flare_dataset_list.txt'

# 执行函数
extract_filenames_to_txt(folder_path, output_file)