import cv2
import os

# 输入视频路径和输出帧目录
video_path = 'G://Datasets//laji//laji_/VID_20240527_152311.mp4'
output_dir = 'G://Datasets//laji//laji_/frames_paper'

# 创建输出目录（如果不存在）
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 打开视频文件
cap = cv2.VideoCapture(video_path)

frame_count = 0
while True:
    # 逐帧读取视频
    ret, frame = cap.read()
    if not ret:
        break
    if frame_count % 4 == 0:
        # 生成输出文件名
        frame_filename = os.path.join(output_dir, f'frame_{frame_count:04d}.jpg')

        # 保存帧为图片
        cv2.imwrite(frame_filename, frame)

    frame_count += 1
"""

1.关于poster：先演示整个流程，再一块立起支架，准备其他材料（透明胶带、小刀），最后分好组（4-7人），每组负责一列；
2.关于装袋：装袋也是分小组，组内大概10个人，按照流水线的顺序，每人负责好2-3个广告，传递给下一个，一直到最后装袋，只要每个人没有遗漏，就不会出错；
"""
# 释放视频捕获对象
cap.release()

print(f'Total {frame_count} frames extracted.')
