

#!/usr/bin/env python3
"""
run_ascde.py: Compute Adaptive System Capacity & Deliverability Evaluation (ASCDE)
scores for interconnection queue projects by merging survival, capacity, ELCC, and
expected unserved energy (EUE), then monetizing via Value of Lost Load (VOLL).
"""

import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt

def parse_args():
    parser = argparse.ArgumentParser(
        description="Compute ASCDE scores for queue projects."
    )
    parser.add_argument(
        "--queue", "-q", required=True,
        help="CSV of queue projects (ProjectID, ISO, TechType, Capacity, SurvivalProbability)."
    )
    parser.add_argument(
        "--elcc", "-e", required=True,
        help="CSV from calc_elcc.py (ISO, TechType, AdjustedELCC)."
    )
    parser.add_argument(
        "--eue", "-u", required=True,
        help="CSV of expected unserved energy by project (ProjectID, EUE in MWh)."
    )
    parser.add_argument(
        "--voll", "-v", type=float, default=5000.0,
        help="Value of Lost Load ($/MWh). Default: 5000."
    )
    parser.add_argument(
        "--output", "-o", default="outputs/ascde_scores.csv",
        help="Output path for ASCDE scores CSV."
    )
    parser.add_argument(
        "--plot", action="store_true",
        help="Generate and save histogram of ASCDE scores."
    )
    return parser.parse_args()

def main():
    args = parse_args()
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    # Load inputs
    queue_df = pd.read_csv(args.queue)
    elcc_df = pd.read_csv(args.elcc)
    eue_df  = pd.read_csv(args.eue)

    # Merge datasets
    df = queue_df.merge(elcc_df[['ISO', 'TechType', 'AdjustedELCC']],
                        on=['ISO', 'TechType'], how='left')
    df = df.merge(eue_df[['ProjectID', 'EUE']],
                  on='ProjectID', how='left')

    # Compute ASCDE: ASCDE = EUE * VOLL / (Capacity * AdjustedELCC)
    df['ASCDE'] = df['EUE'] * args.voll / (df['Capacity'] * df['AdjustedELCC'])

    # Save results
    df.to_csv(args.output, index=False)
    print(f"Saved ASCDE scores to {args.output}")

    # Optional histogram
    if args.plot:
        plt.figure(figsize=(8,6))
        df['ASCDE'].hist(bins=50)
        plt.title('Distribution of ASCDE Scores')
        plt.xlabel('ASCDE ($/MWh)')
        plt.ylabel('Project Count')
        plt.grid(False)
        plot_path = args.output.replace('.csv', '_hist.png')
        plt.savefig(plot_path, dpi=300)
        print(f"Saved ASCDE histogram to {plot_path}")

if __name__ == "__main__":
    main()