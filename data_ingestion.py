"""
PLTR Stock Data Ingestion Script
===============================

This script loads PLTR (Palantir) stock data from a CSV file and stores it
in a SQLite database for use by the Flask API.

The CSV file contains historical stock data with OHLCV (Open, High, Low, Close, Volume)
information from September 30, 2020 to September 9, 2025.

Author: [Your Name]
Date: [Current Date]
Version: 1.0.0

Dependencies:
- pandas: Data manipulation and analysis
- sqlalchemy: Database connectivity and ORM

Usage:
    python data_ingestion.py

Note:
    This script will replace any existing 'stocks' table in the database.
    Make sure to backup your data if needed before running this script.
"""

import pandas as pd
from sqlalchemy import create_engine

# Load PLTR stock data from CSV file
# The CSV contains historical stock data with columns: date, open, high, low, close, adj_close, volume
print("Loading PLTR stock data from CSV file...")
df = pd.read_csv('Datasets/PLTR_2020-09-30_2025-09-09.csv')

# Display basic information about the loaded data
print(f"Data loaded successfully!")
print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
print(f"Columns: {list(df.columns)}")

# Create SQLite database connection using SQLAlchemy
# echo=True enables SQL query logging for debugging purposes
print("\nConnecting to SQLite database...")
engine = create_engine('sqlite:///pltr.db', echo=True)

# Ingest data into the 'stocks' table
# if_exists='replace' will drop and recreate the table if it already exists
# index=False prevents pandas from writing row indices to the database
print("Ingesting data into database...")
df.to_sql('stocks', con=engine, if_exists='replace', index=False)

print("Data ingestion completed successfully!")
print("The 'stocks' table has been created/updated in pltr.db")
print("You can now run the Flask API server using: python routes.py")
