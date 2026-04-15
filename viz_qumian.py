import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa

# ----------------------------
# 1. 构造类似原图的“帽子形”曲面
# ----------------------------
x = np.linspace(-3, 3, 250)
y = np.linspace(-3, 3, 250)
X, Y = np.meshgrid(x, y)

# 让曲面更像“帽子”，不是太尖的高斯
R = np.sqrt(X**2 + Y**2)
Z = np.exp(-0.45 * R**2)    # 控制形状扁平一些

# ----------------------------
# 2. 放置蓝点（内部）
# ----------------------------
rng = np.random.default_rng(1)
blue_x = rng.uniform(-2.2, 1.2, 20)
blue_y = rng.uniform(-1.2, 1.2, 20)
blue_z = np.exp(-0.45 * (blue_x**2 + blue_y**2))

# ----------------------------
# 3. 红点（靠近边界）
# ----------------------------
angles = np.array([0.3, 1.4, 5.2])  # 手动挑选，让分布更像原图
red_r = 2.7
red_x = red_r * np.cos(angles)
red_y = red_r * np.sin(angles)
red_z = np.exp(-0.45 * (red_x**2 + red_y**2))

# ----------------------------
# 4. 绘图
# ----------------------------
fig = plt.figure(figsize=(7, 6))
ax = fig.add_subplot(111, projection="3d")

# 曲面
ax.plot_surface(
    X, Y, Z,
    cmap="jet",
    linewidth=0,
    antialiased=True,
    alpha=1.0
)

# 线框（加强结构感）
ax.plot_wireframe(
    X, Y, Z,
    rstride=12, cstride=12,
    color="k", alpha=0
)

# 蓝点
ax.scatter(blue_x, blue_y, blue_z, color="royalblue", s=45, zorder=10)

# 红点
ax.scatter(red_x, red_y, red_z, color="red", s=55, zorder=10)

# 底部虚线圈
theta = np.linspace(0, 2*np.pi, 400)
circle_x = 3 * np.cos(theta)
circle_y = 3 * np.sin(theta)
ax.plot(circle_x, circle_y, np.zeros_like(theta), "k--", alpha=0.8)

# 顶部箭头
max_z = np.max(Z)
ax.quiver(0, 0, max_z, 0, 0, 0.8,
          color="black", linewidth=2,
          arrow_length_ratio=0.2)

# 外观设置
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
ax.set_box_aspect([1, 1, 0.5])  # 控制形状扁平程度
ax.view_init(elev=23, azim=45)

plt.tight_layout()
plt.show()