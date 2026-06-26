# Second Task
# "I tested the dataset yesterday, but I accidentally introduced some data problems. 
# Some values are missing, some numeric columns have text, a few timestamps are invalid, and some symbols have inconsistent formatting. 
# This happens more often than we like to admit. Can you clean it properly?"

# This task requires building a data cleaning script with five core components:
# 1) Categorical String Normalization: Fix inconsistent formatting in the symbol column by stripping whitespace and enforcing uppercase standardization.
# 2) Data Type Validation & Parsing: Cast numeric columns like open, high, low, close, and volumes to floats, and trade counts to integers, handling corrupted text anomalies safely.
# 3) Timestamp Verification: Validate Unix/millisecond open and close timestamps, removing entries with negative, mathematically impossible, or missing chronological data.
# 4) Missing Value Management: Locate and handle null or NaN fields across the dataset using an appropriate dropping or imputation strategy to preserve time-series continuity.
# 5) Verification & Audit Logging: Export the clean data, verify the final structural metrics, and log the exact number of rows modified or dropped for troubleshooting.

# part2_clean_with_pandas.py
# Team 2: Data Quality (25 marks)
# Loads Dara's messy dataset, find the problems, clean the data, and save a reliable cleaned CSV for the Analytics team. 
# You will do a small balanced pandas analysis on only 50 records, but this is just a sample check. 
# It is not the final analytics section.

import pandas as pd
import numpy as np
from pathlib import Path
import os

# Setup directories 
messy_path = Path("data/messy/messy_market_data.csv")
clean_path = Path("data/clean/cleaned_market_data.csv")

# Easy tasks

# 1. Load data/messy/messy_market_data.csv with pandas, print the number of rows and columns, show the first 10 rows, and print the data types of all columns. 
# This proves that you are using the messy file created by Dara's script and helps you identify columns that are stored as text even though they should be numbers or timestamps. 
# 3 marks

# Example output:
# Loaded data/messy/messy_market_data.csv
# Rows: 9991
# Columns: 13
# First 10 rows shown
# symbol        object
# open_time     object
# open          object
# close         object
# trade_count   object

# Load data/messy/messy_market_data.csv with pandas
print(f"Loaded data/messy/messy_market_data.csv")
df = pd.read_csv(messy_path)
# Print the number of rows and columns
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")
# Show the first 10 rows
print("First 10 rows:")
print(df.head(10).to_string()) # Used Gemini here as print(df.head(10)) was showing [10 rows x 8 columns]
# Print the data types of all columns. 
print(f"\nColumn data types:")
print(df.dtypes)

# 2. Count missing values for every column and identify which columns have the most missing data. 
# Do not only show the total number of missing values; explain which columns are most affected. 
# 2 marks

# Example output:
# Missing values:
# close_time        58
# high              57
# quote_volume      51
# Most affected column: close_time

# Count missing values for every column 
print(f"\nMissing values:")
missing_value_count = df.isnull().sum()
print(missing_value_count[missing_value_count > 0]) #Gemini helped refine - originally just print(missing_value_count)
# Identify which columns have the most missing data. 
print(f"Most affected column: {df.isnull().sum().idxmax()}") 

# Medium tasks

# 3. Convert all price, volume, and trade-count columns to numeric data types using safe conversion. 
# If a value such as unknown, error, or an empty cell cannot become a number, mark it as invalid/missing so it can be handled later. 
# 2 marks

# Example output:
# Converted numeric columns:
# open, high, low, close, volume, quote_volume, trade_count
# Invalid numeric rows after conversion: 769

# Convert all price, volume, and trade-count columns to numeric data types.
available_numeric = ["open", "high", "low", "close", "volume", "quote_volume", "trade_count"]
numeric_cols = [col for col in available_numeric if col in df.columns]
print(f"\nConverted numeric columns:")
print(", ".join(numeric_cols))

# If a value such as unknown, error, or an empty cell cannot become a number, mark as invalid. 
pre_invalid_removal_numeric = df[numeric_cols].isna().sum().sum()
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')
post_invalid_removal_numeric = df[numeric_cols].isna().sum().sum()
new_invalid_numeric = post_invalid_removal_numeric - pre_invalid_removal_numeric
invalid_numeric_rows_count = df[numeric_cols].isna().any(axis=1).sum()
print(f"Invalid numeric rows after conversion: {invalid_numeric_rows_count}")

