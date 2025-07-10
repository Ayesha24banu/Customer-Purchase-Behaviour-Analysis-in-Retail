# scripts/data_cleaning.py

import pandas as pd
import logging
from scripts.utils import generate_transaction_hash

def load_and_clean_data(csv_path: str) -> pd.DataFrame:
    """
    Load and clean the retail dataset.

    Args:
        csv_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Cleaned dataset
    """
    try:
        logging.info(" Starting data cleaning process...")
        
        # Load dataset
        df = pd.read_csv(csv_path, encoding='ISO-8859-1')
        logging.info("Dataset loaded successfully.")

        # Drop duplicate rows
        df.drop_duplicates(inplace=True)
        logging.info(f" Removed duplicates. Rows remaining: {len(df)}")

        # Drop missing Customer ID rows
        df.dropna(subset=['Customer ID'], inplace=True)
        logging.info(f" Removed rows with missing CustomerID. Rows remaining: {len(df)}")

        # Convert Customer ID to integer
        df['Customer ID'] = df['Customer ID'].astype(int)

        # Convert InvoiceDate to datetime
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

        # Remove rows with Quantity <= 0 or Price <= 0
        df = df[(df['Quantity'] > 0) & (df['Price'] > 0)]

        # Clean whitespace in Description
        df['Description'] = df['Description'].str.strip()

        # Convert Invoice to string for consistent handling
        df['Invoice'] = df['Invoice'].astype(str)

        # Add TotalPrice column
        df['TotalPrice'] = df['Quantity'] * df['Price']

        # Add transaction hash to prevent duplicates
        df['Transaction_hash'] = df.apply(generate_transaction_hash, axis=1)

        logging.info(f"Data cleaned successfully. Shape: {df.shape}")
        return df

    except Exception as e:
        logging.error(f"Error in load_and_clean_data: {e}")
        raise
