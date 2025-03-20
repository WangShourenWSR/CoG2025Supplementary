import matplotlib.pyplot as plt
import numpy as np

# ==== 数据部分：两组对比 ====
# 第一组对比：8 : 4
models_1 = ['Special Move Reward', 'Baseline']
wins_1 = [8, 4]
total_games_1 = sum(wins_1)
win_rates_1 = [w / total_games_1 * 100 for w in wins_1]

# 第二组对比：8 : 5
models_2 = ['Default Reward', 'Baseline']
wins_2 = [8, 4]
total_games_2 = sum(wins_2)
win_rates_2 = [w / total_games_2 * 100 for w in wins_2]

# ==== 创建图像和两个子图 ====
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
# 定义bar宽度
bar_width = 0.50

# --------------- 子图1 ---------------
ax1 = axes[0]

# 绘制第一组柱状图
bars1 = ax1.bar(models_1, wins_1, color=['steelblue', 'salmon'], width=bar_width)
ax1.tick_params(axis='x', labelsize=17)  # 将 x 轴刻度标签字体大小改为 12

# 设置子图标题、坐标轴标签等
ax1.set_title('Win Rate: \nSpecial Move Reward vs. Baseline', fontsize=19)
# ax1.set_xlabel('Model and Reward Function', fontsize=18)
ax1.set_ylabel('Number of Wins', fontsize=18)

# 为避免文字和图像边缘重叠，预留顶部空间
max_win_1 = max(wins_1)
upper_margin_factor_1 = 1.2
ylim_top_1 = max_win_1 * upper_margin_factor_1
ax1.set_ylim(0, ylim_top_1)

# 在每个柱状图上方标注文字（示例：获胜场次与胜率）
num = 0
for bar, win, rate in zip(bars1, wins_1, win_rates_1):
    num += 1
    height = bar.get_height()
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.1,  # 在柱顶稍向上
        f'{win} wins\n({rate:.1f}%)',
        ha='center',
        va='bottom',
        fontsize=20,
        color='steelblue' if num == 1 else 'salmon',
    )
ax1.annotate('(a)', xy=(0.5, -0.15), xycoords='axes fraction',
             ha='center', va='center',
             fontsize=24, fontname='Times New Roman', fontweight='bold')

# --------------- 子图2 ---------------
ax2 = axes[1]

# 绘制第二组柱状图
bars2 = ax2.bar(models_2, wins_2, color=['steelblue', 'salmon'], width=bar_width)
ax2.tick_params(axis='x', labelsize=17)  # 将 x 轴刻度标签字体大小改为 12

# 设置子图标题、坐标轴标签等
ax2.set_title('Win Rate: \nDefault Reward vs. Baseline', fontsize=19)
# ax2.set_xlabel('Model and Reward Function', fontsize=18)
ax2.set_ylabel('Number of Wins', fontsize=18)

# 同样为顶部文字预留空间
max_win_2 = max(wins_2)
upper_margin_factor_2 = 1.2
ylim_top_2 = max_win_2 * upper_margin_factor_2
ax2.set_ylim(0, ylim_top_2)

# 在每个柱状图上方标注文字
num = 0
for bar, win, rate in zip(bars2, wins_2, win_rates_2):
    num += 1
    height = bar.get_height()
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.1,
        f'{win} wins\n({rate:.1f}%)',
        ha='center',
        va='bottom',
        fontsize=20,
        color='steelblue' if num == 1 else 'salmon',
    )
ax2.annotate('(b)', xy=(0.5, -0.15), xycoords='axes fraction',
             ha='center', va='center',
             fontsize=24, fontname='Times New Roman', fontweight='bold')
# ==== 调整子图布局并显示 ====
# plt.tight_layout()
plt.subplots_adjust(wspace=0.5, bottom=0.2)
plt.show()
