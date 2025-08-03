# Unified Energy Valuation Framework – ASCDE Modeling Stack

This repository hosts the modeling architecture, scripts, and analytics pipeline for the **Unified Energy Valuation Framework (UEVF)** and **Adaptive System Capacity & Deliverability Evaluation (ASCDE)**. This stack quantifies project viability, reliability-adjusted contribution, and queue dynamics using empirical queue data, probabilistic modeling, and interconnection-specific friction metrics.

---

## 🧠 Core Concepts

- **UEVF-IQ**: A predictive scoring model that converts raw interconnection queue data into reliability- and finance-adjusted viability scores.
- **ELCC Calibration**: Effective Load Carrying Capability modeled by technology, season, and ISO penetration saturation.
- **ASCDE ($/MWh)**: A monetized reliability value metric based on the project’s ability to reduce Expected Unserved Energy (EUE) under probabilistic demand/generation scenarios.
- **Queue Survival Entropy (bits)**: An information-theoretic measure of uncertainty across queue cohorts or vintages.

---

## 📁 Repository Structure

```plaintext
uevf-ascde-modeling/
├── data/             # Sample queue data, project metadata, ELCC tables (linked to Google Drive)
├── notebooks/        # Jupyter notebooks for interactive modeling and charting
├── scripts/          # Main modeling pipeline (e.g., run_ascde.py, calc_elcc.py)
├── utils/            # Helper modules for queue parsing, ELCC curves, entropy modeling
├── models/           # Serialized survival models, ELCC decay fits, etc.
├── outputs/          # Generated CSVs, ASCDE rankings, plots, charts

## 📂 Data Directory (Google Drive)

All large data assets are stored externally in Drive.

See [`data/README.md`](data/README.md) for file list, structure, and integration instructions.