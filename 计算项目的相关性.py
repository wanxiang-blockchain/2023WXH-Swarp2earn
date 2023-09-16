# ...
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import urllib.request as urllib2
import json
import  os


folder_path = 'D:\swap2earn\klines3\klines3\gamefi'


# 获取文件夹中所有文件名
file_names = os.listdir(folder_path)

output_folder = 'plots_output'
os.makedirs(output_folder, exist_ok=True)

all_stock_data = []  # List to store data from all files
file_labels = []  # List to store file labels for the legend



# Loop through each file in the folder
for file_name in file_names:
    if file_name.endswith('.xlsx'):  # Only process Excel files
        excel_file = os.path.join(folder_path, file_name)
        stock_index = pd.read_excel(excel_file)
        stock_index.set_index('snapped_at', inplace=True)
        stock_index.sort_index(inplace=True)

        # Append the stock data to the list using the correct column name
        all_stock_data.append(stock_index['price'])  # Replace 'close_price' with the correct column name
        file_labels.append(os.path.splitext(file_name)[0])  # Store the file label

        print(f'Processed: {file_name}')

# Concatenate all stock data into a single DataFrame
combined_data = pd.concat(all_stock_data, axis=1)
combined_data.columns = file_labels

# Calculate the correlation matrix
correlation_matrix = combined_data.corr()

# Create a heatmap of the correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, square=True, cmap='coolwarm')
plt.title('Correlation Matrix')

# Get the top ten projects with the highest correlation (excluding self-correlation)
top_correlations = (correlation_matrix
                    .stack()
                    .sort_values(ascending=False)
                    .reset_index()
                    .rename(columns={0: 'correlation'}))

top_correlations = top_correlations[
    top_correlations['level_0'] != top_correlations['level_1']]  # Exclude self-correlation
top_10_correlations = top_correlations.head(6)

# Get the project names with the highest correlation
top_10_project_names = []
for idx, row in top_10_correlations.iterrows():
    project1 = row['level_0']
    project2 = row['level_1']
    correlation = row['correlation']
    top_10_project_names.append((project1, project2, correlation))

print("Top 10 project pairs with the highest correlation:")
for idx, (project1, project2, correlation) in enumerate(top_10_project_names, start=1):
    print(f"{idx}. {project1} and {project2} (Correlation: {correlation:.2f})")

plt.show()
