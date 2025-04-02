import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Define the name of the sheets in the Excel file
sheet_names = ['DeepSeek-R1-Full','DeepSeek-Llama-8B', 'DeepSeek-Qwen-7B', 'Llama-3.1-8B-Instruct','Qwen2.5-7B-Instruct-1M','Ministral-8B-Instrcut-2410']
colors = ['#12b5cb','steelblue','steelblue','#7f8c8d','#7f8c8d','#7f8c8d']

entropies_type = []
entropies_character = []
# For each sheet, read the data and plot it
for sheet_idx, sheet_name in enumerate(sheet_names):
    # Read the Excel file
    df = pd.read_excel('data_plot/llms_test/hyper-agent-test.xlsx', sheet_name=sheet_name)
    # If the data is 'N/A', just remvoe this data from the calculation.
    df = df[df['Type'] != 'N/A']
    df = df[df['Character'] != 'N/A']

    # Calculate the entropy of the 'Type' column
    value_counts_type = df['Type'].value_counts(normalize=True)
    entropy_type = -np.sum(value_counts_type * np.log2(value_counts_type))

    # Calculate the entropy of the 'Character' column
    value_counts_character = df['Character'].value_counts(normalize=True)
    entropy_character = -np.sum(value_counts_character * np.log2(value_counts_character))

    # Append the results to the lists
    entropies_type.append(entropy_type)
    entropies_character.append(entropy_character)




# Plot the results in two bar subplots
fig, axs = plt.subplots(1, 2, figsize=(12, 8))
fig.suptitle('Entropy of Type and Character for Different LLMs\n(The Lower the Better)', fontsize=22)

bars1 = axs[0].bar(sheet_names, entropies_type, color=colors)
axs[0].bar(sheet_names, entropies_type, color=colors)
axs[0].set_title('Selected DRL Agent Type', fontsize=18)
axs[0].set_ylabel('Entropy', fontsize=18)
axs[0].set_xticklabels(sheet_names, rotation=45, ha='right', fontsize=14)
axs[0].set_ylim(0, max(entropies_type) + 0.5)
for bar in bars1:
    height = bar.get_height()
    axs[0].annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=12)

bars2 = axs[1].bar(sheet_names, entropies_character, color=colors)  # 修复这里
axs[1].set_title('Selected Character', fontsize=18)
axs[1].set_ylabel('Entropy', fontsize=18)
axs[1].set_xticks(np.arange(len(sheet_names)))
axs[1].set_xticklabels(sheet_names, rotation=45, ha='right', fontsize=14)
axs[1].set_ylim(0, max(entropies_character) + 0.5)
for bar in bars2:
    height = bar.get_height()
    axs[1].annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=12)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()





