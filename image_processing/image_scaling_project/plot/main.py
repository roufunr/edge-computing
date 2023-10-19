import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the style using Seaborn
sns.set(style="whitegrid", rc={"axes.facecolor": "#f0f0f0", "grid.linestyle": "--"})

# Read the CSV data into a DataFrame
data = pd.read_csv('orin_latency.csv')  # Replace with your filename

# Create a box and whisker plot
plt.figure(figsize=(16, 10))

# Extract numeric columns (excluding the 'sample/latency' column)
numeric_columns = data.columns[1:]
boxplot = plt.boxplot(data[numeric_columns], labels=numeric_columns, patch_artist=True)

# Set colors for the boxes
colors = sns.color_palette("pastel")
for patch, color in zip(boxplot['boxes'], colors):
    patch.set_facecolor(color)

plt.yscale('log')  # Set y-axis to log scale
plt.ylabel('Transfer time (Log Scale - ms)')

plt.title('Box and Whisker Plot of Transfer Latency')
plt.xlabel('Frame')  # Add x-axis label
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='dashed', which='both', alpha=0.6)

# Add legend for the boxes
plt.legend(boxplot["boxes"], numeric_columns, loc='upper right')

plt.tight_layout()
plt.show()
