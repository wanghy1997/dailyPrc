import os
import glob


def delete_files_with_extension(directory, extension):
    # 构建匹配模式
    pattern = os.path.join(directory, f'*.{extension}')

    # 获取匹配的文件列表
    files_to_delete = glob.glob(pattern)

    # 删除文件
    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            print(f"文件 {file_path} 已删除。")
        except Exception as e:
            print(f"删除文件 {file_path} 时发生错误：{e}")


# 指定目录和文件后缀
directory_path = 'I:/多粒度-相册/101ONLY_'
file_extension = 'NEF'

# 调用函数删除指定后缀的文件
delete_files_with_extension(directory_path, file_extension)
