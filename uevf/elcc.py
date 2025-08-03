"""
elcc.py

Module for Effective Load Carrying Capability (ELCC) calculations.
"""

import pandas as pd
import numpy as np

def compute_baseline_elcc(resource_df: pd.DataFrame,
                          netload_df: pd.DataFrame,
                          percentile: float) -> pd.DataFrame:
    """
    Compute baseline ELCC for each ISO and TechType based on top-percentile net load hours.

    Parameters:
    - resource_df: DataFrame with columns ['Timestamp', 'ISO', 'TechType', 'CapacityFactor']
    - netload_df: DataFrame with columns ['Timestamp', 'ISO', 'NetLoad']
    - percentile: float between 0 and 1 to select peak net load threshold

    Returns:
    - DataFrame with columns ['ISO', 'TechType', 'BaselineELCC']
    """
    results = []
    for iso in netload_df['ISO'].unique():
        nl_iso = netload_df[netload_df['ISO'] == iso]
        threshold = nl_iso['NetLoad'].quantile(percentile)
        peak_hours = nl_iso[nl_iso['NetLoad'] >= threshold]['Timestamp']
        for tech in resource_df['TechType'].unique():
            prof = resource_df[
                (resource_df['ISO'] == iso) &
                (resource_df['TechType'] == tech)
            ]
            prof_peak = prof[prof['Timestamp'].isin(peak_hours)]
            baseline = prof_peak['CapacityFactor'].mean() if not prof_peak.empty else 0.0
            results.append({
                'ISO': iso,
                'TechType': tech,
                'BaselineELCC': baseline
            })
    return pd.DataFrame(results)

def apply_penetration_decay(elcc_df: pd.DataFrame,
                            penetration: dict,
                            decay_params: dict) -> pd.DataFrame:
    """
    Apply exponential decay to baseline ELCC values to account for saturation.

    Parameters:
    - elcc_df: DataFrame with ['ISO', 'TechType', 'BaselineELCC']
    - penetration: dict mapping ISO->TechType->penetration_ratio
    - decay_params: dict mapping TechType->decay_constant (lambda)

    Returns:
    - DataFrame with columns ['ISO', 'TechType', 'BaselineELCC',
      'Penetration', 'Lambda', 'AdjustedELCC']
    """
    records = []
    for _, row in elcc_df.iterrows():
        iso = row['ISO']
        tech = row['TechType']
        base = row['BaselineELCC']
        pen = penetration.get(iso, {}).get(tech, 0.0)
        lam = decay_params.get(tech, 0.0)
        adjusted = base * np.exp(-lam * pen)
        records.append({
            'ISO': iso,
            'TechType': tech,
            'BaselineELCC': base,
            'Penetration': pen,
            'Lambda': lam,
            'AdjustedELCC': adjusted
        })
    return pd.DataFrame(records)