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
├── requirements.txt  # Dependencies
├── README.md         # Project overview and usage instructions
└── .gitignore        # Ignored files and folders
```

---

## ⚙️ Key Scripts

- `scripts/run_ascde.py`: Full ASCDE score computation from preprocessed data
- `scripts/calc_elcc.py`: ELCC assignment by tech/region with saturation penalties
- `utils/queue_utils.py`: Functions for parsing queue data, computing friction scores
- `notebooks/survival_modeling.ipynb`: Survival entropy, probability fitting, and visualization

---

## 📊 Key Outputs

- `outputs/ascde_scores.csv`: Project-level ASCDE valuations
- `outputs/survival_entropy_report.csv`: Entropy levels by ISO, year, and technology
- `outputs/elcc_summary.csv`: Normalized ELCC scores by region and saturation level
- `outputs/ascde_scores_hist.png`: Histogram of ASCDE score distribution

---

## 🔗 Data Access

Due to size and volatility, primary datasets (e.g., ISO queues, ELCC tables, survival histories) are stored externally.

📂 [Google Drive Folder](https://drive.google.com/drive/folders/your-folder-id)

Use `data/README.md` for schema and access instructions.

---

## 🚀 Getting Started

```bash
# Clone this repo
git clone https://github.com/nousentllc/uevf-ascde-modeling.git
cd uevf-ascde-modeling

# Create virtual environment and install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run survival modeling notebook
jupyter lab notebooks/survival_modeling.ipynb

# Compute ELCC
scripts/calc_elcc.py \
  -r data/resource_profiles.csv \
  -n data/netload.csv \
  -p data/penetration.json \
  -d data/decay_params.json \
  --output outputs/elcc_summary.csv \
  --plot

# Compute ASCDE
scripts/run_ascde.py \
  -q data/queue_projects.csv \
  -e outputs/elcc_summary.csv \
  -u data/eue.csv \
  --output outputs/ascde_scores.csv \
  --plot
```

---

## 🧠 Future Enhancements

- Integrate battery dispatch behavior for hybrid ELCC scoring
- Expand LMP-based curtailment penalty analysis
- Monte Carlo variant for multi-scenario EUE risk modeling

---

## 📄 License

MIT License © 2025 [Nous Enterprise LLC](https://www.linkedin.com/in/justin-candler-83971090/)

---

## 🤝 Contributions

Open to collaboration with grid modelers, ISO economists, or regulatory analysts.  
Contact: nousentllc@gmail.com