"""
Development Note: Resolved a KeyError crash caused by structural schema variations 
in the messy input file (missing 'quote_volume' and 'trade_count' columns). 
Refactored with AI assistance (Gemini) to implement a dynamic list comprehension 
([col for col in numeric_cols if col in df.columns]) that automatically aligns the 
data-cleansing loop with the columns present on disk. This preserves full multi-column 
'errors=coerce' data type validation without letting structural omissions break the 
ingestion pipeline.
"""

# 4. Convert open_time and close_time to timestamp values, detect invalid dates, and clean the symbol column. 
# Valid timestamps should become real date/time values; invalid values such as not_a_date should be counted as invalid. 
# Symbol values such as btcusdt, BTCUSDT, and BTC/USDT should become BTCUSDT. 
# 4 marks

# Example output:
# Converted timestamp columns:
# open_time, close_time
# Invalid open_time values: 205
# Invalid close_time values: 197
# Symbols before cleaning: btcusdt,  BTCUSDT , BTC/USDT
# Symbols after cleaning: BTCUSDT
# Unique cleaned symbols: 10


# Convert open_time and close_time to timestamp values
print(f"\nConverted timestamp columns:")
timestamp_cols = ["open_time", "close_time"]
print(", ".join(timestamp_cols)) # Gemini enhanced, previously just print(f"open_time, close_time")

# Valid timestamps should become real date/time values
df["open_time"] = pd.to_numeric(df["open_time"], errors='coerce') # Gemini FIX: Force columns to numeric values first so unit='ms' can read them
df["close_time"] = pd.to_numeric(df["close_time"], errors='coerce') # Gemini FIX: Force columns to numeric values first so unit='ms' can read them
df["open_time"] = pd.to_datetime(df["open_time"], unit='ms', errors='coerce')
df["close_time"] = pd.to_datetime(df["close_time"], unit='ms', errors='coerce')

# Detect invalid dates
# Invalid values such as not_a_date should be counted as invalid. 
invalid_open = df["open_time"].isna().sum()
invalid_close = df["close_time"].isna().sum()

print(f"Invalid open_time values: {invalid_open}")
print(f"Invalid close_time values: {invalid_close}")

# Clean the symbol column.
# Symbol values such as btcusdt, BTCUSDT, and BTC/USDT should become BTCUSDT.
symbols_before = df["symbol"].dropna().unique()
before_sample = ",  ".join(list(symbols_before)[:3])
print(f"Symbols before cleaning: {before_sample}")

df["symbol"] = df["symbol"].astype(str).str.upper().str.strip().str.replace("/", "", regex=False)

symbols_after = df["symbol"].unique()
print(f"Symbols after cleaning: {symbols_after}")
print(f"Unique cleaned symbols: {len(symbols_after)}")

# Hard tasks

# 5. Find and remove duplicated rows. 
# Explain how many duplicates were found before you removed them, and 
# make sure the cleaned dataset does not count the same market candle more than once. 
# 2 marks

# Example output:
# Duplicate rows found: 213
# Rows before removing duplicates: 9991
# Rows after removing duplicates: 9778

# Find and remove duplicated rows. 
duplicate_count = df.duplicated().sum()
print(f"\nDuplicate rows found: {duplicate_count}")
# Explain how many duplicates were found before removed
rows_before = df.shape[0]
print(f"Rows before removing duplicates: {rows_before}")
df = df.drop_duplicates() # Gemini fix, reassigned to df so changes stick 
rows_after = df.shape[0]
print(f"Rows before removing duplicates: {rows_after}")
# Cleaned dataset does not count the same market candle more than once


# 6. Detect impossible numeric values, such as negative volume, negative trade count, or high lower than low. Explain which rules you used to decide that a row was invalid. 
# 2 marks

# Example output:
# Negative volume rows: 299
# Negative trade_count rows: 0
# Rows where high < low: 0
# Invalid numeric rows total: 769

# Detect impossible numeric values:
# Negative volume
negative_volume = df["volume"] < 0
print(f"\nNegative volume rows: {negative_volume.sum()}")
# Ngative trade count
    # Enhanced with Gemini, safely checked only if the column exists 
    # previously just negative_trade_count = df["trade_count"] < 0
if "trade_count" in df.columns:
    negative_trade_count = df["trade_count"] < 0
else:
    negative_trade_count = pd.Series(False, index=df.index) 
