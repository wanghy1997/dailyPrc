def compute_pairwise_cosine_similarity(x1, index, info):
    """
        计算特征矩阵 x1 中第 index 条数据与其他所有数据之间的欧氏距离。

        参数:
        x1 (numpy.ndarray): 形状为 (N, D) 的特征矩阵，其中 N 是样本数，D 是特征维度。
        index (int): 要计算距离的样本索引。

        返回:
        numpy.ndarray: 形状为 (N,) 的数组，表示第 index 条数据与其他所有数据之间的欧氏距离。
        """
    # 提取第 index 条数据
    x1 = x1.cpu().numpy()
    query_vector = x1[index]
    # 计算第 index 条数据与其他所有数据之间的欧氏距离
    # 计算每个向量的平方和
    query_vector_sq = np.sum(query_vector ** 2)
    x1_sq = np.sum(x1 ** 2, axis=1)
    # 计算内积矩阵
    inner_product = np.dot(x1, query_vector)
    # 使用公式: distance^2 = (query_vector^2 + x1_sq - 2 * inner_product)
    dist_sq = query_vector_sq + x1_sq - 2 * inner_product
    # 将 NumPy 数组转换为 PyTorch Tensor，指定数据类型为 float32
    dist = torch.sqrt(torch.tensor(dist_sq, dtype=torch.float32))
    del x1, query_vector, x1_sq, inner_product, dist_sq
    return dist


def relaxation(u_rank_arg, l_feature_list, neighbor_num, info, unlabeled_len):
    """
    松弛策略：基于余弦相似性选择样本子集。
    u_rank_arg, g_u_featureMap_list, 5, info['config'].queries, len(name_list), cosine=info['config'].cosine
    Args:
    - u_rank_arg (list): 按某种顺序排序的样本索引列表。
    - l_feature_list (torch.Tensor): 形状为（样本数，特征维度）的特征张量，包含所有样本的特征。
    - neighbor_num (int): 考虑的邻居数量，基于余弦相似性。
    - query_num (int): 要选择的样本数量。
    - unlabeled_len (int): 未标记样本的总数。
    - cosine (float, optional): 余弦相似性阈值，默认为0.85。

    Returns:
    - rank_arg (list): 选定样本的索引列表。
    """
    torch.cuda.empty_cache()  # 释放未使用的显存
    # 初始化标志和计数器
    query_flag = torch.zeros(unlabeled_len, 1)
    chosen_idx = []
    ignore_cnt = 0
    # 创建一个集合以存储有效的索引数字
    valid_indices = set(range(info['config'].train_len))  # 0到100的范围

    # 遍历排序后的样本索引
    for i in u_rank_arg:
        # 遍历列表中的每个元素
        for item in chosen_idx:
            if item in valid_indices:
                chosen_idx.remove(item)
        if len(chosen_idx) == info['config'].queries:
            # 如果已选择了所需数量的样本，则停止
            break

        # 获取第 i 个样本与其他所有样本的余弦相似性
        cos_sim = compute_pairwise_cosine_similarity(l_feature_list, i, info)
        # 按余弦相似性降序排序邻居
        neighbor_arg = torch.argsort(-cos_sim)  # 排序

        # 选择余弦相似性高于阈值的邻居
        if len(neighbor_arg) > 1:
            neighbor_arg = neighbor_arg[cos_sim[neighbor_arg] > info['config'].cosine][1:1 + neighbor_num]
        else:
            neighbor_arg = []

        # 检查邻居中是否有已选择的样本
        neighbor_flag = query_flag[neighbor_arg.cpu()]

        # 如果没有选择的邻居或邻居数量不足，选择当前样本
        if neighbor_flag.sum() == 0 or len(neighbor_arg) < neighbor_num:
            query_flag[i] = 1
            chosen_idx.append(i)
        else:
            ignore_cnt += 1
            continue

    gc.collect()  # 调用垃圾回收器
    if torch.cuda.is_available():
        torch.cuda.empty_cache()  # 释放显存

    return chosen_idx  # 返回最终选定的样本索引列表