import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def smooth_curve(values, alpha=0.6):
    """
    使用指数移动平均 (Exponential Moving Average) 来平滑曲线
    （注意：单侧 EMA 会产生一定滞后效应）
    """
    smoothed = []
    last = values[0]
    for v in values:
        last = alpha * v + (1 - alpha) * last
        smoothed.append(last)
    return np.array(smoothed)

def plot_experiments(
    csv_files,
    labels,
    smoothing_alpha=0.6,
    baseline_label=None,
    compare_step=None,
    xlim=None,
    ylim=None,
    x_label='Step',
    y_label='Score (or Metric)',
    figure_title='Comparison of Different Models',
    ax=None
):
    """
    读取多份 CSV 文件并在一个坐标系中绘制（支持在多个子图中调用），并在指定 compare_step 处与 baseline 对比。
    
    在比较位置处，对于每个非 baseline 方法：
      - 在该点处画出 baseline 对应值与方法对应值的水平虚线（一小段线段）
      - 在这两条水平虚线之间绘制一根竖直箭头，表示二者的差值，
        并在箭头旁边标注提升百分比。
    
    参数说明与原函数相同，增加了：
      ax : matplotlib.axes.Axes 或 None
        若传入，则在该子图上绘制；否则自动使用当前坐标系。
    """
    if ax is None:
        ax = plt.gca()
    ax.set_title(figure_title, fontsize=22, pad=20)
    ax.set_xlabel(x_label, fontsize=20, labelpad=0)
    ax.set_ylabel(y_label, fontsize=20)
    
    # 存储每条曲线的 steps 与平滑后的数值
    all_steps = {}
    all_smoothed = {}
    
    # 定义颜色列表
    colors = ['#e67e22' , '#3498db', '#7f8c8d','#e74c3c']
    
    # 遍历每个 CSV 文件，读取数据并绘制曲线
    for i, (csv_file, label) in enumerate(zip(csv_files, labels)):
        df = pd.read_csv(csv_file)
        df = df.sort_values(by='Step')
        steps = df['Step'].values
        raw_values = df['Value'].values
        
        # 绘制原始曲线（淡色）
        ax.plot(steps, raw_values, color=colors[i % len(colors)], alpha=0.2, zorder=1)
        # 绘制平滑曲线
        smoothed_values = smooth_curve(raw_values, alpha=smoothing_alpha)
        ax.plot(steps, smoothed_values, color=colors[i % len(colors)],
                label=label, linewidth=2, alpha=1, zorder=4)
        
        all_steps[label] = steps
        all_smoothed[label] = smoothed_values
    
    # 设置横轴和纵轴范围（如果指定）
    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)
    
    # 如果需要进行 baseline 对比
    if baseline_label is not None and baseline_label in all_steps:
        baseline_steps = all_steps[baseline_label]
        baseline_smooth = all_smoothed[baseline_label]
        # 如果 compare_step 未指定或超出范围，则使用 baseline 的最后一个 step
        if compare_step is None or compare_step > baseline_steps.max():
            compare_step = baseline_steps[-1]
        baseline_value_at_compare = np.interp(compare_step, baseline_steps, baseline_smooth)
        
        # 计算一个水平虚线左右的延伸距离
        if xlim is not None:
            total_width = xlim[1] - xlim[0]
        else:
            total_width = baseline_steps.max() - baseline_steps.min()
        delta = 0.02 * total_width  # 水平虚线左右延伸长度
        
        # 先在 baseline 对应值处画一条水平虚线（这里用 axhline 绘制整条横线，或用 hlines 绘制局部短线）
        ax.hlines(y=baseline_value_at_compare, xmin=compare_step - delta, xmax=compare_step + delta,
                  linestyles='--', color='#8e44ad', linewidth=2, zorder=3)
        
        # 为了防止多个对比标注重叠，计算每个方法的横向偏移（这里只是示例，按顺序排列）
        offset_gap = 0.05 * total_width
        offset_count = 1  # 从 1 开始，保证 baseline 不参与
        
        for label in labels:
            if label == baseline_label:
                continue
            method_steps = all_steps[label]
            method_smooth = all_smoothed[label]
            # 如果 compare_step 超出该方法数据范围，则取该方法的最大 step
            actual_compare_step = min(compare_step, method_steps.max())
            method_value_at_compare = np.interp(actual_compare_step, method_steps, method_smooth)
            
            improvement = method_value_at_compare - baseline_value_at_compare
            if baseline_value_at_compare != 0:
                improvement_percent = (improvement / baseline_value_at_compare) * 100
            else:
                improvement_percent = 0.0
            
            # 定义本次对比的横坐标：在 compare_step 附近加上偏移
            x_center = compare_step + offset_count * offset_gap
            offset_count += 1
            
            # 在方法对应值处也画一条水平虚线
            ax.hlines(y=method_value_at_compare, xmin=x_center - delta, xmax=x_center + delta,
                      linestyles='--', color='#8e44ad', linewidth=2, zorder=3)
            
            # 在两条水平虚线的右侧画一个竖直箭头，从 baseline 到方法
            ax.annotate("",
                        xy=(x_center + delta, method_value_at_compare),
                        xytext=(x_center + delta, baseline_value_at_compare),
                        arrowprops=dict(arrowstyle='<->', color='#ff795e', lw=1),
                        zorder=10)
            
            # 在箭头旁边标注提升比例
            mid_y = (baseline_value_at_compare + method_value_at_compare) / 2
            text = f"{label}: {improvement_percent:.2f}%↑"
            ax.text(x_center + delta + 0.01 * total_width, mid_y, text,
                    fontsize=12, va='center',
                    bbox=dict(boxstyle="round,pad=0.3", fc="#c8e6f5", ec="black", alpha=1, zorder=3))
    
    ax.legend(loc='upper left', fontsize=15)
    ax.tick_params(labelsize=14)

