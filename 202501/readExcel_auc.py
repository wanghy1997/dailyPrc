from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_category_auc(file_path):
    # 设置 matplotlib 字体为支持中文的字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 读取Excel文件
    excel_file = pd.ExcelFile(file_path)
    sheet_names = excel_file.sheet_names

    # 创建一个字典来存储每个医生在不同sheet中的各类别的AUC值
    doctor_data = {sheet_name: {} for sheet_name in sheet_names}

    # 类别列表
    categories = [0, 1, 2, 3, 4, 5, 6]

    for sheet_name in sheet_names:
        # 读取工作表数据
        df = excel_file.parse(sheet_name)

        # 提取倒数前6列（各级别医生的判读结果列）和第一列（真实病例的标签列）
        result_columns = df.columns[-6:]
        true_column = df.columns[0]

        for col in result_columns:
            if col not in doctor_data[sheet_name]:
                doctor_data[sheet_name][col] = {category: {'auc': 0} for category in categories}

            # 对每个类别计算AUC
            for category in categories:
                # 获取真实标签和预测标签的概率
                category_true = (df[true_column] == category).astype(int)  # 真实标签
                category_pred = df[col].astype(int)  # 预测标签

                # 计算ROC曲线的FPR, TPR以及AUC
                fpr, tpr, _ = roc_curve(category_true, category_pred)
                auc_score = auc(fpr, tpr)

                # 存储AUC值
                doctor_data[sheet_name][col][category]['auc'] = auc_score

    # 设置图片清晰度
    plt.rcParams['figure.dpi'] = 300

    # 创建子图：7个子图分别表示7个类别
    fig, axes = plt.subplots(7, 1, figsize=(15, 20))
    fig.subplots_adjust(hspace=0.5)

    # 定义医生的颜色
    sheet_colors = ['blue', 'green', 'orange']

    for i, category in enumerate(categories):
        ax = axes[i]  # 获取第i个子图

        # 定义柱状图的宽度
        bar_width = 0.2
        x_positions = np.arange(len(doctor_data[sheet_names[0]]))  # 获取医生的数量

        # 绘制每个医生的AUC值，sheet之间相邻
        for j, sheet_name in enumerate(sheet_names):
            # 获取每个医生在当前类别下的AUC值
            auc_scores = [doctor_data[sheet_name][doctor][category]['auc'] for doctor in doctor_data[sheet_name]]

            # 计算相邻的位置偏移量
            x_offset = x_positions + j * bar_width

            # 获取当前sheet_name的颜色
            category_color = sheet_colors[j]

            # 绘制AUC值的柱状图
            ax.bar(x_offset, auc_scores, width=bar_width, label=f'{sheet_name} 类别 {category}', color=category_color, edgecolor='black')

        # 设置每个子图的标题和标签
        ax.set_title(f'类别 {category} 的AUC')
        ax.set_xlabel('各级别医生')
        ax.set_ylabel('AUC')
        ax.set_xticks(x_positions + bar_width * (len(sheet_names) - 1) / 2)  # 中间对齐
        ax.set_xticklabels(doctor_data[sheet_names[0]].keys())
        ax.legend()

    # 显示图表
    plt.tight_layout()
    plt.show()

# 调用函数，传入Excel文件路径
file_path = 'F:\\文档\\a_6________写作\\turbt_论文\\总体判读对比_验证1-6_v2.xlsx'
plot_category_auc(file_path)
