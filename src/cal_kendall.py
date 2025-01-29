import os
import pandas as pd
from scipy.stats import pearsonr, kendalltau
import numpy as np


def load_scores(folder, t60_range=None):
    """
    Load scores from CSV files in the folder, associate them with T60 and RIR,
    and optionally filter by T60 range.

    Args:
        folder (str): Path to the folder containing score CSV files.
        t60_range (tuple): A tuple (min_t60, max_t60) specifying the range of T60 values to consider.
                           If None, all T60 values are included.

    Returns:
        pd.DataFrame: A DataFrame with columns: T60, RIR (mic and source position), and score.
    """
    # List all CSV files in the folder
    csv_files = [f for f in os.listdir(
        folder) if f.endswith("_mean_scores.csv")]

    scores = []

    for csv_file in csv_files:
        try:
            # Extract the T60 value from the filename (before "_mean_scores.csv")
            t60 = float(csv_file.split("_mean_scores")[0])

            # Skip files outside the specified T60 range
            if t60_range and not (t60_range[0] <= t60 <= t60_range[1]):
                continue

            csv_path = os.path.join(folder, csv_file)
            # Read the CSV file
            df = pd.read_csv(csv_path, header=None, names=[
                             "rir", "score", "count"])

            # Convert the score column to numeric, coercing errors
            df["score"] = pd.to_numeric(df["score"], errors="coerce")

            # Drop rows with NaN scores
            df = df.dropna(subset=["score"])

            # Add T60 value to each row
            df["t60"] = t60

            # Collect the relevant data
            scores.append(df[["t60", "rir", "score"]])
        except Exception as e:
            print(f"Failed to process {csv_file}: {e}")

    # Concatenate all data into a single DataFrame
    return pd.concat(scores, ignore_index=True) if scores else pd.DataFrame()


def calculate_folders_metrics(folder1, folder2, t60_range=None):
    """
    Calculate Pearson's correlation, Kendall's Tau, and RMSE between two metric folders
    based on paired scores (same T60 and RIR), with an optional T60 range.

    Args:
        folder1 (str): Path to the first folder containing score CSV files.
        folder2 (str): Path to the second folder containing score CSV files.
        t60_range (tuple): A tuple (min_t60, max_t60) specifying the range of T60 values to consider.
                           If None, all T60 values are included.

    Returns:
        dict: Dictionary containing Pearson's correlation, Kendall's Tau, Kendall's p-value, and RMSE.
    """
    # Load scores from both folders
    scores1 = load_scores(folder1, t60_range)
    scores2 = load_scores(folder2, t60_range)

    # Merge the two DataFrames on T60 and RIR
    merged_df = pd.merge(scores1, scores2, on=[
                         "t60", "rir"], suffixes=("_1", "_2"))

    if merged_df.empty:
        raise ValueError(
            "No common T60 and RIR pairs found between the two folders within the specified range."
        )

    # Extract scores
    x = merged_df["score_1"]
    y = merged_df["score_2"]

    # Calculate Pearson's correlation
    pearson_corr, _ = pearsonr(x, y)

    # Calculate Kendall's Tau
    kendall_corr, kendall_p_value = kendalltau(x, y, variant="c")

    # Calculate RMSE
    rmse = np.sqrt(np.mean((x - y) ** 2))

    return {
        "pearson": pearson_corr,
        "kendall": kendall_corr,
        "kendall_p_value": kendall_p_value,
        "rmse": rmse,
    }


if __name__ == "__main__":
    # Define the folders
    folder1 = "siib_scores_english_mean"  # Replace with your first folder path
    folder2 = "stipa_scores_mean"  # Replace with your second folder path

    # Define the T60 range to consider (None means no filtering)
    t60_range = (1.0, 8.0)  # Set to None for no filtering

    try:
        # Calculate metrics between the two folders
        metrics = calculate_folders_metrics(folder1, folder2, t60_range)

        # Print results
        print(f"Pearson correlation: {metrics['pearson']:.3f}")
        print(f"Kendall's Tau correlation: {metrics['kendall']:.3f}")
        print(f"Kendall's Tau p-value: {metrics['kendall_p_value']:.3e}")


    except ValueError as e:
        print(f"Error: {e}")
