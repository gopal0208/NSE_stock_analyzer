# NSE Stock Analyzer

This project processes raw NSE Bhavcopy data and analyzes delivery-based stock metrics to identify strong buy candidates using capital flow and delivery percentage.
Also to get updated results, go to NSE website: `https://www.nseindia.com/all-reports`>archives>download `Full Bhavcopy and Security Deliverable Data`> store it in NSE folder.

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
## Column Selection and Plot Justification

### processNSE.py – Why Specific Columns Were Chosen

The following columns were selected for processing each NSE file due to their relevance in identifying potential stock investments based on delivery and price metrics:

- `SYMBOL`: Identifies the stock uniquely.
- `DATE1`: Helps track the stock data over time.
- `AVG_PRICE`: Represents the average traded price, useful for computing actual money flow.
- `DELIV_QTY`: Shows how much quantity was actually delivered (not intraday), indicating serious investors.
- `DELIV_PER`: Percentage of total traded quantity that was delivered. A high value often signals accumulation by strong hands.
- `CLOSE_PRICE`: Reflects the final trading price of the day, giving context to market sentiment.
- `NO_OF_TRADES`: Provides insight into trading activity.
- `TTL_TRD_QNTY`: Total quantity traded; used in evaluating demand and delivery against total volume.
- `TURNOVER_LACS`: Monetary value of trades; used for understanding capital movement.
- `amount` (derived): A calculated field from `AVG_PRICE * DELIV_QTY`, used to measure the actual rupee value of delivered stock.

Columns like `OPEN_PRICE`, `HIGH_PRICE`, and `LOW_PRICE` were excluded as they don't strongly indicate delivery-based accumulation or investor seriousness.

---

### plotIt.py – Why Two Plots Were Shown

Two main plots were chosen in the visualization phase:

1. **Top 10 Stocks by Avg Delivery %**:
   - Helps identify stocks with consistently high delivery ratios, which can indicate accumulation or investor confidence.

2. **Top 10 Stocks by Max ₹ Amount Invested**:
   - Shows which stocks had the most capital flow through delivery, giving an idea of where institutional money might be flowing.

Both metrics (delivery % and amount) are powerful when combined, and thus:

### Quadrant Plot (Smart Summary Visualization)

A third visualization was added as a decision-making quadrant chart to analyze the **top 30 stocks** based on combined delivery % and amount invested. This helps investors visually identify stocks that lie in the high delivery–high amount quadrant, making them prime buy candidates.

Other metrics like `NO_OF_TRADES` or `TURNOVER_LACS` were not directly plotted as they are less reliable independently in making strong buy decisions compared to the delivery-focused metrics.