print(f"Negative trade_count rows: {negative_trade_count.sum()}")
# High lower than low
high_lower_than_low = df["high"] < df["low"]
print(f"Rows where high < low: {high_lower_than_low.sum()}")
# Explain which rules you used to decide that a row was invalid.
    # 1. Volume/trade_count cannot be less than zero.
    # 2. Ceiling price boundary (high) cannot be less than the floor price boundary (low).
    # 3. Any key numeric metric contains a structural missing indicator (NaN/NaT).
missing_value = df[["open", "high", "low", "close", "volume"]].isna().any(axis=1) # Flagged by Gemini, previously just the first two rules considered
invalid_rows_total =  (
    negative_volume | 
    negative_trade_count | 
    high_lower_than_low | 
    missing_value
).sum()
print(f"Invalid numeric rows total: {invalid_rows_total}")

# 7. Create price_range, price_change, percent_change, and candle_direction so the cleaned dataset is ready for checking and later analytics. Calculate price_range as high - low, price_change as close - open, and percent_change as (price_change / open) * 100. Set candle_direction to up when close is greater than open, down when close is lower than open, and flat when they are equal. 
# 3 marks

# Example output:
# Created columns:
# price_range, price_change, percent_change, candle_direction
# Example row:
# open=100.00 close=105.00 high=110.00 low=95.00
# price_range=15.00 price_change=5.00 percent_change=5.00 candle_direction=up

# Create price_range, price_change, percent_change, and candle_direction 
created_columns = ["price_range", "price_change", "percent_change", "candle_direction"]
print(f"\nCreated columns:")
print(f", ".join(created_columns))
# Calculate price_range as high - low
df["price_range"] = df["high"] - df["low"]
# Calculate price_change as close - open
df["price_change"] = df["close"] - df["open"]
# Calculate  percent_change as (price_change / open) * 100. 
df["percent_change"] = (df["price_change"] / df["open"]) * 100
# Set candle_direction to up when close is greater than open, down when close is lower than open, and flat when they are equal. 
df["candle_direction"] = [
    "up" if close > open else "down" if close < open else "flat"
    for open, close in zip(df["open"], df["close"])
]

# Very hard task


# 8. Build a before/after data-quality report with row counts, missing values, invalid numeric values, invalid timestamps, duplicates, rows removed or repaired, and a short paragraph explaining the cleaning decisions. The report should make it clear what changed between the messy dataset and the cleaned dataset. 
# 4 marks

# Example output:
# Data-quality report
# Rows before cleaning: 9991
# Rows after cleaning: 8364
# Missing values before: 496
# Missing values after: 0
# Duplicate rows before: 213
# Duplicate rows after: 0
# Cleaning decision: invalid rows were removed because ...

# Save the cleaned dataset as:
# data/clean/cleaned_market_data.csv

# Build a before/after data-quality report
df_clean = df.dropna().copy() 

#Below section added using Gemini
# Refactored cleaning step: .dropna() only removes structural missing data (NaN/NaT).
# Added explicit filters to remove semantic errors (like negative volumes) 
# that .dropna() misses, bringing "Invalid numeric values after" down to a clean 0.
df_clean = df_clean[df_clean["volume"] >= 0]
if "trade_count" in df_clean.columns:
    df_clean = df_clean[df_clean["trade_count"] >= 0]
df_clean = df_clean[df_clean["high"] >= df_clean["low"]]

print(f"\nData-quality report:")
# Row counts 
print(f"Rows before cleaning: {rows_before}")
print(f"Rows after cleaning: {df_clean.shape[0]}")
# Missing values
print(f"Missing values before: {missing_value.sum()}")
print(f"Missing values after: {df_clean.isnull().sum().sum()}")
# Invalid numeric values
print(f"Invalid numeric values before: {invalid_rows_total}")
clean_neg_vol = (df_clean["volume"] < 0).sum()
clean_neg_trade = (df_clean["trade_count"] < 0).sum() if "trade_count" in df_clean.columns else 0
clean_high_low = (df_clean["high"] < df_clean["low"]).sum()
print(f"Invalid numeric values after: {clean_neg_vol + clean_neg_trade + clean_high_low}")
# Invalid timestamps
print(f"Invalid timestamps before: {invalid_open + invalid_close}")
print(f"Invalid timestamps after: {df_clean['open_time'].isna().sum() + df_clean['close_time'].isna().sum()}")
# Duplicates
print(f"Duplicate rows before: {duplicate_count}")
print(f"Duplicate rows after: {df_clean.duplicated().sum()}")
# Short paragraph explaining the cleaning decisions. 
# The report should make it clear what changed between the messy dataset and the cleaned dataset. 
print("Cleaning decision: Invalid rows were removed because it contains impossible values (like negative volumes), text errors, (like unknown or not a date), and duplicate entries. "
    "These errors break data integrity, so converting them into missing values and dropping them ensures the dataset contains only realistic, "
    "and unique market data that won't distort our final analysis.")
