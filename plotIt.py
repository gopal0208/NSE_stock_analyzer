import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")
data_folder = "NSE_REQ"
all_data = []

# Step 1: Read and merge all CSVs
for filename in sorted(os.listdir(data_folder)):
    if filename.startswith("sec_bhavdata_full_") and filename.endswith(".csv"):
        try:
            path = os.path.join(data_folder, filename)
            df = pd.read_csv(path)

            # Standardize column names
            df.columns = [col.strip().upper() for col in df.columns]
            df = df[[  # Only keep required columns
                "SYMBOL", "DATE1", "AVG_PRICE", "DELIV_QTY", "DELIV_PER",
                "CLOSE_PRICE", "NO_OF_TRADES", "TTL_TRD_QNTY"  # original name for TTL_TRD_QUANTITY
            ]].copy()

            # Clean string columns
            for col in df.select_dtypes(include='object').columns:
                df[col] = df[col].str.strip()

            # Convert numeric fields
            for col in ["AVG_PRICE", "DELIV_QTY", "DELIV_PER", "CLOSE_PRICE", "TTL_TRD_QNTY"]:
                df[col] = pd.to_numeric(df[col], errors="coerce")

            # Add inferred date from filename
            date_str = filename[-12:-4]
            df["FILE_DATE"] = pd.to_datetime(date_str, format="%d%m%Y", errors="coerce")

            # Calculate amount = AVG_PRICE * DELIV_QTY
            df["AMOUNT"] = df["AVG_PRICE"] * df["DELIV_QTY"]

            all_data.append(df)

        except Exception as e:
            print(f"Error processing {filename}: {e}")

# Step 2: Combine all
if not all_data:
    print("No files found or could not be processed.")
    exit()

df_all = pd.concat(all_data, ignore_index=True)

# Step 3: Clean final dataset
df_all.dropna(subset=["SYMBOL", "DELIV_PER", "DELIV_QTY", "AMOUNT"], inplace=True)

# Step 4: Group by SYMBOL
summary = df_all.groupby("SYMBOL").agg({
    "DELIV_PER": "mean",
    "DELIV_QTY": "max",
    "AMOUNT": "max",
    "TTL_TRD_QNTY": "mean",
    "CLOSE_PRICE": "last",
    "FILE_DATE": "max"
}).reset_index()

summary.rename(columns={
    "DELIV_PER": "AVG_DELIV_PER",
    "DELIV_QTY": "MAX_DELIV_QTY",
    "AMOUNT": "MAX_AMOUNT",
    "TTL_TRD_QNTY": "AVG_TTL_QTY",
    "CLOSE_PRICE": "LAST_CLOSE",
    "FILE_DATE": "LAST_DATE"
}, inplace=True)

# Step 5: Define Buy Candidates
qty_thresh = summary["MAX_DELIV_QTY"].quantile(0.75)
amt_thresh = summary["MAX_AMOUNT"].quantile(0.75)

summary["BUY_CANDIDATE"] = (
    (summary["AVG_DELIV_PER"] > 50) &
    (summary["MAX_DELIV_QTY"] > qty_thresh) &
    (summary["MAX_AMOUNT"] > amt_thresh)
)

buy_list = summary[summary["BUY_CANDIDATE"]].sort_values("AVG_DELIV_PER", ascending=False)

# Step 6: Print results
print("\nTop Buy Candidates Based on Delivery Strength & Capital Inflow:\n")
if buy_list.empty:
    print("No strong buy candidates found.")
else:
    print(buy_list[[
        "SYMBOL", "AVG_DELIV_PER", "MAX_DELIV_QTY", "MAX_AMOUNT", "LAST_CLOSE", "LAST_DATE"
    ]].to_string(index=False))

# Step 7: Visualization
top_delivery = summary.sort_values("AVG_DELIV_PER", ascending=False).head(10)
top_amount = summary.sort_values("MAX_AMOUNT", ascending=False).head(10)

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
sns.barplot(data=top_delivery, x="SYMBOL", y="AVG_DELIV_PER", palette="crest")
plt.xticks(rotation=45)
plt.title("Top 10 Stocks by Avg Delivery %")

plt.subplot(1, 2, 2)
sns.barplot(data=top_amount, x="SYMBOL", y="MAX_AMOUNT", palette="magma")
plt.xticks(rotation=45)
plt.title("Top 10 Stocks by Delivery Amount ₹")

plt.tight_layout()
plt.show()

# Step 8: Smart quadrant-based decision graph

# Select top 30 stocks based on combined rank
summary["rank_score"] = summary["AVG_DELIV_PER"].rank(ascending=False) + summary["MAX_AMOUNT"].rank(ascending=False)
top30 = summary.sort_values("rank_score").head(30).copy()


top30.drop(columns=["rank_score"]).sort_values(by=["AVG_DELIV_PER", "MAX_AMOUNT"], ascending=False).to_csv(
    "nse_summary_ranked.csv", index=False
)
print("Saved top 30 ranked stocks to 'nse_summary_ranked.csv'")
median_deliv = top30["AVG_DELIV_PER"].median()
median_amt = top30["MAX_AMOUNT"].median()

plt.figure(figsize=(10, 8))
sns.scatterplot(
    data=top30, x="AVG_DELIV_PER", y="MAX_AMOUNT",
    hue="BUY_CANDIDATE", palette={True: "green", False: "red"}, s=100
)

# Add quadrant lines
plt.axhline(median_amt, color='gray', linestyle='--', label='Median Amount')
plt.axvline(median_deliv, color='gray', linestyle='--', label='Median Delivery %')

# Annotate symbols
for _, row in top30.iterrows():
    plt.text(row["AVG_DELIV_PER"] + 0.2, row["MAX_AMOUNT"], row["SYMBOL"],
             fontsize=8, alpha=0.9)

plt.title("Top 30 Stock Quadrant Decision Map")
plt.xlabel("Average Delivery %")
plt.ylabel("Max ₹ Amount Invested")
plt.legend()
plt.tight_layout()
plt.show()
