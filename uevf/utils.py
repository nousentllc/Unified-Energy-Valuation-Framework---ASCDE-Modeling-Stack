

"""
utils.py

Helper functions for I/O operations in the UEVF pipeline.
"""

import pandas as pd
import os

def load_csv(path: str, parse_dates=None) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.
    
    Parameters:
    - path: Path to the CSV file.
    - parse_dates: List of column names to parse as dates.
    
    Returns:
    - DataFrame containing the CSV data.
    """
    return pd.read_csv(path, parse_dates=parse_dates)

def save_dataframe(df: pd.DataFrame, path: str):
    """
    Save a pandas DataFrame to CSV, creating directories if needed.
    
    Parameters:
    - df: DataFrame to save.
    - path: Output CSV file path.
    """
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    df.to_csv(path, index=False)