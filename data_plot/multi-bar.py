import matplotlib.pyplot as plt
import numpy as np

# Data for the grouped bar chart
# Modify these lists to add or remove categories and adjust data.
categories = ['Overall\nEnjoyability', 'Difficulty\nSuitability', 'Diversity\nand Expectation', 'Preferrd\nGroup']
exp_data = [1.67, 1.67, 1.5, 3]      # Experimental group data
control_data = [1.17, 1.33, 1.5, 2]  # Control group data

# Define the bar width and the positions on the x-axis
bar_width = 0.32
x = np.arange(len(categories))

# Create the figure and axes
fig, ax = plt.subplots(figsize=(10, 6))

# Plot the bars for both groups, placing them side-by-side
bars_exp = ax.bar(x - bar_width/2, exp_data, bar_width,
                  label='Experimental', color='steelblue')
bars_control = ax.bar(x + bar_width/2, control_data, bar_width,
                      label='Control', color='#7f8c8d')

# Set the x-axis tick positions and labels
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=18)

# Set axis labels and title
# ax.set_xlabel('Data Category', fontsize=18)
ax.set_ylabel('Value', fontsize=20)
ax.set_ylim(0, 3.5)  # Adjust y-axis limit to fit the data
ax.set_title('User Study:\nEnjoyability Score', fontsize=24)

# Place the legend at the upper left corner
ax.legend(loc='upper left', fontsize=18)

def autolabel(bars):
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,  # X position: center of bar
            height,                             # Y position: top of bar
            f'{height}',                        # Text label: the bar height
            ha='center', va='bottom',           # Centered horizontally, aligned at the bottom vertically
            fontsize=20
        )

# Add text labels for both experimental and control bars
autolabel(bars_exp)
autolabel(bars_control)

# Adjust layout to ensure there is no clipping
plt.tight_layout()
plt.show()