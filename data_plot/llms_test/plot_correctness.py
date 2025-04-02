import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Define the name of the sheets in the Excel file
sheet_names = ['DeepSeek-R1-Full','DeepSeek-Llama-8B', 'DeepSeek-Qwen-7B', 'Llama-3.1-8B-Instruct','Qwen2.5-7B-Instruct-1M','Ministral-8B-Instrcut-2410']
colors = ['#12b5cb','steelblue','steelblue','#7f8c8d','#7f8c8d','#7f8c8d']

legal_output_rates = []
format_correctness_rates = []
# For each sheet, read the data and plot it
for sheet_idx, sheet_name in enumerate(sheet_names):
    # Read the Excel file
    df = pd.read_excel('data_plot/llms_test/hyper-agent-test.xlsx', sheet_name=sheet_name)
    
    # Calculate the legal output rate, if a row of data's 'Selection' is not 'N/A', then it is legal output.
    # print(df['Selection'])
    # import time
    # if sheet_idx > 1:
    #     time.sleep(20)
    legal_output_rate = len(df[(df['Selection'] != 'N/A') & (~df['Selection'].isna())]) / len(df) * 100
    legal_output_rates.append(legal_output_rate)

    # Calculate the format correctness rate, if a row of data's 'Number of Json' is 1, then it is format correctness.
    format_correctness_rate = len(df[df['Number of Json'] == 1]) / len(df) * 100
    format_correctness_rates.append(format_correctness_rate)


# Plot the results in two bar subplots
fig, axs = plt.subplots(1, 2, figsize=(12, 8))
fig.suptitle('Output Correctness for different LLMs\n(The Higher the Better)', fontsize=22)

bars1 = axs[0].bar(sheet_names, legal_output_rates, color=colors)
axs[0].bar(sheet_names, legal_output_rates, color=colors)
axs[0].set_title('Json in Output', fontsize=18)
axs[0].set_ylabel('Percentage', fontsize=18)
axs[0].set_xticklabels(sheet_names, rotation=45, ha='right', fontsize=14)
axs[0].set_ylim(0, 119)
for bar in bars1:
    height = bar.get_height()
    axs[0].annotate(f'{height:.2f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=11)

bars2 = axs[1].bar(sheet_names, format_correctness_rates, color=colors)  # 修复这里
axs[1].set_title('Format Correctness', fontsize=18)
axs[1].set_ylabel('Percentage', fontsize=18)
axs[1].set_xticks(np.arange(len(sheet_names)))
axs[1].set_xticklabels(sheet_names, rotation=45, ha='right', fontsize=14)
axs[1].set_ylim(0, 119)
for bar in bars2:
    height = bar.get_height()
    axs[1].annotate(f'{height:.2f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=11)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

