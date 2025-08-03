

"""
survival.py

Module for survival analysis and entropy computation in the UEVF pipeline.
"""

import pandas as pd
from lifelines import KaplanMeierFitter
from scipy.stats import entropy

def compute_survival_curve(df: pd.DataFrame, group_by=None, min_count=20):
    """
    Compute Kaplan–Meier survival curves.
    
    Parameters:
    - df: DataFrame with columns ['SurvivalTime', 'Event', plus grouping columns]
    - group_by: Optional column name to group curves by (e.g., 'TechType' or 'ISO')
    - min_count: Minimum records per group to compute a curve

    Returns:
    - dict mapping group labels to fitted KaplanMeierFitter objects
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

def compute_survival_entropy(df: pd.DataFrame, year_col='QueueYear', base=2):
    """
    Compute information-theoretic entropy of project survival outcomes.

    Parameters:
    - df: DataFrame with 'Event' column (1=survived, 0=failed) and 'QueueDate'
    - year_col: Column name to group by year (will extract from QueueDate if missing)
    - base: Logarithm base for entropy calculation (default base-2, bits)

    Returns:
    - DataFrame with columns ['ISO', year_col, 'SurvivalEntropy']
    """
    # Ensure year column exists
    if year_col not in df.columns:
        df[year_col] = df['QueueDate'].dt.year

    def _compute_entropy(events):
        counts = events.value_counts(normalize=True)
        return entropy(counts, base=base)

    entropy_df = (
        df
        .groupby(['ISO', year_col])['Event']
        .apply(_compute_entropy)
        .reset_index()
    )
    entropy_df.rename(columns={'Event': 'SurvivalEntropy'}, inplace=True)
    return entropy_df