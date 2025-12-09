from pydriller import Repository
import pandas as pd
from pathlib import Path

REPO_PATH = Path("external/numpy")

#Output directory where the cleaned dataset will be stored.
DATA_CLEAN = Path("data/clean")
DATA_CLEAN.mkdir(parents=True, exist_ok=True)


def main():
    """
    Traverse the full Git history of the NumPy repository using PyDriller,
    extract commit metadata and code churn information, and aggregate
    the results at a monthly level.
    The output is saved as a CSV file for further analysis.
    """
    records = []

    print(f"Analyzing repository: {REPO_PATH.resolve()}")
    for commit in Repository(str(REPO_PATH)).traverse_commits():

        # Optional: skip merge commits since they do not introduce new code changes
        if len(commit.parents) > 1:
            continue

        date = commit.committer_date
        month = date.strftime("%Y-%m")
        additions = commit.insertions or 0
        deletions = commit.deletions or 0
        
        records.append({
            "month": month,
            "hash": commit.hash,
            "additions": additions,
            "deletions": deletions,
            "churn": additions + deletions,
        })
    df = pd.DataFrame(records)

    # Aggregate metrics at a monthly level
    monthly = df.groupby("month").agg(
        commits=("hash", "count"),
        additions=("additions", "sum"),
        deletions=("deletions", "sum"),
        churn=("churn", "sum"),
    ).reset_index().sort_values("month")


    output_path = DATA_CLEAN / "monthly_activity.csv"
    monthly.to_csv(output_path, index=False)
    print(f"Monthly activity data saved to: {output_path}")


if __name__ == "__main__":
    main()