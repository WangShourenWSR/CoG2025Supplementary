import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def smooth_curve(values, alpha=0.6):
    """
    使用指数移动平均 (Exponential Moving Average) 来平滑曲线
    alpha 越接近 1，平滑程度越弱
    alpha 越小，平滑程度越强
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
    figure_title='Comparison of Different Models'
):
    """
    读取多份CSV文件并绘制在同一张图中，并在指定 compare_step 处与 baseline 对比。
    
    参数：
    -------
    csv_files : list of str
        CSV 文件的路径列表（从 TensorBoard 导出的文件）。
    labels : list of str
        与 csv_files 一一对应的曲线名称，用于图例。
    smoothing_alpha : float
        平滑曲线时的 alpha 值（指数平滑）。
    baseline_label : str or None
        用于对比提升的基准模型名称。如果不为 None，则会在图中显示所有方法
        相对于 baseline 的提升情况。
    compare_step : float or None
        指定要比较的 x 轴位置（Step）。如果为 None，则默认使用每条曲线的“最后一个 step”进行对比。
    xlim : tuple or None
        (xmin, xmax) 用于手动设置横轴范围。如果为 None，则使用默认范围。
    ylim : tuple or None
        (ymin, ymax) 用于手动设置纵轴范围。如果为 None，则使用默认范围。
    x_label : str
        x 轴名称
    y_label : str
        y 轴名称
    figure_title : str
        图标题
    """
    
    plt.figure(figsize=(10, 6))
    
    # 存储各方法的 (steps, smoothed_values) 和最终分数
    all_steps = {}
    all_smoothed = {}
    
    # 颜色循环，可自定义更多颜色
    colors = ['#7f8c8d','#e67e22', '#3498db', '#e74c3c']
    
    for i, (csv_file, label) in enumerate(zip(csv_files, labels)):
        # 1. 读取 CSV 文件
        # 如果你的 CSV 列名与此不同，请根据实际情况修改
        df = pd.read_csv(csv_file)
        
        # 假设 TensorBoard 导出的列为 ["Wall time", "Step", "Value"]
        # 按 Step 排序
        df = df.sort_values(by='Step')
        
        steps = df['Step'].values
        raw_values = df['Value'].values
        
        # 2. 平滑曲线
        smoothed_values = smooth_curve(raw_values, alpha=smoothing_alpha,)
        
        # 3. 绘制原始曲线（淡色）
        plt.plot(steps, raw_values, color=colors[i % len(colors)], alpha=0.2, zorder =1)
        
        # 4. 绘制平滑曲线
        plt.plot(steps, smoothed_values, color=colors[i % len(colors)], 
                 label=label, linewidth=2, alpha = 1, zorder = 4)
        
        # 保存数据以便后续对比
        all_steps[label] = steps
        all_smoothed[label] = smoothed_values
    
    # 手动设置横纵轴范围
    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)
    
    # 如果需要和 baseline 做对比
    if baseline_label is not None and baseline_label in all_steps:
        baseline_steps = all_steps[baseline_label]
        baseline_smooth = all_smoothed[baseline_label]
        
        # 如果 compare_step 为 None，默认使用 baseline 的最后一个 step
        if compare_step is None:
            compare_step = baseline_steps[-1]
        
        # 线性插值获取 baseline 在 compare_step 处的平滑值
        baseline_value_at_compare = np.interp(compare_step, baseline_steps, baseline_smooth)
        
        # 为所有非baseline的曲线画对比虚线，并标注
        offset_count = 0
        offset_gap = 0.05 * (compare_step if compare_step != 0 else 1)

        # 在baseline处绘制一条平行于x轴的虚线
        plt.axhline(y=baseline_value_at_compare, color='#8e44ad', linestyle='--', linewidth=2)
        
        num_iter = 0
        for label in labels:
            num_iter += 1
            if label == baseline_label:
                continue  # 跳过 baseline 自身
            
            method_steps = all_steps[label]
            method_smooth = all_smoothed[label]
            
            # 在 compare_step 处插值获取该方法的平滑值
            method_value_at_compare = np.interp(compare_step, method_steps, method_smooth)
            
            improvement = method_value_at_compare - baseline_value_at_compare
            # 避免 baseline_value_at_compare 为 0
            if baseline_value_at_compare == 0:
                improvement_percent = 0.0
            else:
                improvement_percent = (improvement / baseline_value_at_compare) * 100

            # 在比较点处绘制一条平行于x轴的虚线
            plt.axhline(y=method_value_at_compare, color='#8e44ad', linestyle='--', linewidth=2)

            # 在该虚线与baseline虚线之间绘制一个向上的箭头，表示提升量
            # 该箭头的位置绘制在x轴的xlim*(num_iter/len(labels))处，即假设有3个label，第一个箭头在xlim的1/3处，第二个在2/3处，第三个在xlim的最右侧
            x_coord = xlim[0] + (xlim[1] - xlim[0]) * (num_iter / (len(labels)+1))
            plt.arrow(x_coord, baseline_value_at_compare, 0, method_value_at_compare - baseline_value_at_compare, 
                      width = 1e5, head_width=5e5, head_length=0.5, length_includes_head= True,
                      fc='#ff795e', ec='#ff795e',
                      alpha = 1, zorder = 10
                      )
            
            # 在箭头中间放一个文本，显示提升比例
            text_y = baseline_value_at_compare + 0.5 * (method_value_at_compare - baseline_value_at_compare)
            # text = f"{label} improves\n{improvement:.2f} ({improvement_percent:.2f}%)"
            text = f"{improvement_percent:.2f}%↑"
            # 在右侧或左侧稍微偏一点写文字
            plt.text(
                x_coord + 0.01 * (xlim[1] - xlim[0]),
                text_y*1.1,
                text,
                fontsize=18,
                va='center',
                bbox=dict(boxstyle="round,pad=0.3", fc="#c8e6f5", ec="black", alpha=1, zorder = 3)
            )

    
    # 设置轴标签和标题
    plt.xlabel(x_label, fontsize=20)
    plt.ylabel(y_label, fontsize=20)
    plt.title(figure_title, fontsize=27)
    
    plt.legend(fontsize=18, loc='upper left')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # 示例：假设你有三份 CSV 文件
    csv_files = [
        "CNN+self_play_only_training_curve_0.csv",
        "purposed_model+hybrid_training_curve_0.csv",
        "pure_special_move_training_curve_0.csv"
    ]
    labels = [
        "baseline",
        "default reward",
        "special move reward",
    ]
    # csv_files = [
    #     "defensive_distance.csv",
    #     "default_distance.csv",
    # ]
    # csv_files = [
    #     "defensive_projectile.csv",
    #     "default_projectile.csv",
    # ]
    # labels = [
    #     "defensive reward",
    #     "default reward",
    # ]
     # 将 baseline_label 设为 "baseline"
    baseline_label = "baseline"
    
    # 手动指定横纵轴范围，例如 x 轴 [0, 5e6]，y 轴 [0, 5]
    xlim = (0, 2e7)
    ylim = (0, 12)
    
    # 指定在 x=2e6 处比较（演示）
    # compare_step = 2e8
    compare_step = 2e7-100

    plot_experiments(
        csv_files=csv_files,
        labels=labels,
        smoothing_alpha=0.01,
        baseline_label=baseline_label,
        compare_step=compare_step,
        xlim=xlim,
        ylim=ylim,
        x_label='Training Steps',
        y_label='Average Special Move / Round',
        figure_title='Special Move Usage (Smoothed)'
    )