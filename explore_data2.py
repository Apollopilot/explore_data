from pathlib import Path
import sys
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns 

sns.set(style="whitegrid") 


CSV_NAME = "simulated_cognitive_data.csv"

def locate_csv(csv_name: str = CSV_NAME) -> Path:
    here = Path(__file__).resolve().parent
    candidates = [
        here / "data" / csv_name,
        here.parent / "data" / csv_name,
        here.parent.parent / "data"/ csv_name,
    ]

    for p in candidates: 
     if p.exists():
        return p  
    
    print("\n[ERROR] Couldn't find the CSV at any of these locations:\n", file=sys.stderr)
    for p in candidates:
        print(f" - {p}", file=sys.stderr)
    print("\nTips:", file=sys.stderr)
    print("  • Make sure the file is really named exactly:", csv_name, file=sys.stderr)
    print("  • Put it in a 'data' folder next to this script or one/two folders above.", file=sys.stderr)
    sys.exit(1)

def load_data(path: Path) -> pd.DataFrame:
    print(f"[INFO] Loading data from:{path}")
    df= pd.read_csv(path)
    return df 

def explore_dataframe(df: pd.DataFrame) -> None:
    print("\n=== BASIC SHAPE & COLLUMNS ===")
    print("Rows, Columns:", df.shape)
    print("Columns:", df.columns.tolist())

    print("\n=== DATA TYPES (dtypes) ===")
    print(df.dtypes)

    print("\n=== FIRST 5 ROWS (preview) ===")
    print(df.head())

    print("=== MISSING STATS (numeric only) ===")
    print(df.describe())

    #If a binary target exists, show its distribution
    if "cognitive_overload" in df.columns:
        print("\n=== cognitive_overload VALUE COUNTS ===")
        print(df["cognitive_overload"].value_counts(dropna=False))


# 1) Mental Effort Hisogram
def plot_distributions(df: pd.DataFrame) -> None:
    if "mental_effort" in df.columns:
        plt.figure(figsize=(8,5))
        sns.histplot(data=df, x="mental_effort", kde=True, bins=20, color="royalblue")
        plt.title("Distribution of Reported Mental Effort")
        plt.xlabel("Mental Effort (1-10 scale)")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.show()

    # 2) task duration histogram (if present)
    if "task_duration_min" in df. columns:
        plt.figure(figsize=(8,5))
        sns.histoplot(data=df, x="tas_duration_min", kde=True, bins=20)
        plt.title("Task Duration (minutes)")
        plt.xlabel("Minutes")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.show()

    # 3) Overload count plot (if present)
    if "cognitive_overload" in df.columns:
        plt.figure(figsize=(6,4))
        sns.countplot(x="cognitive_overload", data=df)
        plt.title("Counts: Cognitive Overload (0 = No, 1 = Yes)")
        plt.xlabel("cognitive_overload")
        plt.ylable("Count")
        plt.tight_layout()
        plt.show()

def plot_correlations (df: pd.DataFrame) -> None:
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.shape[1] < 2:
        print("\n [INFO] Not enough numeric columns for correlation heatmap.")
        return
    
    corr = numeric_df.corr(numeric_only=True)
    plt.figure(figsize=(8,6))
    sns.heatmap(corr, annot=True, fmt=".2f", square=True, cmap="vlag", cbar=True)
    plt.title("Correlation Heatmap (numeric columns)")
    plt.tight_layout()
    plt.show()

def main():
    csv_path= locate_csv(CSV_NAME)  # 1)find the file robustly
    df= load_data(csv_path)         # 2) Load it
    explore_dataframe(df)           # 3) Text-based overview
    plot_distributions(df)          # 4) A few core plots (safe if columns missing)
    plot_correlations(df)           # 5) Optional heatmap for quick insights

if __name__ == "__main__":
    main()

