import pandas as pd
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, f1_score, recall_score, confusion_matrix

# 读取Excel文件（或者CSV文件）
df = pd.read_excel('F://文档//a_6________写作//turbt_论文//0(0)-12(1)-34(2)-56(3).xlsx')

# 假设第一列是原始标签，第二列是模型预测结果
y_true = df.iloc[:, 0]  # 第一列：原始标签
y_pred = df.iloc[:, 1]  # 第二列：模型预测结果

# 计算评估指标

# Accuracy (准确率)
accuracy = accuracy_score(y_true, y_pred)

# Precision (精确度), 使用 'macro' 平均方式
precision = precision_score(y_true, y_pred, average='macro', zero_division=0)

# F1 Score (F1 分数), 使用 'macro' 平均方式
f1 = f1_score(y_true, y_pred, average='macro')

# Recall (召回率), 使用 'macro' 平均方式
recall = recall_score(y_true, y_pred, average='macro')

# Specificity (特异度)
# 计算多分类的特异度需要对每个类别逐一进行计算，这里通过混淆矩阵来获取。
cm = confusion_matrix(y_true, y_pred, labels=[0, 1, 2, 3])
# 计算每个类别的TN, FP, FN, TP
specificity = {}
for i in range(4):  # 针对每个类别计算特异度
    tn = cm.sum() - cm[:, i].sum() - cm[i, :].sum() + cm[i, i]
    fp = cm[:, i].sum() - cm[i, i]
    specificity[i] = tn / (tn + fp)

# AUC (对于多分类问题)
# 如果模型输出的是每个类别的预测概率，使用 'multi_class="ovr"' 和平均方式
# 注意：如果你没有预测概率，可以跳过 AUC 的计算，或者使用 One-vs-Rest 来计算
# 假设你有每个类别的预测概率存储在 y_pred_proba 中，y_pred_proba.shape = (n_samples, 4)
# auc = roc_auc_score(y_true, y_pred_proba, multi_class='ovr', average='macro')

# 打印结果
print(f"Accuracy: {accuracy:.4f}")
print(f"Precision (macro): {precision:.4f}")
print(f"F1 Score (macro): {f1:.4f}")
print(f"Recall (macro): {recall:.4f}")
print("Specificity by class:")
for i in range(4):
    print(f"  Class {i}: Specificity = {specificity[i]:.4f}")