if __name__ == "__main__":
    csv_files_1 = [
        "default_distance.csv",
        "defensive_distance.csv",
    ]
    csv_files_2 = [
        "default_projectile.csv",
        "defensive_projectile.csv",
    ]
    labels = [
        "default reward",
        "defensive reward"
    ]
    baseline_label = "baseline"
    xlim_1 = (0, 2e7)
    ylim_1 = (110, 130)
    xlim_2 = (0, 2e7)
    ylim_2 = (0, 4)
    compare_step = 2e7 - 100
    
    # 创建一个包含多个子图的图像（例如：2 行 1 列）
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 5.3))
    
    # 在第一个子图中绘制实验结果
    plot_experiments(
        csv_files=csv_files_1,
        labels=labels,
        smoothing_alpha=0.01,
        baseline_label=baseline_label,
        compare_step=compare_step,
        xlim=xlim_1,
        ylim=ylim_1,
        x_label='Training Steps',
        y_label='Average Distance / Round',
        figure_title='Average Distance (Smoothed)',
        ax=axs[0]
    )
    axs[0].annotate('(a)', xy=(0.5, -0.3), xycoords='axes fraction', ha='center', va='center',
                fontsize=24, fontname='Times New Roman', fontweight='bold')
    
    # 在第二个子图中绘制相同数据，但可更改参数展示不同视角
    plot_experiments(
        csv_files=csv_files_2,
        labels=labels,
        smoothing_alpha=0.01,
        baseline_label=baseline_label,
        compare_step=compare_step,
        xlim=xlim_2,
        ylim=ylim_2,
        x_label='Training Steps',
        y_label='Average Projectile / Round',
        figure_title='Projectile Usage (Smoothed)',
        ax=axs[1]
    )
    axs[1].annotate('(b)', xy=(0.5, -0.3), xycoords='axes fraction', ha='center', va='center',
                fontsize=24, fontname='Times New Roman', fontweight='bold')
    
    # plt.subplots_adjust(hspace=0.7)
    plt.subplots_adjust(wspace=0.4)
    # plt.tight_layout()
    plt.show()