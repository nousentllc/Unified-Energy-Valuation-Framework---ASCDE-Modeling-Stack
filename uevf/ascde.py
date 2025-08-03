"""
ascde.py

Module for ASCDE score calculation in the UEVF pipeline.
"""

import pandas as pd

def compute_ascde(queue_df: pd.DataFrame,
                  elcc_df: pd.DataFrame,
                  eue_df: pd.DataFrame,
                  voll: float) -> pd.DataFrame:
    """
    Compute ASCDE (Average System Cost of Delivered Energy) scores.

    Parameters:
    - queue_df: DataFrame containing project data, including 'ProjectID', 'ISO', 'TechType', and 'Capacity'.
    - elcc_df: DataFrame with 'ISO', 'TechType', and 'AdjustedELCC' columns.
    - eue_df: DataFrame with 'ProjectID' and 'EUE' columns.
    - voll: Value of Lost Load ($/MWh).

    Returns:
    - DataFrame with original queue_df columns plus an 'ASCDE' column.
    """
    # Merge ELCC values into queue
    merged = queue_df.merge(
        elcc_df[['ISO', 'TechType', 'AdjustedELCC']],
        on=['ISO', 'TechType'],
        how='left'
    )
    # Merge EUE values
    merged = merged.merge(
        eue_df[['ProjectID', 'EUE']],
        on='ProjectID',
        how='left'
    )
    # Calculate ASCDE = EUE * VOLL / (Capacity * AdjustedELCC)
    merged['ASCDE'] = merged['EUE'] * voll / (merged['Capacity'] * merged['AdjustedELCC'])
    return merged