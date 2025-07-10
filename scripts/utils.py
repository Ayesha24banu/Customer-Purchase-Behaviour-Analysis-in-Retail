# generate_transaction_hash
import hashlib

def generate_transaction_hash(row):
    """
    Generate a safe SHA-256 hash for unique identification of transaction rows.
    """
    key = f"{row['Invoice']}_{row['StockCode']}_{row['Quantity']}_{row['Customer ID']}"
    return hashlib.sha256(key.encode()).hexdigest()