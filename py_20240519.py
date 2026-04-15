import random

# 定义一个包含12个线路的列表
options = [
    "线路1",
    "线路2",
    "线路3",
    "线路4",
    "线路5",
    "线路6",
    "国博线",
    "线路9",
    "线路10",
    "线路18"
]

# 使用random.choice()函数从列表中随机选择一个线路
selected_option = random.choice(options)

# 打印选择的线路
print("随机选择的线路是:", selected_option)
