# CSE3000
This repository contains scripts and data related to CSE3000. The project structure is organized as follows:

## Folder Structure
```
├── README.md          # Project documentation
├── src/               # Source code for intelligibility analysis
│   ├── cal_kendall.py          # Script to calculate Kendall's Tau correlation
│   ├── scatter_plot.py         # Script for generating scatter plots
│   ├── get_estoi.py            # Script to compute ESTOI scores
│   ├── get_siib.py             # Script to compute SIIB scores
│   ├── std_deviation_plot.py   # Script to generate standard deviation plots
│   ├── variance_test.py        # Script for variance testing
│   ├── cal_stipa_scores.m      # MATLAB script for STIPA score calculations
│   ├── get_test_signals.m      # MATLAB script to obtain test signals
│
├── csv_files/         # Contains CSV data files
│   ├── raw_scores/          # Raw score data
│   ├── mean_scores/         # Processed mean score data
│   ├── at_zero/             # Data recorded at zero reverberation condition
│   ├── Leven's_results/     # Levene's test results for variance analysis
```

## Setup and Dependencies
Ensure you have Python installed along with the following libraries:
```bash
pip install numpy pandas matplotlib scipy seaborn
```
If you need to run MATLAB scripts, ensure MATLAB is installed.

### Additional Dependencies
- For STIPA, the MATLAB library is required: [STIPA MATLAB Library](https://github.com/zawi01/stipa)
- For SIIB, install using:
  ```bash
  pip install git+https://github.com/kamo-naoyuki/pySIIB.git
  ```
- For ESTOI, install using:
  ```bash
  pip install pystoi
  ```
- For HASPI, install using:
  ```bash
  pip install pyclarity
  ```

## Usage
- Python and MATLAB scripts in `src/` are used for intelligibility calculations and visualizations.
- CSV files in `csv_files/` store the scores and results of this project.

## License
This project is open-source and licensed under the MIT License.
