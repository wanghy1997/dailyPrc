import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

class MedicalImageVisualizer:
    """
    支持自定义颜色表和 Slicer 颜色表导入的医学图像可视化工具。
    """

    @staticmethod
    def load_nifti_data(image_path, label_path):
        try:
            img_obj = nib.load(image_path)
            lbl_obj = nib.load(label_path)
            image_data = img_obj.get_fdata()
            label_data = lbl_obj.get_fdata().astype(np.int32)
            return image_data, label_data
        except Exception as e:
            print(f"Error loading data: {e}")
            return None, None

    @staticmethod
    def extract_slice(volume_data, axis, slice_index):
        # ... (与之前相同，省略以节省空间) ...
        if axis == 0: return volume_data[slice_index, :, :]
        elif axis == 1: return volume_data[:, slice_index, :]
        elif axis == 2: return volume_data[:, :, slice_index]
        return volume_data # Fallback

    @staticmethod
    def normalize_image(image_slice):
        # ... (与之前相同) ...
        min_val, max_val = np.min(image_slice), np.max(image_slice)
        if max_val - min_val == 0: return image_slice
        return (image_slice - min_val) / (max_val - min_val)

    @staticmethod
    def parse_slicer_color_table(file_path):
        """
        功能: 解析 3D Slicer 导出的颜色表 (.txt)
        
        Slicer 导出格式通常为: No. Name R G B A (R,G,B,A 为 0-255 的整数)
        例如: 
        1 Spleen 255 0 0 255
        2 Liver 0 255 0 255
        """
        color_map = {}
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'): 
                        continue
                    
                    parts = line.split()
                    # 只有当行包含足够的信息时才解析
                    # 格式通常是: ID Name R G B A (有些名字带空格，所以我们要取最后4个作为RGBA)
                    if len(parts) >= 6:
                        try:
                            # ID 是第一个元素
                            class_id = int(parts[0])
                            
                            # RGBA 是最后四个元素
                            r = int(parts[-4]) / 255.0
                            g = int(parts[-3]) / 255.0
                            b = int(parts[-2]) / 255.0
                            # a = int(parts[-1]) / 255.0 # 我们通常忽略文件里的透明度，使用统一的透明度
                            
                            color_map[class_id] = (r, g, b)
                        except ValueError:
                            continue
            print(f"成功从 {file_path} 加载了 {len(color_map)} 个颜色定义。")
            return color_map
        except Exception as e:
            print(f"加载颜色表失败: {e}")
            return {}

    @staticmethod
    def plot_multiclass_contours(image_slice, label_slice, color_map, global_alpha=0.8, line_width=2.0):
        plt.figure(figsize=(10, 10))
        plt.imshow(image_slice.T, cmap='gray', origin='lower')
        
        unique_classes = np.unique(label_slice)
        
        # 预定义 Synapse 13 类的名称映射 (仅用于显示图例 Label)
        # 如果你的 ID 映射不同，请修改这里
        class_names = {
            1: "Spleen", 2: "R.Kidney", 3: "L.Kidney", 4: "Gallbladder",
            5: "Esophagus", 6: "Liver", 7: "Stomach", 8: "Aorta",
            9: "IVC", 10: "Portal/Splenic Vein", 11: "Pancreas",
            12: "R.Adrenal Gland", 13: "L.Adrenal Gland"
        }

        plotted_patches = []
        plotted_labels = []

        for class_id in unique_classes:
            if class_id == 0: continue 

            # 获取颜色
            color = color_map.get(class_id, 'white') # 默认白
            
            binary_mask = (label_slice == class_id)
            
            if np.any(binary_mask):
                plt.contour(
                    binary_mask.T, 
                    levels=[0.5], 
                    colors=[color], 
                    linewidths=line_width, 
                    alpha=global_alpha, 
                    origin='lower'
                )
                
                # 为图例收集信息
                import matplotlib.patches as mpatches
                plotted_patches.append(mpatches.Patch(color=color))
                # 如果有名字就用名字，没有就用 ID
                name = class_names.get(class_id, f"Class {class_id}")
                plotted_labels.append(name)

        if plotted_patches:
            plt.legend(plotted_patches, plotted_labels, loc='upper right', bbox_to_anchor=(1.3, 1))

        plt.title(f"Synapse 13-Class Segmentation")
        plt.axis('off')
        plt.tight_layout() # 防止图例被切掉
        plt.show()

# --- 预设的 Synapse 13 类配色 (参考 Slicer 风格) ---
# 格式: {ID: (R, G, B)} 其中 R,G,B 为 0-1 的浮点数
SYNAPSE_COLOR_MAP = {
    1:  (0.86, 0.45, 0.08),  # Spleen (Orange/Brown)
    2:  (0.00, 0.80, 0.40),  # R.Kidney (Green)
    3:  (0.00, 0.60, 0.30),  # L.Kidney (Darker Green)
    4:  (0.50, 0.50, 0.00),  # Gallbladder (Olive)
    5:  (0.90, 0.80, 0.60),  # Esophagus (Beige)
    6:  (0.80, 0.20, 0.20),  # Liver (Red)
    7:  (0.20, 0.40, 0.80),  # Stomach (Blue)
    8:  (0.90, 0.10, 0.10),  # Aorta (Bright Red)
    9:  (0.10, 0.10, 0.90),  # IVC (Bright Blue)
    10: (0.40, 0.80, 0.90),  # Portal/Splenic Vein (Light Blue)
    11: (0.90, 0.60, 0.80),  # Pancreas (Pink)
    12: (0.80, 0.80, 0.20),  # R.Adrenal (Yellow)
    13: (0.70, 0.70, 0.10)   # L.Adrenal (Darker Yellow)
}

# --- Main 流程 ---
def main():
    # 1. 路径设置
    img_path = '/Users/wanghongyi/datasets/SSL_dataprocess/可视化数据/img0010.nii.gz'
    lbl_path = '/Users/wanghongyi/datasets/SSL_dataprocess/可视化数据/label0010.nii.gz'
    
    visualizer = MedicalImageVisualizer()

    image_data, label_data = visualizer.load_nifti_data(image_path=img_path, label_path=lbl_path)

    # 2. 确定颜色表
    # 选项 A: 使用代码里预设的 SYNAPSE_COLOR_MAP (推荐)
    print("使用预设 Synapse 颜色表...")
    my_colors = SYNAPSE_COLOR_MAP
    
    # 3. 绘图
    visualizer.plot_multiclass_contours(
        visualizer.extract_slice(image_data, 2, 66),
        visualizer.extract_slice(label_data, 2, 66),
        color_map=my_colors,
        global_alpha=0.5
    )

if __name__ == "__main__":
    main()