# Save the cleaned dataset as: data/clean/cleaned_market_data.csv
output_dir = "data/clean"
os.makedirs(output_dir, exist_ok=True)
clean_path = os.path.join(output_dir, "cleaned_market_data.csv")
df_clean.to_csv(clean_path, index=False)
print(f"Cleaned dataset saved to: {clean_path}")

# SAMPLE CHECK
# 3 marks

# Dara warns you:
# "Do not do the final analysis in pandas. 
# Use pandas to inspect and test a small sample only. 
# The analytics team will use Spark for the full dataset."

# Use only a random sample of 50 records for the pandas analytics section.
# The sample must include data from all 10 symbols. Use 5 random records from each symbol:
# 10 symbols x 5 random records = 50 sample records
df_sample = df_clean.groupby("symbol").sample(n=5, random_state=42)
sample_rows = df_sample.shape[0]
unique_symbols = df_sample["symbol"].nunique()
records_per_symbol = df_sample.groupby("symbol").size().iloc[0]

# On the 50-record sample, answer at least three simple questions:
# 1. What is the average close price by symbol?
avg_close = df_sample.groupby("symbol")["close"].mean()
# 2. Which symbol has the highest average volume?
highest_vol_symbol = df_sample.groupby("symbol")["volume"].mean().idxmax()
# 3. How many candles went up or down?
direction_counts = df_sample["candle_direction"].value_counts()
# 4. Which row has the largest price range?
largest_range_idx = df_sample["price_range"].idxmax()
largest_range_row = df_sample.loc[largest_range_idx]

# Save the sample result as:
# results/pandas_sample_results.csv
os.makedirs("results", exist_ok=True)
sample_results_path = "results/pandas_sample_results.csv"
results_df = pd.DataFrame({
    "Metric": [
        "Sample rows used", 
        "Symbols included", 
        "Records per symbol", 
        "Questions answered"
    ],
    "Value": [
        sample_rows, 
        unique_symbols, 
        records_per_symbol, 
        4
    ]
})
results_df.to_csv(sample_results_path, index=False)

# Example sample result:
# Average close price by symbol:
# BTCUSDT: 108921.44
# ETHUSDT: 2647.82

# Highest average volume:
# XRPUSDT

# Candle direction counts:
# up: 27
# down: 22
# flat: 1

# Sample requirement A: Answer at least three sample-analysis questions using only 50 records and save results/pandas_sample_results.csv. 2 marks

# Example output:
# Saved results/pandas_sample_results.csv
# Sample rows used: 50
# Symbols included: 10
# Records per symbol: 5
# Questions answered: 3

print(f"\nSaved {sample_results_path}")
print(f"Sample rows used: {sample_rows}")
print(f"Symbols included: {unique_symbols}")
print(f"Records per symbol: {records_per_symbol}")
print(f"Questions answered: 4\n")

print("Average close price by symbol:")
for symbol, price in avg_close.items():
    print(f"  {symbol}: {price:.2f}")

print(f"\nHighest average volume:\n  {highest_vol_symbol}")

print(f"\nCandle direction counts:")
print(f"  up: {direction_counts.get('up', 0)}")
print(f"  down: {direction_counts.get('down', 0)}")
print(f"  flat: {direction_counts.get('flat', 0)}")

print(f"\nLargest price range:")
print(f"  Symbol: {largest_range_row['symbol']}")
print(f"  Range Spread: {largest_range_row['price_range']:.4f}")

# Explain why pandas is useful for checking and cleaning data, but why a 50-record sample is not enough for final analytics.

# Sample requirement B: Explain why pandas is useful for checking and cleaning, but not enough for final full-dataset analytics. 1 mark
"""
Pandas loads data into memory, so it works well for inspecting, filtering, and cleaning datasets interactively. However, it struggles with datasets larger than available RAM. 
For full-dataset analytics at scale, tools like Spark, Dask, or SQL engines are needed instead
"""