import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math


def plot_scatter(x_folders_with_labels, y_folder, output_label, subplots_per_row=2):
    """
    Generate scatter plots where each subplot compares one x-folder with the y-folder.
    The dots for each T60 are colored differently.

    Args:
        x_folders_with_labels (dict): Dictionary where keys are folder paths for the x-axis
                                      and values are their corresponding labels.
        y_folder (str): Folder containing data for the y-axis.
        output_label (str): Label for the y-axis data.
        subplots_per_row (int): Number of subplots to display per row.
    """
    plt.rcParams.update({'font.size': 15})

    # Collect data for the y-folder
    print(f"Processing Y folder: {y_folder} with label '{output_label}'...")
    y_data = {}
    for file_name in os.listdir(y_folder):
        if file_name.endswith("_mean_scores.csv"):
            t60 = file_name.split("_")[0]
            file_path = os.path.join(y_folder, file_name)
            df = pd.read_csv(file_path)
            for _, row in df.iterrows():
                rir = row["rir"]
                y_data[(t60, rir)] = row["mean_score"]

    # Prepare subplots
    num_subplots = len(x_folders_with_labels)
    num_rows = math.ceil(num_subplots / subplots_per_row)
    fig, axes = plt.subplots(num_rows, subplots_per_row, figsize=(
        6 * subplots_per_row, 5 * num_rows), squeeze=False)
    axes = axes.flatten()

    # Iterate over x folders
    for subplot_idx, (x_folder, x_label) in enumerate(x_folders_with_labels.items()):
        ax = axes[subplot_idx]
        print(f"Processing X folder: {x_folder} with label '{x_label}'...")
        x_data = {}

        # Collect data for the x-folder
        for file_name in os.listdir(x_folder):
            if file_name.endswith("_mean_scores.csv"):
                t60 = file_name.split("_")[0]
                file_path = os.path.join(x_folder, file_name)
                df = pd.read_csv(file_path)
                for _, row in df.iterrows():
                    rir = row["rir"]
                    x_data[(t60, rir)] = row["mean_score"]

        # Match data points between x and y folders
        common_keys = sorted(set(x_data.keys()).intersection(y_data.keys()))
        x_scores = np.array([x_data[key] for key in common_keys])
        y_scores = np.array([y_data[key] for key in common_keys])
        t60_values = [key[0] for key in common_keys]  # Extract T60 values

        # Generate distinct colors for each T60 value
        unique_t60 = sorted(set(t60_values))
        color_map = {t60: plt.cm.viridis(i / len(unique_t60))
                     for i, t60 in enumerate(unique_t60)}

        # Scatter plot for current x-folder against the y-folder
        for t60, x, y in zip(t60_values, x_scores, y_scores):
            ax.scatter(
                x, y, label=f"T60={t60}", color=color_map[t60],
                alpha=0.8, edgecolor='k', s=30  # Marker size
            )

        # Plot settings for the subplot
        ax.set_xlabel(f"{x_label} (Scores)")
        ax.set_ylabel(f"{output_label} (Scores)")
        # ax.set_title(f"{x_label} vs {output_label}")
        ax.grid(alpha=0.5, linestyle='--')
        # ax.legend()

    # Hide unused subplots
    for idx in range(len(x_folders_with_labels), len(axes)):
        fig.delaxes(axes[idx])

    plt.tight_layout()
    plt.show()


# Example usage:
x_folders_with_labels = {
    "haspi_scores_english_mean": "HASPI English",

    "estoi_scores_english_mean": "ESTOI English",

    "siib_scores_english_mean": "SIIB English",

    "haspi_scores_mandarin_mean": "HASPI Mandarin",
    "estoi_scores_mandarin_mean": "ESTOI Mandarin",
    "siib_scores_mandarin_mean": "SIIB Mandarin",
}

y_folder = "stipa_scores_mean"
output_label = "STIPA"

plot_scatter(x_folders_with_labels, y_folder, output_label, subplots_per_row=3)
