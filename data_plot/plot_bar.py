import matplotlib.pyplot as plt
import numpy as np

# 1. 模型及胜场数据
models = ['Model 1', 'Model 2']
wins = [8, 4]
total_games = 12

# 2. 计算胜率（百分比）
win_rates = [w / total_games * 100 for w in wins]

# 3. 为了避免文字与顶部边框重叠，可以先在 y 轴上预留空间
#    例如，让 y 轴上限比最大柱子再高一些
max_win = max(wins)
upper_margin_factor = 1.2  # 可根据需要调整
ylim_top = max_win * upper_margin_factor

# 4. 创建图像并设置尺寸
plt.figure(figsize=(8, 6))

# 5. 画柱状图
bars = plt.bar(models, wins, color=['steelblue', 'salmon'])

# 6. 设置轴标签和标题
plt.xlabel('Model', fontsize=14)
plt.ylabel('Number of Wins', fontsize=14)
plt.title('Comparison of Model Win Rates', fontsize=16)

# 7. 在每个柱子上方添加文字
for bar, win, rate in zip(bars, wins, win_rates):
    height = bar.get_height()
    # 在柱子顶部加一点偏移（如 0.1），并使用 'va="bottom"' 让文字底部对齐该位置
    plt.text(bar.get_x() + bar.get_width() / 2,
             height + 0.1,
             f'{win} wins\n({rate:.1f}%)',
             ha='center',      # 水平居中
             va='bottom',      # 垂直对齐在文本框底部
             fontsize=12)

# 8. 设置 y 轴上限，让最高的文字也有足够空间
plt.ylim(0, ylim_top)

# 9. 如果仍有重叠，可再做微调：
#    - 增加 figure 的高度
#    - 或者使用 plt.subplots_adjust() 或 plt.tight_layout(rect=...)
# 这里演示再加一点 top margin：
plt.tight_layout(rect=[0, 0, 1, 0.95])

# 10. 显示图像
plt.show()
