import pandas as pd
import matplotlib.pyplot as plt
import ast  # 解析 95% CI 格式的字符串


def plot_mean_variance(df_dict, metric_name, variance_name, title, ylabel):
    """
    绘制不同方法在 1-5 轮次中的某个指标折线图（均值 + 方差），
    方差通过带状区域来表示。

    :param df_dict: 一个字典，键为方法名（Sheet 名），值为 DataFrame
    :param metric_name: 需要绘制的均值指标列名，例如 'Avg Dice'
    :param variance_name: 方差列名，例如 'Var Dice'
    :param title: 图表标题
    :param ylabel: Y 轴标签
    """
    plt.figure(figsize=(10, 6))

    # 颜色列表
    colors = ['b', 'g', 'y', 'c', 'm', 'r', 'k']

    # 标记样式列表
    markers = ['o', 's', '^', 'D', 'p', 'X', '*']

    for idx, (method, df) in enumerate(df_dict.items()):
        # 获取方差
        df['Variance'] = df[variance_name]

        # 绘制均值折线
        plt.plot(df['Round'], df[metric_name],
                 label=method,
                 color=colors[idx % len(colors)],
                 marker=markers[idx % len(markers)],
                 linestyle='-')

        # 填充方差区域（用均值 ± 方差表示）
        plt.fill_between(df['Round'],
                         df[metric_name] - df['Variance'],
                         df[metric_name] + df['Variance'],
                         color=colors[idx % len(colors)],
                         alpha=0.2)


    # 设置横轴刻度，只显示 1 到 5 的整数
    plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,14,15])

    # 图表设置
    plt.xlabel("Round (Active Learning)")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_metric(df_dict, metric_name, ci_name, title, ylabel):
    """
    绘制不同方法在 1-5 轮次中的某个指标折线图（均值 + 95% 置信区间），不同方法使用不同的标记。

    :param df_dict: 一个字典，键为方法名（Sheet 名），值为 DataFrame
    :param metric_name: 需要绘制的均值指标列名，例如 'Avg Dice'
    :param ci_name: 置信区间列名，例如 '95% CI Dice'
    :param title: 图表标题
    :param ylabel: Y 轴标签
    """
    plt.figure(figsize=(10, 6))

    # 颜色列表
    colors = ['b', 'g', 'y', 'c', 'm', 'r', 'k']

    # 标记样式列表
    markers = ['o', 's', '^', 'D', 'p', 'X', '*']

    for idx, (method, df) in enumerate(df_dict.items()):
        # 解析 95% CI
        df[ci_name] = df[ci_name].apply(ast.literal_eval)
        df['CI Lower'] = df[ci_name].apply(lambda x: x[0])
        df['CI Upper'] = df[ci_name].apply(lambda x: x[1])

        # 绘制均值折线（不同方法使用不同的标记）
        plt.plot(df['Round'], df[metric_name],
                 label=method,
                 color=colors[idx % len(colors)],
                 marker=markers[idx % len(markers)],  # 设置不同的标记
                 linestyle='-')

        # 填充置信区间
        plt.fill_between(df['Round'], df['CI Lower'], df['CI Upper'],
                         alpha=0.2,
                         color=colors[idx % len(colors)])

    # 图表设置
    # 设置横轴刻度，只显示 1 到 5 的整数
    plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,14,15])
    plt.xlabel("Round (Active Learning)")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_metric_from_excel(file_path):
    """
    读取 Excel 文件，并绘制 Dice、HD95、ASSD、Recall 的折线图。

    :param file_path: Excel 文件路径
    """
    xls = pd.ExcelFile(file_path)
    df_dict = {}

    # 遍历所有方法（Sheet）
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        df = df[df['Round'].between(1, 15)]  # 过滤 1-5 轮次
        df_dict[sheet_name] = df

    # 绘制不同指标的变化曲线
    plot_metric(df_dict, "Avg Dice", "95% CI Dice", "Dice Score Progression (Mean & 95% CI)", "Dice Score")
    plot_metric(df_dict, "Avg HD95", "95% CI HD95", "HD95 Score Progression (Mean & 95% CI)", "HD95 Score")
    plot_metric(df_dict, "Avg ASSD", "95% CI ASSD", "ASSD Score Progression (Mean & 95% CI)", "ASSD Score")
    plot_metric(df_dict, "Avg Recall", "95% CI Recall", "Recall Score Progression (Mean & 95% CI)", "Recall Score")
    # 示例调用
    plot_mean_variance(df_dict, metric_name='Avg Dice', variance_name='Var Dice', title='Dice Score with Variance', ylabel='Dice Score')
    plot_mean_variance(df_dict, metric_name='Avg HD95', variance_name='Var HD95', title='HD95 Score with Variance', ylabel='HD95 Score')
    plot_mean_variance(df_dict, metric_name='Avg ASSD', variance_name='Var ASSD', title='ASSD Score with Variance', ylabel='ASSD Score')
    plot_mean_variance(df_dict, metric_name='Avg Recall', variance_name='Var Recall', title='Recall Score with Variance', ylabel='Recall Score')


# 运行代码（替换为你的 Excel 文件路径）
file_path = "F:\\文档\\a_6________写作\\active_learning__1\\结果数据表格.xlsx"
plot_metric_from_excel(file_path)
