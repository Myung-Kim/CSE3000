import os
import csv
import numpy as np
import soundfile as sf
from pystoi import stoi
from joblib import Parallel, delayed

# Paths
clean_audio_folder = "clean_english"  # Folder containing clean .wav files
# Base folder containing subfolders for degraded files
degraded_base_folder = "clean_english_zero"
# Name of the folder to save the .csv file
output_folder_name = "estoi_scores_zero_english"
output_folder_path = os.path.join(os.getcwd(), output_folder_name)

# Ensure the output folder exists
os.makedirs(output_folder_path, exist_ok=True)

# List all T60 folders
t60_folders = [
    f for f in os.listdir(degraded_base_folder) if os.path.isdir(os.path.join(degraded_base_folder, f))
]


def process_rir_folder(rir_folder_path, clean_audio_folder, output_csv_path, rir_subfolder_name):
    """
    Process a single RIR folder to calculate eSTOI scores.
    """
    with open(output_csv_path, mode="a", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)

        # List all clean and degraded files
        clean_files = sorted([f for f in os.listdir(
            clean_audio_folder) if f.endswith(".wav")])
        degraded_files = sorted(
            [f for f in os.listdir(rir_folder_path) if f.endswith(".wav")])

        # Check if the number of files matches
        if len(clean_files) != len(degraded_files):
            raise ValueError(
                f"Mismatch: {len(clean_files)} clean files vs {len(degraded_files)} degraded files in {rir_folder_path}"
            )

        # Process each file pair
        for clean_file, degraded_file in zip(clean_files, degraded_files):
            clean_file_path = os.path.join(clean_audio_folder, clean_file)
            degraded_file_path = os.path.join(rir_folder_path, degraded_file)

            try:
                # Read clean and degraded audio files
                clean_signal, fs_clean = sf.read(clean_file_path)
                degraded_signal, fs_degraded = sf.read(degraded_file_path)

                # Ensure the sampling rates match
                if fs_clean != fs_degraded:
                    raise ValueError(
                        f"Sampling rates do not match for {clean_file} and {degraded_file}"
                    )

                # Pad the clean signal to match the length of the degraded signal
                if len(clean_signal) < len(degraded_signal):
                    padding = len(degraded_signal) - len(clean_signal)
                    clean_signal = np.pad(
                        clean_signal, (0, padding), mode="constant")
                elif len(clean_signal) > len(degraded_signal):
                    clean_signal = clean_signal[:len(degraded_signal)]

                # Calculate eSTOI score
                estoi_score = stoi(
                    clean_signal, degraded_signal, fs_clean, extended=True)

                # Add the subfolder name to the degraded file name
                file_record_name = f"{rir_subfolder_name}/{degraded_file}"

                # Write the score to the CSV file
                csv_writer.writerow([file_record_name, estoi_score])
                print(f"Processed {file_record_name}: eSTOI={estoi_score:.3f}")

            except Exception as e:
                # Handle errors and log them
                csv_writer.writerow([degraded_file, f"Error: {str(e)}"])
                print(f"Failed to process {degraded_file}: {e}")


def process_t60_folder(t60_folder):
    """
    Process a single T60 folder containing multiple RIR folders.
    """
    t60_folder_path = os.path.join(degraded_base_folder, t60_folder)
    output_csv_path = os.path.join(
        output_folder_path, f"{t60_folder}_estoi_scores.csv")

    # List all RIR folders within the T60 folder
    rir_folders = [
        f for f in os.listdir(t60_folder_path) if os.path.isdir(os.path.join(t60_folder_path, f))
    ]

    # Process each RIR folder
    for rir_folder in rir_folders:
        rir_folder_path = os.path.join(t60_folder_path, rir_folder)
        process_rir_folder(rir_folder_path, clean_audio_folder,
                           output_csv_path, rir_folder)


# Parallel processing for each T60 folder
Parallel(n_jobs=-1)(delayed(process_t60_folder)(folder)
                    for folder in t60_folders)

print(f"All eSTOI scores saved in {output_folder_path}")
