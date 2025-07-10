import mysql.connector
import pandas as pd 
import logging
from datetime import datetime

def store_to_mysql(df, config: dict, mode: str = 'append', backup: bool = True):
    """
    Store cleaned DataFrame into MySQL and create DB/table if not exist.

    Args:
        df (pd.DataFrame): Cleaned data
        config (dict): MySQL connection config
        mode (str): 'append' (default) or 'replace'
        backup (bool): Whether to create a backup table
    """
    try:
        # Ensure database exists
        db_name = config['database']
        base_config = config.copy()
        del base_config['database']  # used for initial connection without selecting DB

        # Step 1: Connect without selecting DB
        conn = mysql.connector.connect(**base_config)
        cursor = conn.cursor()

        # Step 2: Create database if not exists
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        logging.info(f" Database '{db_name}' created (if it didn't exist).")
        cursor.close()
        conn.close()
        
        # Step 3: Reconnect using selected DB
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Step 4: Create table if not exists
        table_name = "cleaned_sales_data"
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            Transaction_hash VARCHAR(64) PRIMARY KEY,
            Invoice VARCHAR(20),
            StockCode VARCHAR(20),
            Description TEXT,
            Quantity INT,
            InvoiceDate DATETIME,
            Price FLOAT,
            CustomerID INT,
            Country VARCHAR(50),
            TotalPrice FLOAT
        )
        """)
        logging.info(f" Table '{table_name}' checked/created.")

        # Optional: clear existing rows if mode is 'replace'
        if mode == 'replace':
            cursor.execute(f"DELETE FROM {table_name}")
            conn.commit()
            logging.info(f"Data in '{table_name}' deleted (mode='replace').")

        # Step 5: Count before insert
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        before_insert = cursor.fetchone()[0]
        
        # Step 6: Insert rows
        insert_query = f"""
        INSERT IGNORE INTO {table_name} (
            Transaction_hash, Invoice, StockCode, Description, Quantity,
            InvoiceDate, Price, CustomerID, Country, TotalPrice
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # iterates over each row in the DataFrame df, and inserts it into a MySQL table row-by-row 
        for _, row in df.iterrows():
            cursor.execute(insert_query, (
                row["Transaction_hash"], row["Invoice"], row["StockCode"], row["Description"],
                int(row["Quantity"]), row["InvoiceDate"].to_pydatetime(),
                float(row["Price"]), int(row["Customer ID"]),
                row["Country"], float(row["TotalPrice"])
            ))
        conn.commit()

        # Step 7: Count after insert
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        after_insert = cursor.fetchone()[0]
        inserted_count = after_insert - before_insert

        
        #checking the inserted rows 
        if inserted_count > 0:
            logging.info(f" {inserted_count} new rows inserted into '{table_name}'.")
            print(f" {inserted_count} new rows inserted into MySQL.")

        # Step 8: Optional backup
        if backup:
            backup_table = f"{table_name}_backup"

            # Drop old backup table if it exists
            cursor.execute(f"DROP TABLE IF EXISTS {backup_table}")
            logging.info(" Old backup table dropped.")

            # Create new backup from main table
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {backup_table}
                AS SELECT * FROM {table_name}
            """)
            conn.commit()
            logging.info(f" Backup table '{backup_table}' updated.")
            print(f" Backup table '{backup_table}' updated.")
        else:
            print(" No new data inserted. Skipped backup.")
            logging.info("No data inserted. Backup skipped.")

        # Step 7: Cleanup
        cursor.close()
        conn.close()
        logging.info("MySQL connection closed.")

    except Exception as e:
        logging.error(f"MySQL storage failed: {e}")
        raise

def read_clean_data(config: dict, table: str = 'cleaned_sales_data') -> pd.DataFrame:
    """
    Load cleaned data back from MySQL for analysis.

    Args:
        config (dict): MySQL config
        table(str): 'cleaned_sales_data'

    Returns:
        pd.DataFrame: Cleaned data
    """
    conn = mysql.connector.connect(**config)
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    conn.close()
    return df
