from sklearn.metrics import recall_score
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_category_recall(file_path):
    # 设置 matplotlib 字体为支持中文的字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 读取Excel文件
    excel_file = pd.ExcelFile(file_path)
    sheet_names = excel_file.sheet_names

    # 创建一个字典来存储每个医生在不同sheet中的各类别的Recall值
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
                doctor_data[sheet_name][col] = {category: {'recall': 0} for category in categories}

            # 对每个类别计算Recall
            for category in categories:
                # 获取真实标签和预测标签
                category_true = (df[true_column] == category).astype(int)
                category_pred = (df[col] == category).astype(int)

                # 计算Recall值
                recall = recall_score(category_true, category_pred, zero_division=0)

                # 存储Recall值
                doctor_data[sheet_name][col][category]['recall'] = recall

    # 设置图片清晰度
    plt.rcParams['figure.dpi'] = 300

    # 创建子图：7个子图分别表示7个类别
    fig, axes = plt.subplots(7, 1, figsize=(15, 20))
    fig.subplots_adjust(hspace=0.5)

    # 定义医生的颜色
    sheet_colors = ['blue', 'green', 'orange']

    for i, category in enumerate(categories):
        ax = axes[i]  # 获取第i个子图

        for j, sheet_name in enumerate(sheet_names):
            # 获取每个医生在当前类别下的Recall值
            recall_scores = [doctor_data[sheet_name][doctor][category]['recall'] for doctor in doctor_data[sheet_name]]

            # 获取当前sheet_name的颜色
            category_color = sheet_colors[j]

            # 绘制Recall值的柱状图
            ax.bar(np.arange(len(doctor_data[sheet_name])), recall_scores, width=0.2, label=f'{sheet_name} 类别 {category}', color=category_color, edgecolor='black')

        # 设置每个子图的标题和标签
        ax.set_title(f'类别 {category} 的Recall')
        ax.set_xlabel('各级别医生')
        ax.set_ylabel('Recall')
        ax.set_xticks(np.arange(len(doctor_data[sheet_names[0]])))
        ax.set_xticklabels(doctor_data[sheet_names[0]].keys())
        ax.legend()

    # 显示图表
    plt.tight_layout()
    plt.show()

# 调用函数，传入Excel文件路径
file_path = 'F:\\文档\\a_6________写作\\turbt_论文\\总体判读对比_验证1-6_v2.xlsx'
plot_category_recall(file_path)
