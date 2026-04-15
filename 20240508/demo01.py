import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FixedLocator

# Random strategy values (assuming these are provided by you)
random_values = np.array([0.6601, 0.6603, 0.6639, 0.662, 0.6653, 0.6611, 0.6638, 0.6586, 0.6617, 0.6617])
# random_values = np.array([0.6492, 0.6634, 0.6555, 0.6594, 0.6615])
# Actual values for the methods without the differences applied
actual_values = np.array([
    [0.6593, 0.6629, 0.6627, 0.6674, 0.6674, 0.6674, 0.6674, 0.6674, 0.6674, 0.6674],
    [0.6539, 0.6646, 0.6576, 0.6674, 0.6584, 0.6672, 0.6606, 0.6587, 0.6573, 0.6573],
    [0.6625, 0.6596, 0.6523, 0.6364, 0.6343, 0.6336, 0.5534, 0.5979, 0.6264, 0.6264],
    [0.6500, 0.6580, 0.6562, 0.6529, 0.6554, 0.6507, 0.6548, 0.6554, 0.6418, 0.6418]
])

# actual_values = np.array([
#     [0.65, 0.658, 0.6562, 0.6529, 0.6554],
#     [0.6625, 0.6596, 0.6523, 0.6364, 0.6343],
#     [0.6539, 0.6646, 0.6576, 0.6674, 0.6584, 0.6672, 0.6607, 0.6587, 0.6573, 0.6573],
#     [0.6593, 0.6629, 0.6627, 0.6674, 0.6674, 0.6674, 0.6674, 0.6674, 0.6674, 0.6674],
# ])

# Compute the differences between actual values and random values
values = (actual_values - random_values) * 100

# Data from the image
methods = ['MVDAL_activeFT', 'MVDAL_cluster', 'distance', 'entropy']
al_num = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

# Create a figure and axis with a specific size
fig, ax = plt.subplots(figsize=(10, 6))  # Width x Height in inches
cmap = plt.get_cmap('coolwarm')
# Set the aspect of the plot to 'auto', 'equal', or a numeric value
ax.set_aspect('equal')  # Makes each cell square

# Create a mesh grid and plot
x = np.arange(len(al_num) + 1)
y = np.arange(len(methods) + 1)
cax = ax.pcolormesh(x, y, values, cmap=cmap, edgecolors='white', linewidth=1, vmin=-1.5, vmax=1.5)

# Add color bar
fig.colorbar(cax)

# Set ticks
ax.set_xticks(x[:-1] + 0.5)
ax.set_yticks(y[:-1] + 0.5)

# Fix the tick labels issue by specifying tick locations explicitly
ax.xaxis.set_major_locator(FixedLocator(x[:-1] + 0.5))
ax.yaxis.set_major_locator(FixedLocator(y[:-1] + 0.5))

# Set labels
ax.set_xticklabels(al_num)
ax.set_yticklabels(methods)

# Set axis labels
ax.set_xlabel('AL Iterations (budget=5)')
ax.set_ylabel('AL Methods')

# Annotate each cell with the numeric value
for (i, j), val in np.ndenumerate(values):
    ax.text(j + 0.5, i + 0.5, f'{val:.2f}', ha='center', va='center', color='white' if abs(val) > 1 else 'black')

plt.show()
