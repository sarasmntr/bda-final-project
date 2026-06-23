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

# Setup directories 

# Easy tasks

# 1. Load data/messy/messy_market_data.csv with pandas, print the number of rows and columns, show the first 10 rows, and print the data types of all columns. This proves that you are using the messy file created by Dara's script and helps you identify columns that are stored as text even though they should be numbers or timestamps. 
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


# 2. Count missing values for every column and identify which columns have the most missing data. Do not only show the total number of missing values; explain which columns are most affected. 
# 2 marks

# Example output:
# Missing values:
# close_time        58
# high              57
# quote_volume      51
# Most affected column: close_time


# Medium tasks

# 3. Convert all price, volume, and trade-count columns to numeric data types using safe conversion. If a value such as unknown, error, or an empty cell cannot become a number, mark it as invalid/missing so it can be handled later. 
# 2 marks

# Example output:
# Converted numeric columns:
# open, high, low, close, volume, quote_volume, trade_count
# Invalid numeric rows after conversion: 769

# 4. Convert open_time and close_time to timestamp values, detect invalid dates, and clean the symbol column. Valid timestamps should become real date/time values; invalid values such as not_a_date should be counted as invalid. Symbol values such as btcusdt, BTCUSDT, and BTC/USDT should become BTCUSDT. 
# 4 marks

# Example output:
# Converted timestamp columns:
# open_time, close_time
# Invalid open_time values: 205
# Invalid close_time values: 197
# Symbols before cleaning: btcusdt,  BTCUSDT , BTC/USDT
# Symbols after cleaning: BTCUSDT
# Unique cleaned symbols: 10


# Hard tasks

# 5. Find and remove duplicated rows. Explain how many duplicates were found before you removed them, and make sure the cleaned dataset does not count the same market candle more than once. 
# 2 marks

# Example output:
# Duplicate rows found: 213
# Rows before removing duplicates: 9991
# Rows after removing duplicates: 9778


# 6. Detect impossible numeric values, such as negative volume, negative trade count, or high lower than low. Explain which rules you used to decide that a row was invalid. 
# 2 marks

# Example output:
# Negative volume rows: 299
# Negative trade_count rows: 0
# Rows where high < low: 0
# Invalid numeric rows total: 769


# 7. Create price_range, price_change, percent_change, and candle_direction so the cleaned dataset is ready for checking and later analytics. Calculate price_range as high - low, price_change as close - open, and percent_change as (price_change / open) * 100. Set candle_direction to up when close is greater than open, down when close is lower than open, and flat when they are equal. 
# 3 marks

# Example output:
# Created columns:
# price_range, price_change, percent_change, candle_direction
# Example row:
# open=100.00 close=105.00 high=110.00 low=95.00
# price_range=15.00 price_change=5.00 percent_change=5.00 candle_direction=up

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

# Dara warns you:
# "Do not do the final analysis in pandas. 
# Use pandas to inspect and test a small sample only. 
# The analytics team will use Spark for the full dataset."

# Use only a random sample of 50 records for the pandas analytics section.

# The sample must include data from all 10 symbols. Use 5 random records from each symbol:
# 10 symbols x 5 random records = 50 sample records

# Create a stratified sample of exactly 5 random records from each of the 10 symbols

# On the 50-record sample, answer at least three simple questions:
# What is the average close price by symbol?
# Which symbol has the highest average volume?
# How many candles went up or down?
# Which row has the largest price range?

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

# These sample answers are only a quick quality check. Team 3 will use Spark to extend this work with full-dataset rankings, time-based activity analysis, and a final market summary.

# Save the sample result as:
# results/pandas_sample_results.csv


# Explain why pandas is useful for checking and cleaning data, but why a 50-record sample is not enough for final analytics.

# This sample check is worth 3 marks.

# Sample requirement A: Answer at least three sample-analysis questions using only 50 records and save results/pandas_sample_results.csv. 2 marks

# Example output:
# Saved results/pandas_sample_results.csv
# Sample rows used: 50
# Symbols included: 10
# Records per symbol: 5
# Questions answered: 3

# Sample requirement B: Explain why pandas is useful for checking and cleaning, but not enough for final full-dataset analytics. 1 mark
