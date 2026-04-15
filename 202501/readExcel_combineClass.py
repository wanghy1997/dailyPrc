import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import to_rgba


def plot_category_accuracies(file_path):
    # 设置 matplotlib 字体为支持中文的字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 读取Excel文件
    excel_file = pd.ExcelFile(file_path)
    sheet_names = excel_file.sheet_names

    # 创建一个字典来存储每个医生在不同sheet中的各类别准确度 (accuracy)
    doctor_data = {sheet_name: {} for sheet_name in sheet_names}

    # 合并后的类别映射
    # merged_categories = {
    #     'Benign Lesions and Tissue': [0, 1, 2],
    #     'Non-Invasive Papillary Urothelial Carcinoma': [3, 5],
    #     'Invasive Papillary Urothelial Carcinoma': [4, 6]
    # }
    merged_categories = {
        'Benign Lesions and Tissue': [0, 1, 2],
        'Papillary Urothelial Carcinoma': [3, 4, 6, 5],
    }

    # 反向映射：将原类别映射到新类别
    category_map = {category: new_category for new_category, old_categories in merged_categories.items() for category in old_categories}

    # 用于存储每个医生在合并类别下的准确度和参与次数
    for sheet_name in sheet_names:
        # 读取工作表数据
        df = excel_file.parse(sheet_name)

        # 清理列名中的空格或特殊字符
        df.columns = df.columns.str.strip()

        # 提取倒数前6列（各级别医生的判读结果列）和第一列（真实病例的标签列）
        result_columns = df.columns[-6:]
        true_column = df.columns[0]

        # 对每个医生，针对每个类别计算准确率
        for col in result_columns:
            if col not in doctor_data[sheet_name]:
                doctor_data[sheet_name][col] = {new_category: {'accuracy': 0, 'count': 0} for new_category in merged_categories.keys()}

            # 按类别计算准确率
            for category in range(7):  # 原始类别 0 到 6
                new_category = category_map[category]
                # 统计该类别下的真实标签和预测标签的匹配情况
                category_true = (df[true_column] == category)
                category_pred = (df[col] == category)

                # 计算该类别的准确率
                accuracy = (category_true & category_pred).sum() / category_true.sum() if category_true.sum() > 0 else 0
                doctor_data[sheet_name][col][new_category]['accuracy'] += accuracy
                doctor_data[sheet_name][col][new_category]['count'] += 1  # 增加每个类别出现的次数

    # 打印每个医生在合并类别下的准确度
    print("\n每个医生在不同合并类别的准确度：")
    for sheet_name in sheet_names:
        print(f"\n医生在 {sheet_name} 中的准确度:")
        for doctor in doctor_data[sheet_name]:
            print(f"  医生 {doctor}:")
            for new_category in merged_categories.keys():
                # 计算每个医生的平均准确度
                accuracy = doctor_data[sheet_name][doctor][new_category]['accuracy'] / doctor_data[sheet_name][doctor][new_category]['count']
                print(f"    {new_category}: {accuracy:.4f}")

    # 设置图片清晰度
    plt.rcParams['figure.dpi'] = 300

    # 定义医生的颜色（为不同的sheet_name指定不同的颜色）
    sheet_colors = ['#8CCAFD', '#009FF6', '#EE8400']

    for i, new_category in enumerate(merged_categories.keys()):
        # 创建一个新的图形，仅包含当前的合并类别
        fig, ax = plt.subplots(figsize=(15, 10))

        for j, sheet_name in enumerate(sheet_names):
            # 计算每个医生的位置偏移量
            x_offset = np.arange(len(doctor_data[sheet_name])) + (j - 1) * 0.2

            # 获取每个医生在当前合并类别下的准确度
            accuracies = [
                doctor_data[sheet_name][doctor][new_category]['accuracy'] /
                doctor_data[sheet_name][doctor][new_category]['count']  # 计算平均准确度
                for doctor in doctor_data[sheet_name]
            ]

            # 获取当前sheet_name的颜色
            category_color = sheet_colors[j]

            # 绘制准确度的柱状图
            ax.bar(x_offset, accuracies, width=0.2, label=sheet_name, color=category_color, edgecolor='black')

        # 设置每个子图的标题和标签
        ax.set_title(f'')
        ax.set_xlabel('Doctors at all levels')
        ax.set_ylabel('Accuracy')
        ax.set_xticks(np.arange(len(doctor_data[sheet_names[0]])))
        ax.set_xticklabels(doctor_data[sheet_names[0]].keys())

        # 添加图例，统一放在左上角并保持在图形内
        ax.legend(loc='upper left', bbox_to_anchor=(0.0, 1.0))  # 在图的左上角，避免被挤出

        # 设置纵轴范围为 [0, 1]
        ax.set_ylim(0, 1)

        # 保存每个子图为一个单独的文件
        plt.tight_layout()
        output_file = f"F:\\文档\\a_6________写作\\turbt_论文\\总体判读对比_验证1-6_v2（论文图专用）\\Accuracy of {new_category}.png"
        plt.savefig(output_file)
        print(f"图形已保存为: {output_file}")

        # 清理当前图形，以便下一个子图的绘制
        plt.close(fig)


# 调用函数，传入Excel文件路径
file_path = 'F:\\文档\\a_6________写作\\turbt_论文\\总体判读对比_验证1-6_v2（论文图专用）.xlsx'
plot_category_accuracies(file_path)
