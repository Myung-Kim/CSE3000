import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math


def plot_mean_std(input_folders_with_labels, y_limits=None, folders_per_subplot=2, subplots_per_row=2, show_std=True):
    """
    Generate subplots with error bars (mean and standard deviation) for multiple metrics.

    Args:
        input_folders_with_labels (dict): Dictionary where keys are folder paths containing mean scores CSV files
                                          and values are the labels to use in the plot.
        y_limits (dict): Optional dictionary specifying y-axis limits for each subplot.
                         Format: {subplot_index: (ymin, ymax)}.
        folders_per_subplot (int): Number of folders to plot in each subplot.
        subplots_per_row (int): Number of subplots to display per row.
        show_std (bool): Whether to display standard deviation as error bars.
    """
    plt.rcParams.update({'font.size': 15})

    # Color palette
    colors = plt.cm.tab10.colors  # Use a colormap for distinct colors

    all_t60_values = set()  # Collect all unique T60 values for consistent x-axis
    all_plot_data = []

    # Collect data for each folder
    for folder, label in input_folders_with_labels.items():
        print(f"Processing folder: {folder} with label '{label}'...")
        plot_data = []

        for file_name in os.listdir(folder):
            if file_name.endswith("_mean_scores.csv"):
                # Extract T60 value from the filename
                t60 = file_name.split("_")[0]
                file_path = os.path.join(folder, file_name)

                # Read the CSV file
                df = pd.read_csv(file_path)

                # Append T60 and mean scores
                t60_value = float(t60)
                mean_score = df["mean_score"].mean()
                std_score = df["mean_score"].std()

                all_t60_values.add(t60_value)
                plot_data.append(
                    {"t60": t60_value, "mean": mean_score, "std": std_score})

        # Convert plot_data to a DataFrame and sort by T60
        plot_df = pd.DataFrame(plot_data).sort_values(by="t60")
        all_plot_data.append((plot_df, label))

    # Sort T60 values and create equal spacing for the x-axis
    sorted_t60_values = sorted(all_t60_values)
    x_positions = np.arange(len(sorted_t60_values))

    # Calculate the number of subplots needed
    num_subplots = math.ceil(len(all_plot_data) / folders_per_subplot)
    num_rows = math.ceil(num_subplots / subplots_per_row)
    fig, axes = plt.subplots(num_rows, subplots_per_row, figsize=(
        6 * subplots_per_row, 5 * num_rows), squeeze=False)
    axes = axes.flatten()

    # Plot data in subplots
    for subplot_idx in range(num_subplots):
        ax = axes[subplot_idx]
        start_idx = subplot_idx * folders_per_subplot
        end_idx = start_idx + folders_per_subplot
        current_data = all_plot_data[start_idx:end_idx]

        for idx, (plot_df, label) in enumerate(current_data):
            # Assign colors within the subplot
            color = colors[idx % len(colors)]

            # Map T60 values to x positions
            plot_df["x_pos"] = plot_df["t60"].apply(
                lambda t: x_positions[sorted_t60_values.index(t)]
            )

            # Plot the data
            if show_std:
                ax.errorbar(
                    plot_df["x_pos"], plot_df["mean"], yerr=plot_df["std"], fmt='-o',
                    label=label, color=color, capsize=5, markeredgewidth=3, markersize=5, alpha=0.8,
                    linewidth=2, elinewidth=2
                )
            else:
                ax.plot(
                    plot_df["x_pos"], plot_df["mean"], '-o',
                    label=label, color=color, linewidth=2,
                )

        # Set y-axis limits if provided
        if y_limits and subplot_idx in y_limits:
            ax.set_ylim(y_limits[subplot_idx])
            ax.margins(y=0.1)


        # Format the x-axis for this subplot
        ax.set_xticks(x_positions)
        ax.set_xticklabels(
            [f"{t60:.2f}" for t60 in sorted_t60_values], rotation=45)
        ax.set_xlabel("T60 (s)")
        ax.set_ylabel("Score")
        # ax.set_title(f"Subplot {subplot_idx + 1}")
        ax.legend(title="Metrics")
        ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Hide unused subplots
    for idx in range(num_subplots, len(axes)):
        fig.delaxes(axes[idx])

    plt.tight_layout()
    plt.show()


# Example usage:
input_folders_with_labels = {
    "haspi_scores_english_mean": "HASPI English",
    "haspi_scores_mandarin_mean": "HASPI Mandarin",
    "estoi_scores_english_mean": "ESTOI English",
    "estoi_scores_mandarin_mean": "ESTOI Mandarin",
    "siib_scores_english_mean": "SIIB English",
    "siib_scores_mandarin_mean": "SIIB Mandarin",
    "stipa_scores_mean": "STIPA",
}

# Set y-axis limits for specific subplots
y_axis_limits = {
    0: (0, 1.1),   # Subplot 0: y-axis range 0 to 1
    1: (0, 1.1),  # Subplot 1: y-axis range 0.5 to 1
    2: (0, 490),
    3: (0, 1.1),
}

plot_mean_std(input_folders_with_labels, y_limits=y_axis_limits,
              folders_per_subplot=2, subplots_per_row=2, show_std=True)
