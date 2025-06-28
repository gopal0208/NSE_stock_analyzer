# NSE Stock Analyzer

This project processes raw NSE Bhavcopy data and analyzes delivery-based stock metrics to identify strong buy candidates using capital flow and delivery percentage.

## Folder Structure

```
.
├── NSE/                   # Raw bhavcopy CSV files (e.g., sec_bhavdata_full_ddmmyyyy.csv)
├── NSE_REQ/               # Cleaned and processed data files
├── processNSE.py          # Script to extract, clean, and store essential data
├── plotIt.py              # Script to analyze, summarize and visualize stock performance
├── setup_env.bat          # Windows batch file to setup Python environment and install packages
├── run_analysis.bat       # Windows batch file to run both scripts
├── setup_env.sh           # Linux/macOS shell script to setup Python environment and install packages
├── run_analysis.sh        # Linux/macOS shell script to run both scripts
├── nse_summary_ranked.csv # Final CSV with top 30 buy candidates based on metrics
└── README.md              # Project instructions and documentation
```

## Setup Instructions

### Windows

1. Run the setup script to create the virtual environment and install required libraries:
   ```
   setup_env.bat
   ```

2. After setup, run the full analysis pipeline:
   ```
   run_analysis.bat
   ```

### macOS / Linux

1. Make the shell scripts executable:
   ```
   chmod +x setup_env.sh run_analysis.sh
   ```

2. Run the setup script:
   ```
   ./setup_env.sh
   ```

3. Run the analysis pipeline:
   ```
   ./run_analysis.sh
   ```

## Scripts Overview

### processNSE.py

- Reads all files from the `NSE/` folder with names like `sec_bhavdata_full_ddmmyyyy.csv`.
- Filters rows where `SERIES == 'EQ'`.
- Computes an `amount` column as `AVG_PRICE * DELIV_QTY`.
- Selects relevant columns and saves to the `NSE_REQ/` folder.

### plotIt.py

- Aggregates all processed files in `NSE_REQ/`.
- Computes mean delivery percentage, max delivery quantity and amount.
- Identifies potential buy candidates using threshold-based filtering.
- Generates two bar plots (top 10 delivery %, top 10 amount).
- Saves top 30 stocks by delivery strength + capital inflow to `nse_summary_ranked.csv`.
- Generates a quadrant scatter plot to visualize final buy decision candidates.

## Output

- `nse_summary_ranked.csv` — A ranked list of top 30 buy candidates with delivery statistics.
- Graphs showing delivery behavior and capital involvement across shortlisted stocks.

## Requirements

- Python 3.8+
- Libraries: `pandas`, `matplotlib`, `seaborn`

These are installed via the setup scripts.