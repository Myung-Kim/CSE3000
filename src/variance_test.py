import os
import pandas as pd
from scipy.stats import levene


def get_t60_data(folder):
    """
    Extract data from a folder and organize it by T60.

    Args:
        folder (str): Path to the folder containing the metric files.

    Returns:
        dict: A dictionary where keys are T60 values and values are lists of scores.
    """
    t60_data = {}
    for file_name in os.listdir(folder):
        if file_name.endswith("_mean_scores.csv"):
            try:
                # Extract T60 from the filename
                t60 = float(file_name.split("_mean_scores")[0])
                file_path = os.path.join(folder, file_name)

                # Read the file
                df = pd.read_csv(file_path)

                # Collect scores
                scores = df["mean_score"].tolist()
                t60_data[t60] = scores
            except Exception as e:
                print(f"Error processing {file_name} in {folder}: {e}")
    return t60_data


def levene_test_between_folders(folder1, folder2, output_file="levene_results.csv"):
    """
    Perform Levene's test for variance differences between two folders at each T60.

    Args:
        folder1 (str): Path to the first folder.
        folder2 (str): Path to the second folder.
        output_file (str): Path to save the results as a CSV file.
    """
    # Extract T60 data for both folders
    folder1_data = get_t60_data(folder1)
    folder2_data = get_t60_data(folder2)

    # Find common T60s
    common_t60s = sorted(
        set(folder1_data.keys()).intersection(folder2_data.keys()))

    results = []
    print("\nLevene's Test Results:\n")
    print(f"{'T60':<10}{'Levene_Stat':<15}{'P_Value':<15}")
    print("-" * 40)

    for t60 in common_t60s:
        scores1 = folder1_data[t60]
        scores2 = folder2_data[t60]

        try:
            # Perform Levene's test
            stat, p_value = levene(scores1, scores2)

            results.append({
                "T60": t60,
                "Levene_Stat": stat,
                "P_Value": p_value
            })

            # Print the result to the console
            print(f"{t60:<10}{stat:<15.5f}{p_value:<15.5f}")

        except Exception as e:
            print(f"Error performing Levene's test for T60={t60}: {e}")

    # Save results to a CSV file
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values(by="T60")
    results_df.to_csv(output_file, index=False)
    print(f"\nResults saved to {output_file}")


if __name__ == "__main__":
    # Define the folders to compare
    folder1 = "estoi_scores_english_mean"
    folder2 = "estoi_scores_mandarin_mean"

    # Output file for the results
    output_file = "levene_results_estoi.csv"

    # Perform Levene's test
    levene_test_between_folders(folder1, folder2, output_file)
