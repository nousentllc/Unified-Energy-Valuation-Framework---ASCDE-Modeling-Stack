

#!/usr/bin/env python3
"""
calc_elcc.py: Compute Effective Load Carrying Capability (ELCC) by technology and region,
apply penetration-driven decay, and output summarized ELCC values.
"""

import os
import argparse
import json

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def compute_baseline_elcc(resource_df, netload_df, percentile=0.99):
    """
    Compute baseline ELCC as the mean capacity factor during the top percentile of net load hours.
    Returns a DataFrame with columns: ['ISO', 'TechType', 'BaselineELCC'].
    """
    results = []
    # process each ISO separately
    for iso in netload_df['ISO'].unique():
        nl_iso = netload_df[netload_df['ISO'] == iso]
        # threshold for peak hours
        threshold = nl_iso['NetLoad'].quantile(percentile)
        peak_hours = nl_iso[nl_iso['NetLoad'] >= threshold]['Timestamp']
        # for each tech in this ISO
        for tech in resource_df['TechType'].unique():
            prof = resource_df[(resource_df['ISO'] == iso) & (resource_df['TechType'] == tech)]
            # align on peak hours
            prof_peak = prof[prof['Timestamp'].isin(peak_hours)]
            if prof_peak.empty:
                baseline = 0.0
            else:
                baseline = prof_peak['CapacityFactor'].mean()
            results.append({'ISO': iso, 'TechType': tech, 'BaselineELCC': baseline})
    return pd.DataFrame(results)

def apply_penetration_decay(df, penetration_dict, decay_params):
    """
    Apply exponential decay: AdjustedELCC = BaselineELCC * exp(-lambda * penetration)
    Returns a DataFrame with appended columns: 'Penetration', 'Lambda', 'AdjustedELCC'.
    """
    records = []
    for _, row in df.iterrows():
        iso = row['ISO']
        tech = row['TechType']
        baseline = row['BaselineELCC']
        # lookup penetration
        penetration = penetration_dict.get(iso, {}).get(tech, 0.0)
        # lookup decay constant
        lam = decay_params.get(tech, 0.0)
        adjusted = baseline * np.exp(-lam * penetration)
        records.append({
            'ISO': iso,
            'TechType': tech,
            'BaselineELCC': baseline,
            'Penetration': penetration,
            'Lambda': lam,
            'AdjustedELCC': adjusted
        })
    return pd.DataFrame(records)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Compute baseline and adjusted ELCC for each ISO and technology."
    )
    parser.add_argument(
        "--resource-profiles", "-r", required=True,
        help="CSV of resource profiles (Timestamp, ISO, TechType, CapacityFactor)."
    )
    parser.add_argument(
        "--netload", "-n", required=True,
        help="CSV of net load (Timestamp, ISO, NetLoad)."
    )
    parser.add_argument(
        "--penetration", "-p", required=True,
        help="JSON file mapping ISO->TechType->penetration ratio."
    )
    parser.add_argument(
        "--decay-params", "-d", required=True,
        help="JSON file mapping TechType->decay constant lambda."
    )
    parser.add_argument(
        "--output", "-o", default="outputs/elcc_summary.csv",
        help="Path to output CSV summary."
    )
    parser.add_argument(
        "--plot", action="store_true",
        help="If set, generate and save ELCC vs penetration plots."
    )
    return parser.parse_args()

def main():
    args = parse_args()
    # create output dir if needed
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    # Load inputs
    res_df = pd.read_csv(args.resource_profiles, parse_dates=['Timestamp'])
    nl_df = pd.read_csv(args.netload, parse_dates=['Timestamp'])
    with open(args.penetration) as f:
        penetration = json.load(f)
    with open(args.decay_params) as f:
        decay_params = json.load(f)

    # Compute baseline ELCC
    baseline_df = compute_baseline_elcc(res_df, nl_df)

    # Apply decay
    summary_df = apply_penetration_decay(baseline_df, penetration, decay_params)

    # Save summary
    summary_df.to_csv(args.output, index=False)
    print(f"Saved ELCC summary to {args.output}")

    # Optional plot
    if args.plot:
        plt.figure(figsize=(8,6))
        for tech in summary_df['TechType'].unique():
            subset = summary_df[summary_df['TechType'] == tech]
            plt.plot(subset['Penetration'], subset['AdjustedELCC'], marker='o', label=tech)
        plt.title('Adjusted ELCC vs. Penetration')
        plt.xlabel('Penetration')
        plt.ylabel('Adjusted ELCC')
        plt.legend()
        plt.grid(True)
        plot_path = args.output.replace('.csv', '.png')
        plt.savefig(plot_path, dpi=300)
        print(f"Saved ELCC penetration plot to {plot_path}")

if __name__ == "__main__":
    main()