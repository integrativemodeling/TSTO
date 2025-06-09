import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# Set font scale for better visibility (set it once)
sns.set_context("notebook", font_scale=1.8)

# Read in the data (Removed df_star_* data)
df_trifunctional_20 = pd.read_csv('input_data/trifunctional_20.csv', index_col=0).T
df_trifunctional_30 = pd.read_csv('input_data/trifunctional_30.csv', index_col=0).T
df_trifunctional_40 = pd.read_csv('input_data/trifunctional_40.csv', index_col=0).T
df_trifunctional_60 = pd.read_csv('input_data/trifunctional_60.csv', index_col=0).T

df_bi_20 = pd.read_csv('input_data/bifunctional_20.csv', index_col=0).T
df_bi_30 = pd.read_csv('input_data/bifunctional_30.csv', index_col=0).T
df_bi_40 = pd.read_csv('input_data/bifunctional_40.csv', index_col=0).T
df_bi_60 = pd.read_csv('input_data/bifunctional_60.csv', index_col=0).T
df_bi_120 = pd.read_csv('input_data/bifunctional_120.csv', index_col=0).T

# Check if 'Model Accuracy' and 'Cluster Precision' exist in the DataFrames
required_columns = ['Model Accuracy', 'Cluster Precision']
dataframes = [
    df_trifunctional_20, df_trifunctional_30, df_trifunctional_40, df_trifunctional_60,
    df_bi_20, df_bi_30, df_bi_40, df_bi_60, df_bi_120
]

for df in dataframes:
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"'{col}' not found in one of the DataFrames.")

# Function to create plots
def create_plots(metric):
    # Do not set sns.set_context here to avoid cumulative changes

    # Combine the data into separate DataFrames for plotting
    # Main plot data
    data_main = {
        'Bifunctional 20 XLs': df_bi_20[metric],
        'Trifunctional 20 XLs': df_trifunctional_20[metric],
        'Bifunctional 30 XLs': df_bi_30[metric],
        'Trifunctional 30 XLs': df_trifunctional_30[metric],
        'Bifunctional 40 XLs': df_bi_40[metric],
        'Trifunctional 40 XLs': df_trifunctional_40[metric],
        'Bifunctional 60 XLs': df_bi_60[metric],
        'Trifunctional 60 XLs': df_trifunctional_60[metric],
    }

    df_main = pd.DataFrame(data_main)

    # Separate plot data for 120 XLs
    data_120 = {
        'Bifunctional 120 XLs': df_bi_120[metric],
        # Include trifunctional data for 120 XLs if available
        # 'Triangle 120 XLs': df_trifunctional_120[metric],
    }

    df_120 = pd.DataFrame(data_120)

    # Experimental data
    tsto_data = np.random.rand(5) * 0.2 + 0.7  # Random data between 0.7 and 0.9
    dsso_data = [11.11]  # Single data point

    # Create DataFrames
    df_TSTO = pd.DataFrame({
        'Type': 'TSTO',
        metric: tsto_data,
        'Number': '83'
    })

    df_DSSO = pd.DataFrame({
        'Type': 'DSSO',
        metric: dsso_data,
        'Number': '83'
    })

    # Combine the DataFrames
    df_exp = pd.concat([df_TSTO, df_DSSO], ignore_index=True)

    # Create a figure with 3 subplots sharing the y-axis
    fig, axes = plt.subplots(
        1, 3, figsize=(18, 8), sharey=True,
        gridspec_kw={'width_ratios': [4, 0.5, 1]}
    )

    # Define the custom color palette
    custom_palette = {
        'Bifunctional': '#1b85b8',
        'Trifunctional': '#FF6961',
        'TSTO': '#ff7f0e',
        'DSSO': '#2ca02c'
    }

    ## Plot 1: Synthetic Data
    # Prepare data
    df_main_melted = df_main.melt(var_name='Crosslinks', value_name=metric)
    df_main_melted['Type'] = df_main_melted['Crosslinks'].apply(lambda x: x.split()[0])
    df_main_melted['Number'] = df_main_melted['Crosslinks'].apply(lambda x: x.split()[1])

    # Plot
    sns.boxplot(
        x='Number',
        y=metric,
        hue='Type',
        data=df_main_melted,
        palette=custom_palette,
        ax=axes[0]
    )

    sns.stripplot(
        x='Number',
        y=metric,
        hue='Type',
        data=df_main_melted,
        jitter=0.2,
        dodge=True,
        marker='o',
        alpha=0.5,
        color='black',
        size=8,
        ax=axes[0],
        legend=False
    )

    axes[0].set_title('Synthetic Data')
    axes[0].set_xlabel('No. of XL sites')
    axes[0].set_ylabel(f"{metric} (Å)")
    axes[0].grid(True)

    ## Plot 2: Synthetic Data
    # Prepare data
    df_120_melted = df_120.melt(var_name='Crosslinks', value_name=metric)
    df_120_melted['Type'] = df_120_melted['Crosslinks'].apply(lambda x: x.split()[0])
    df_120_melted['Number'] = df_120_melted['Crosslinks'].apply(lambda x: x.split()[1])

    # Plot
    sns.boxplot(
        x='Number',
        y=metric,
        hue='Type',
        data=df_120_melted,
        palette=custom_palette,
        ax=axes[1]
    )

    sns.stripplot(
        x='Number',
        y=metric,
        hue='Type',
        data=df_120_melted,
        jitter=0.2,
        dodge=True,
        marker='o',
        alpha=0.5,
        color='black',
        size=8,
        ax=axes[1],
        legend=False
    )

    #axes[1].set_title('Synthetic Data')
    axes[1].set_xlabel('No. of XL sites')
    axes[1].set_ylabel('')
    axes[1].grid(True)

    ## Plot 3: Experimental Data
    # Plot
    sns.boxplot(
        x='Type',
        y=metric,
        data=df_exp,
        palette=custom_palette,
        ax=axes[2]
    )

    sns.stripplot(
        x='Type',
        y=metric,
        data=df_exp,
        jitter=0.2,
        dodge=True,
        marker='o',
        alpha=0.7,
        color='black',
        size=8,
        ax=axes[2]
    )

    axes[2].set_title('Experimental Data')
    axes[2].set_xlabel('Crosslinker')
    axes[2].set_ylabel('')
    axes[2].grid(True)

    # Adjust legends
    handles0, labels0 = axes[0].get_legend_handles_labels()
    axes[0].legend(
        handles0[:2], labels0[:2], title='Type',
        loc='upper right'
    )
    axes[1].legend().set_visible(False)
    axes[2].legend().set_visible(False)

    # Reduce space between subplots
    plt.subplots_adjust(wspace=0.04)
    plt.tight_layout()

    # Save the plot
    output_dir = 'output_files'
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(
        os.path.join(output_dir, f'whisker_plot_{metric.lower().replace(" ", "_")}.pdf')
    )
    plt.show()

# Create plots for 'Model Accuracy' and 'Cluster Precision'
create_plots('Model Accuracy')
create_plots('Cluster Precision')
