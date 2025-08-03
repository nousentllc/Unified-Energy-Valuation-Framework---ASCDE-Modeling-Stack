#!/usr/bin/env python3
"""
main.py: Unified runner for UEVF-ASCDE modeling pipeline.
"""

import argparse
from uevf.config import load_modeling_config
from uevf.elcc import compute_baseline_elcc, apply_penetration_decay
from uevf.survival import compute_survival_entropy
from uevf.ascde import compute_ascde
from uevf.utils import load_csv, save_dataframe
import logging
import sys
import json
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def main():
    parser = argparse.ArgumentParser(description="Run UEVF-ASCDE pipeline")
    parser.add_argument("--config", "-c", default="data/modeling_config.json",
                        help="Path to unified modeling_config.json")
    parser.add_argument("--resources", "-r", default="data/20250728_rt_lmp_final.csv",
                        help="Path to resource profiles CSV")
    parser.add_argument("--netload", "-n", default="data/EIA_930A_2023_with layout.xlsx",
                        help="Path to net load CSV")
    parser.add_argument("--queue", "-q", default="data/July Queue's 2025.xlsx",
                        help="Path to queue projects CSV")
    parser.add_argument("--eue", "-u", default="data/UEVF-IQ - Foundational.csv",
                        help="Path to EUE CSV")
    parser.add_argument("--pipeline", "-p", choices=["elcc", "survival", "ascde", "full"],
                        default="full", help="Pipeline stage to run")
    parser.add_argument("--penetration", "-x", default="data/penetration_ratios.json",
                        help="Path to penetration ratios JSON")
    parser.add_argument("--data-dir", "-d",
                        help="Base directory for all data inputs; overrides individual file paths")
    args = parser.parse_args()

    # If a single data directory is specified, derive all input paths from it
    if args.data_dir:
        base = args.data_dir.rstrip(os.sep)
        args.config = os.path.join(base, "modeling_config.json")
        args.penetration = os.path.join(base, "penetration_ratios.json")
        args.resources = os.path.join(base, "20250728_rt_lmp_final.csv")
        args.netload = os.path.join(base, "EIA_930A_2023_with layout.xlsx")
        args.queue = os.path.join(base, "July Queue's 2025.xlsx")
        args.eue = os.path.join(base, "UEVF-IQ - Foundational.csv")

    # Load unified config and penetration ratios
    cfg = load_modeling_config(args.config)
    with open(args.penetration, 'r') as f:
        penetration = json.load(f)

    # Verify that all required input files exist
    required_files = [
        args.config, args.penetration,
        args.resources, args.netload,
        args.queue, args.eue
    ]
    for file_path in required_files:
        if not os.path.exists(file_path):
            logging.error("Required input file not found: %s", file_path)
            sys.exit(1)

    if args.pipeline in ("elcc", "full"):
        try:
            logging.info("Starting ELCC calculation...")
            res_df = load_csv(args.resources, parse_dates=["Timestamp"])
            nl_df = load_csv(args.netload, parse_dates=["Timestamp"])
            elcc_df = compute_baseline_elcc(res_df, nl_df, cfg["modeling_parameters"]["peak_percentile"])
            elcc_df = apply_penetration_decay(elcc_df, penetration, cfg["elcc_decay_parameters"])
            save_dataframe(elcc_df, "outputs/elcc_summary.csv")
            logging.info("ELCC step complete: outputs/elcc_summary.csv")
        except Exception as e:
            logging.error("ELCC step failed", exc_info=True)
            sys.exit(1)

    if args.pipeline in ("survival", "full"):
        try:
            logging.info("Starting survival entropy calculation...")
            queue_df = load_csv(args.queue, parse_dates=["QueueDate", "CODDate"])
            queue_df["SurvivalTime"] = (queue_df["CODDate"] - queue_df["QueueDate"]).dt.days
            queue_df["Event"] = queue_df["Status"].apply(lambda x: 1 if x == "Operational" else 0)
            entropy_df = compute_survival_entropy(queue_df)
            save_dataframe(entropy_df, "outputs/survival_entropy_report.csv")
            logging.info("Survival step complete: outputs/survival_entropy_report.csv")
        except Exception as e:
            logging.error("Survival step failed", exc_info=True)
            sys.exit(1)

    if args.pipeline in ("ascde", "full"):
        try:
            logging.info("Starting ASCDE calculation...")
            queue_df = load_csv(args.queue)
            elcc_df = load_csv("outputs/elcc_summary.csv")
            eue_df = load_csv(args.eue)
            ascde_df = compute_ascde(queue_df, elcc_df, eue_df, cfg["modeling_parameters"]["voll"])
            save_dataframe(ascde_df, "outputs/ascde_scores.csv")
            logging.info("ASCDE step complete: outputs/ascde_scores.csv")
        except Exception as e:
            logging.error("ASCDE step failed", exc_info=True)
            sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()