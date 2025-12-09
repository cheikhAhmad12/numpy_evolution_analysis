#!/usr/bin/env python3

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns

DATA_CLEAN_PATH = Path("data/clean/monthly_activity.csv")
PLOTS_DIR = Path("plots")

def load_and_prepare_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_CLEAN_PATH)

    df["month"] = pd.to_datetime(df["month"], errors="raise")
    df = df.sort_values("month").reset_index(drop=True)

    print("=== Dataset Summary ===")
    print("Rows:", len(df))
    print("\nMissing values:")
    print(df.isna().sum())
    print("\nDuplicate rows:", df.duplicated().sum())
    print("\nColumn types:")
    print(df.dtypes)
    print()

    df["year"] = df["month"].dt.year
    df["month_num"] = df["month"].dt.month

    return df


def ensure_plots_dir():
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

def plot_commits_time_series(df: pd.DataFrame):
    plt.figure(figsize=(12, 5))
    plt.plot(df["month"], df["commits"], label="Monthly commits")
    df["commits_rolling_6"] = df["commits"].rolling(window=6).mean()
    plt.plot(df["month"], df["commits_rolling_6"], "--", label="6-month rolling avg")
    plt.title("Monthly Number of Commits in NumPy")
    plt.xlabel("Month")
    plt.ylabel("Commits")
    plt.legend()
    plt.tight_layout()
    path = PLOTS_DIR / "commits_time_series.png"
    plt.savefig(path, dpi=300)
    print("Saved:", path)
    plt.close()

def plot_churn_distribution(df: pd.DataFrame):
    plt.figure(figsize=(10, 5))
    plt.hist(df["churn"], bins=50)
    plt.title("Distribution of Monthly Code Churn")
    plt.xlabel("Churn")
    plt.ylabel("Frequency")
    plt.tight_layout()
    path = PLOTS_DIR / "churn_distribution.png"
    plt.savefig(path, dpi=300)
    print("Saved:", path)
    plt.close()

def plot_commit_heatmap(df: pd.DataFrame):
    data = df.pivot_table(index="year", columns="month_num", values="commits", aggfunc="sum")
    plt.figure(figsize=(14, 10))
    sns.heatmap(data, cmap="viridis", linewidths=0.5, linecolor="gray")
    plt.title("Heatmap of Monthly Commit Activity")
    plt.xlabel("Month")
    plt.ylabel("Year")
    plt.tight_layout()
    path = PLOTS_DIR / "commit_heatmap.png"
    plt.savefig(path, dpi=300)
    print("Saved:", path)
    plt.close()

def plot_commits_vs_churn(df: pd.DataFrame):
    years = df["year"].values
    fig, ax = plt.subplots(figsize=(10, 6))
    norm = plt.Normalize(years.min(), years.max())
    colors = cm.viridis(norm(years))
    ax.scatter(df["commits"], df["churn"], c=colors, alpha=0.7, edgecolor="none")
    cbar = fig.colorbar(cm.ScalarMappable(norm=norm, cmap="viridis"), ax=ax)
    cbar.set_label("Year")
    ax.set_xlabel("Commits")
    ax.set_ylabel("Churn")
    ax.set_title("Commits vs Churn")
    plt.tight_layout()
    path = PLOTS_DIR / "commits_vs_churn_scatter.png"
    plt.savefig(path, dpi=300)
    print("Saved:", path)
    plt.close()

def main():
    ensure_plots_dir()
    df = load_and_prepare_data()
    plot_commits_time_series(df)
    plot_churn_distribution(df)
    plot_commit_heatmap(df)
    plot_commits_vs_churn(df)
    print("All plots generated.")

if __name__ == "__main__":
    main()
