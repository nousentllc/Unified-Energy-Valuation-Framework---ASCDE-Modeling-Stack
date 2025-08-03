"""
queue_utils.py

Utility functions for parsing and analyzing interconnection queue data:
- Loading and preprocessing raw queue CSVs
- Computing survival analysis (Kaplan–Meier)
- Estimating information-theoretic entropy of survival outcomes
"""

import pandas as pd
from lifelines import KaplanMeierFitter
from scipy.stats import entropy

def load_queue_data(path: str) -> pd.DataFrame:
    """
    Load raw queue data CSV and preprocess dates, survival time, and event flag.

    Expected CSV columns: ['ProjectID', 'ISO', 'TechType', 'QueueDate', 'CODDate', 'Status', 'Capacity', ...]
    Returns a DataFrame with added columns:
      - QueueDate (datetime)
      - CODDate (datetime)
      - SurvivalTime (int days)
      - Event (1 if operational, else 0)
    """
    df = pd.read_csv(path)
    df['QueueDate'] = pd.to_datetime(df['QueueDate'])
    df['CODDate'] = pd.to_datetime(df['CODDate'], errors='coerce')
    df['SurvivalTime'] = (df['CODDate'] - df['QueueDate']).dt.days.fillna(0).astype(int)
    df['Event'] = df['Status'].apply(
        lambda x: 1 if str(x).lower() in ['operational', 'commissioned', 'completed'] else 0
    )
    return df

def compute_survival_curve(df: pd.DataFrame, group_by: str = None, min_count: int = 20) -> dict:
    """
    Compute Kaplan–Meier survival curves.
    
    If group_by is None, returns a single KaplanMeierFitter fitted on the entire DataFrame.
    If group_by is a column name (e.g., 'TechType' or 'ISO'), returns a dict mapping group values
    to fitted KaplanMeierFitter objects (only for groups with >= min_count records).
    """
    kmf = KaplanMeierFitter()
    if group_by is None:
        kmf.fit(df['SurvivalTime'], event_observed=df['Event'], label='all')
        return {'all': kmf}
    
    curves = {}
    for name, group in df.groupby(group_by):
        if len(group) >= min_count:
            km = KaplanMeierFitter()
            km.fit(group['SurvivalTime'], event_observed=group['Event'], label=str(name))
            curves[name] = km
    return curves

def compute_survival_entropy(df: pd.DataFrame, year_col: str = 'QueueYear', base: float = 2) -> pd.DataFrame:
    """
    Compute information-theoretic entropy (in bits by default) of survival outcomes
    grouped by ISO and the specified year column (defaults to 'QueueYear').

    Returns a DataFrame with columns: ['ISO', year_col, 'SurvivalEntropy'].
    """
    if year_col not in df.columns:
        df[year_col] = df['QueueDate'].dt.year

    def _entropy(series):
        counts = series.value_counts(normalize=True)
        return entropy(counts, base=base)

    ent = df.groupby(['ISO', year_col])['Event'].apply(_entropy).reset_index()
    ent.rename(columns={'Event': 'SurvivalEntropy'}, inplace=True)
    return ent