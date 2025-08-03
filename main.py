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

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def main():
    parser = argparse.ArgumentParser(description="Run UEVF-ASCDE pipeline")
    parser.add_argument("--config", "-c", default="data/configs/modeling_config.json",
                        help="Path to unified modeling_config.json")
    parser.add_argument("--resources", "-r", default="data/resource_profiles_hourly.csv",
                        help="Path to resource profiles CSV")
    parser.add_argument("--netload", "-n", default="data/netload_hourly_2023.csv",
                        help="Path to net load CSV")
    parser.add_argument("--queue", "-q", default="data/queues_2023_clean_data_r1.csv",
                        help="Path to queue projects CSV")
    parser.add_argument("--eue", "-u", default="data/project_eue_by_region.csv",
                        help="Path to EUE CSV")
    parser.add_argument("--pipeline", "-p", choices=["elcc", "survival", "ascde", "full"],
                        default="full", help="Pipeline stage to run")
    args = parser.parse_args()

    cfg = load_modeling_config(args.config)

    if args.pipeline in ("elcc", "full"):
        try:
            logging.info("Starting ELCC calculation...")
            res_df = load_csv(args.resources, parse_dates=["Timestamp"])
            nl_df = load_csv(args.netload, parse_dates=["Timestamp"])
            elcc_df = compute_baseline_elcc(res_df, nl_df, cfg["modeling_parameters"]["peak_percentile"])
            elcc_df = apply_penetration_decay(elcc_df, cfg["penetration_ratios"], cfg["elcc_decay_parameters"])
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