"""
每个医生+每个类别的精度
"""
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

    # 类别列表
    categories = [0, 1, 2, 3, 4, 5, 6]

    for sheet_name in sheet_names:
        # 读取工作表数据
        df = excel_file.parse(sheet_name)

        # 提取倒数前6列（各级别医生的判读结果列）和第一列（真实病例的标签列）
        result_columns = df.columns[-6:]
        true_column = df.columns[0]

        # 对每个医生，针对每个类别计算准确率
        for col in result_columns:
            if col not in doctor_data[sheet_name]:
                doctor_data[sheet_name][col] = {category: {'accuracy': 0} for category in categories}

            # 按类别计算准确率
            for category in categories:
                # 统计该类别下的真实标签和预测标签的匹配情况
                category_true = (df[true_column] == category)
                category_pred = (df[col] == category)

                # 计算该类别的准确率
                accuracy = (category_true & category_pred).sum() / category_true.sum() if category_true.sum() > 0 else 0
                doctor_data[sheet_name][col][category]['accuracy'] = accuracy

    # 打印每个医生在每个类别的准确度
    print("\n每个医生在不同类别的准确度：")
    for sheet_name in sheet_names:
        print(f"\n医生在 {sheet_name} 中的准确度:")
        for doctor in doctor_data[sheet_name]:
            print(f"  医生 {doctor}:")
            for category in categories:
                accuracy = doctor_data[sheet_name][doctor][category]['accuracy']
                print(f"    类别 {category}: {accuracy:.4f}")

    # 设置图片清晰度
    plt.rcParams['figure.dpi'] = 300

    # 创建子图：7个子图分别表示7个类别
    fig, axes = plt.subplots(7, 1, figsize=(15, 20))
    fig.subplots_adjust(hspace=0.5)  # 调整子图间距

    # 定义医生的颜色（为不同的sheet_name指定不同的颜色）
    sheet_colors = ['blue', 'green', 'orange']

    for i, category in enumerate(categories):
        ax = axes[i]  # 获取第i个子图

        for j, sheet_name in enumerate(sheet_names):
            # 计算每个医生的位置偏移量
            x_offset = np.arange(len(doctor_data[sheet_name])) + (j - 1) * 0.2

            # 获取每个医生在当前类别下的准确度
            accuracies = [doctor_data[sheet_name][doctor][category]['accuracy'] for doctor in doctor_data[sheet_name]]

            # 获取当前sheet_name的颜色
            category_color = sheet_colors[j]

            # 绘制准确度的柱状图
            ax.bar(x_offset, accuracies, width=0.2, label=f'{sheet_name} 类别 {category}', color=category_color,
                   edgecolor='black')

        # 设置每个子图的标题和标签
        ax.set_title(f'类别 {category} 的准确度 (Accuracy)')
        ax.set_xlabel('各级别医生')
        ax.set_ylabel('Accuracy')
        ax.set_xticks(np.arange(len(doctor_data[sheet_names[0]])))
        ax.set_xticklabels(doctor_data[sheet_names[0]].keys())
        ax.legend()

    # 显示图表
    plt.tight_layout()
    plt.show()


# 调用函数，传入Excel文件路径
file_path = 'F:\\文档\\a_6________写作\\turbt_论文\\总体判读对比_验证1-6_v2.xlsx'
plot_category_accuracies(file_path)

