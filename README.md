# NumPy Evolution Analysis

Scripts to extract and visualize how the NumPy repository evolves over time. The workflow pulls monthly commit counts and churn metrics from the Git history, writes them to `data/clean/monthly_activity.csv`, and generates a small set of plots.

## What you get
- Cleaned monthly dataset with `commits`, `additions`, `deletions`, and total `churn`
- Time-series, distribution, heatmap, and scatter plots in `plots/`
- Extraction script that traverses the full NumPy Git history (merge commits are skipped)

## Setup
1) Create/activate a Python environment : `python3 -m venv .venv` `source .venv/bin/activate`
2) Install dependencies: `pip install -r requirements.txt`
3) Clone NumPy into `external/numpy`: `git clone https://github.com/numpy/numpy.git external/numpy`

## Extract the data
Runs PyDriller across the NumPy repo and aggregates monthly metrics.
```
python -m src.extract_data
```
Outputs: `data/clean/monthly_activity.csv` with columns:
- `month` (YYYY-MM)
- `commits` (count)
- `additions`, `deletions` (line-level)
- `churn` (`additions + deletions`)

## Generate plots
Uses the cleaned CSV to build PNGs in `plots/`.
```
python make_plots.py
```
Creates:
- `commits_time_series.png`
- `churn_distribution.png`
- `commit_heatmap.png`
- `commits_vs_churn_scatter.png`

## Repository layout
- `src/extract_data.py` – data extraction and monthly aggregation
- `make_plots.py` – plotting routines
- `data/clean/` – generated CSV output
- `plots/` – generated figures
