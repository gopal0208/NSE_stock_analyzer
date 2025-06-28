import os
import pandas as pd

source_folder = "NSE"
output_folder = "NSE_REQ"
symbol_set = set()

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(source_folder):
    if filename.startswith("sec_bhavdata_full_") and filename.endswith(".csv"):
        input_path = os.path.join(source_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # Skip if already processed
        if os.path.exists(output_path):
            print(f"Skipping (already processed): {filename}")
            continue

        try:
            df = pd.read_csv(input_path, skip_blank_lines=True)

            # Clean column names
            df.columns = [col.strip().upper() for col in df.columns]

            # Clean string values
            for col in df.select_dtypes(include='object').columns:
                df[col] = df[col].str.strip()

            if 'SERIES' not in df.columns:
                print(f"⚠️ Skipping {filename}: 'SERIES' column missing.")
                continue

            df_eq = df[df['SERIES'] == 'EQ'].copy()

            for col in ['AVG_PRICE', 'DELIV_QTY']:
                if col in df_eq.columns:
                    df_eq[col] = pd.to_numeric(df_eq[col], errors='coerce')

            df_eq = df_eq.dropna(subset=['AVG_PRICE', 'DELIV_QTY'])

            df_eq['amount'] = df_eq['AVG_PRICE'] * df_eq['DELIV_QTY']

            selected_cols = [
                'SYMBOL', 'DATE1', 'AVG_PRICE', 'DELIV_QTY',
                'DELIV_PER', 'CLOSE_PRICE', 'NO_OF_TRADES',
                'TTL_TRD_QNTY', 'TURNOVER_LACS', 'amount'
            ]
            selected_cols = [col for col in selected_cols if col in df_eq.columns]

            df_final = df_eq[selected_cols]

            # Collect unique symbols
            symbol_set.update(df_eq['SYMBOL'].unique())

            # Save to NSE_REQ
            df_final.to_csv(output_path, index=False)
            print(f"Processed: {filename}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

# Save all collected symbols to symbol_list.csv in the current directory
if symbol_set:
    symbol_df = pd.DataFrame(sorted(symbol_set), columns=["SYMBOL"])
    symbol_df.to_csv("symbol_list.csv", index=False)
    print(f"Saved {len(symbol_set)} unique symbols to symbol_list.csv")
else:
    print("No symbols found to save.")
