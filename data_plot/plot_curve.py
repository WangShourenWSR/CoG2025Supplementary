import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def smooth_curve(values, alpha=0.6):
    """
    使用指数移动平均 (Exponential Moving Average) 来平滑曲线
    （注意：这种平滑方法可能存在滞后效应）
    """
    smoothed = []
    last = values[0]
    for v in values:
        # EMA: last = alpha * last + (1 - alpha) * v
        last = alpha * last + (1 - alpha) * v
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
    figure_title='Comparison of Different Models'
):
    """
    读取多份CSV文件并绘制在同一张图中，并在指定 compare_step 处与 baseline 对比。
    
    在比较位置处，对于每个非 baseline 方法：
      - 画出 baseline 和方法对应数值处的水平虚线（一小段线段）
      - 在这两条虚线上画出一个垂直箭头，并标注提升幅度及百分比
    
    参数说明见注释
    """
    plt.figure(figsize=(10, 6))
    
    # 存储各方法的 (steps, smoothed_values)
    all_steps = {}
    all_smoothed = {}
    
    # 颜色列表
    colors = ['red', 'gold', 'navy', 'green', 'purple', 'darkorange', 'hotpink']
    
    # 1. 读取并绘制所有曲线
    for i, (csv_file, label) in enumerate(zip(csv_files, labels)):
        df = pd.read_csv(csv_file)
        df = df.sort_values(by='Step')
        
        steps = df['Step'].values
        raw_values = df['Value'].values
        
        # 绘制原始曲线（淡色）
        plt.plot(steps, raw_values, color=colors[i % len(colors)], alpha=0.3)
        # 绘制平滑曲线
        smoothed_values = smooth_curve(raw_values, alpha=smoothing_alpha)
        plt.plot(steps, smoothed_values, color=colors[i % len(colors)],
                 label=label, linewidth=2)
        
        all_steps[label] = steps
        all_smoothed[label] = smoothed_values
    
    # 2. 手动设置横轴、纵轴范围
    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)
    
    # 3. 与 baseline 对比：在 compare_step 处画水平虚线和垂直箭头
    if baseline_label is not None and baseline_label in all_steps:
        baseline_steps = all_steps[baseline_label]
        baseline_smooth = all_smoothed[baseline_label]
        
        # 如果 compare_step 为 None 或超出数据范围，则使用 baseline 的最后一个 step
        if compare_step is None or compare_step > baseline_steps.max():
            compare_step = baseline_steps[-1]
        
        # 使用线性插值获取 baseline 在 compare_step 处的平滑值
        baseline_value_at_compare = np.interp(compare_step, baseline_steps, baseline_smooth)
        
        # 为避免多条对比图重叠，定义横向偏移
        total_width = (xlim[1] - xlim[0]) if xlim is not None else (baseline_steps.max() - baseline_steps.min())
        offset_gap = 0.05 * total_width  # 每个方法的横向偏移
        delta = 0.02 * total_width         # 每个水平虚线左右延伸的距离
        
        offset_count = 0
        for label in labels:
            if label == baseline_label:
                continue
            method_steps = all_steps[label]
            method_smooth = all_smoothed[label]
            # 如果 compare_step 超出该方法的范围，则取该方法的最大 step
            actual_compare_step = min(compare_step, method_steps.max())
            method_value_at_compare = np.interp(actual_compare_step, method_steps, method_smooth)
            
            improvement = method_value_at_compare - baseline_value_at_compare
            if baseline_value_at_compare != 0:
                improvement_percent = (improvement / baseline_value_at_compare) * 100
            else:
                improvement_percent = 0.0
            
            # 计算本次对比的横向位置，防止多个方法重叠
            x_center = compare_step + offset_count * offset_gap
            offset_count += 1
            
            left_x = x_center - delta
            right_x = x_center + delta
            
            # 画 baseline 对应处的水平虚线
            plt.hlines(y=baseline_value_at_compare, xmin=left_x, xmax=right_x,
                       linestyles='--', color='gray')
            # 画方法对应处的水平虚线
            plt.hlines(y=method_value_at_compare, xmin=left_x, xmax=right_x,
                       linestyles='--', color='gray')
            
            # 在这两条水平虚线的右侧画一个垂直箭头，连接 baseline 与方法的数值
            plt.annotate("",
                         xy=(right_x, method_value_at_compare),
                         xytext=(right_x, baseline_value_at_compare),
                         arrowprops=dict(arrowstyle='<->', color='black', lw=1))
            
            # 在箭头旁边标注提升信息
            mid_y = (baseline_value_at_compare + method_value_at_compare) / 2
            text = f"{label} improves\n{improvement:.2f} ({improvement_percent:.2f}%)"
            plt.text(right_x + 0.01 * total_width, mid_y, text,
                     fontsize=9, va='center', ha='left',
                     bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", alpha=0.8))
    
    # 4. 设置轴标签和标题
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.title(figure_title, fontsize=14)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # 示例 CSV 文件列表与对应标签
    csv_files = [
        "CNN+self_play_only_training_curve_0.csv",
        "pure_special_move_training_curve_0.csv",
        "purposed_model+hybrid_training_curve_0.csv"
    ]
    labels = [
        "baseline",
        "special move reward",
        "default reward"
    ]
    
    # 指定 baseline 标签
    baseline_label = "baseline"
    
    # 手动设置横轴、纵轴范围
    xlim = (0, 2e7)
    ylim = (0, 5)
    
    # 指定在 x=2e7-100 处比较（可根据需要调整）
    compare_step = 2e7

    plot_experiments(
        csv_files=csv_files,
        labels=labels,
        smoothing_alpha=0.0001,
        baseline_label=baseline_label,
        compare_step=compare_step,
        xlim=xlim,
        ylim=ylim,
        x_label='Training Steps',
        y_label='Average Special Move / Round',
        figure_title='Special Move Using'
    )