"""
全部医生在不同阶段的判读准确率
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgba

def plot_correct_counts(file_path):
    # 设置 matplotlib 字体为 Times New Roman
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['axes.unicode_minus'] = False

    # 读取Excel文件
    excel_file = pd.ExcelFile(file_path)
    sheet_names = excel_file.sheet_names

    # 创建一个字典来存储每个医生在不同sheet中的准确度 (accuracy)
    doctor_data = {sheet_name: {} for sheet_name in sheet_names}

    for sheet_name in sheet_names:
        # 读取工作表数据
        df = excel_file.parse(sheet_name)

        # 提取倒数前6列（各级别医生的判读结果列）和第一列（真实病例的标签列）
        result_columns = df.columns[-6:]
        true_column = df.columns[0]

        # 对于每个医生，计算准确度 (accuracy)
        for col in result_columns:
            correct = (df[col] == df[true_column]).sum()
            total = len(df)
            accuracy = correct / total  # 计算准确度
            if col not in doctor_data[sheet_name]:
                doctor_data[sheet_name][col] = {'accuracy': 0}
            doctor_data[sheet_name][col]['accuracy'] = accuracy

    # 设置图片清晰度
    plt.rcParams['figure.dpi'] = 300

    # 生成x轴坐标
    doctor_names = list(doctor_data[sheet_names[0]].keys())  # 假设每个sheet医生列名相同
    x = np.arange(len(doctor_names))  # 每个医生的位置

    # 每个医生的柱状图宽度
    bar_width = 0.25

    # 定义颜色：每个sheet一个颜色
    sheet_colors = ['#8CCAFD', '#009FF6', '#EE8400']

    # 绘制每个医生的柱状图
    fig, ax = plt.subplots(figsize=(12, 6))
    for i, sheet_name in enumerate(sheet_names):
        # 计算每个医生的位置偏移量
        x_offset = x + (i - 1) * bar_width

        # 获取准确度 (accuracy)
        accuracies = [doctor_data[sheet_name][doctor]['accuracy'] for doctor in doctor_names]

        # 获取原色
        base_color = sheet_colors[i]
        accuracy_color = to_rgba(base_color, alpha=1.0)  # 原色

        # 绘制准确度的柱状图
        ax.bar(x_offset, accuracies, width=bar_width, label=f'{sheet_name}', color=accuracy_color, edgecolor='black')

    # 设置图表标题和标签
    ax.set_title('')  # Accuracy of doctors at different levels in different stages of the process
    ax.set_xlabel('Doctors at all levels')
    ax.set_ylabel('Accuracy')
    ax.set_xticks(x)
    ax.set_xticklabels(doctor_names)

    # 添加图例，统一放在左上角
    ax.legend(loc='upper left', bbox_to_anchor=(0.0, 1.0))

    # 显示图表
    plt.tight_layout()
    plt.show()


# 调用函数，传入Excel文件路径
file_path = 'F:\\文档\\a_6________写作\\turbt_论文\\总体判读对比_验证1-6_v2（论文图专用）.xlsx'
plot_correct_counts(file_path)