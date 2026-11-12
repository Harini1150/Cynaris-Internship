
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import IsolationForest


# --------------------------------------------------
# 1. PROJECT CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "indian_business_orders.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
EVIDENCE_DIR = BASE_DIR / "evidence"

OUTPUT_DIR.mkdir(exist_ok=True)
EVIDENCE_DIR.mkdir(exist_ok=True)

FEATURES = ["Amount", "Profit", "Quantity"]

CONTAMINATION = 0.05
RANDOM_STATE = 42

sns.set_theme(style="whitegrid")


# --------------------------------------------------
# 2. LOAD AND INSPECT THE DATASET
# --------------------------------------------------

def load_dataset():
    print("\n========== DATASET INSPECTION ==========")

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    print(f"\nDataset shape: {df.shape}")
    print(f"Total rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nFirst five records:")
    print(df.head())

    print("\nMissing values:")
    print(df.isnull().sum())

    print(f"\nDuplicate rows: {df.duplicated().sum()}")

    for feature in FEATURES:
        if feature not in df.columns:
            raise ValueError(
                f"Required column '{feature}' is missing."
            )

        df[feature] = pd.to_numeric(
            df[feature], errors="coerce"
        )

    return df


# --------------------------------------------------
# 3. IQR STATISTICAL ANOMALY DETECTION
# --------------------------------------------------

def detect_iqr_anomalies(df):
    print("\n========== IQR ANOMALY DETECTION ==========")

    summary = []
    iqr_flags = []

    for feature in FEATURES:

        values = df[feature].dropna()

        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)

        flag = (
            (df[feature] < lower_bound)
            | (df[feature] > upper_bound)
        ).fillna(False)

        flag_column = f"{feature}_IQR_Anomaly"
        df[flag_column] = flag

        anomaly_count = int(flag.sum())

        summary.append({
            "Feature": feature,
            "Q1": q1,
            "Q3": q3,
            "IQR": iqr,
            "Lower_Bound": lower_bound,
            "Upper_Bound": upper_bound,
            "Anomaly_Count": anomaly_count,
            "Anomaly_Percentage": (
                anomaly_count / len(df) * 100
            )
        })

        iqr_flags.append(flag)

        print(f"\nFeature: {feature}")
        print(f"Q1: {q1:.2f}")
        print(f"Q3: {q3:.2f}")
        print(f"IQR: {iqr:.2f}")
        print(f"Lower bound: {lower_bound:.2f}")
        print(f"Upper bound: {upper_bound:.2f}")
        print(f"Potential anomalies: {anomaly_count}")

    df["IQR_Anomaly"] = np.logical_or.reduce(iqr_flags)

    summary_df = pd.DataFrame(summary)

    summary_df.to_csv(
        OUTPUT_DIR / "iqr_summary.csv",
        index=False
    )

    return df, summary_df


# --------------------------------------------------
# 4. ISOLATION FOREST ANOMALY DETECTION
# --------------------------------------------------

def detect_isolation_forest(df):
    print("\n========== ISOLATION FOREST ==========")

    # Keep only records with all required numeric features.
    valid_mask = df[FEATURES].notna().all(axis=1)

    X = df.loc[valid_mask, FEATURES]

    if len(X) < 2:
        raise ValueError(
            "Not enough valid records for Isolation Forest."
        )

    model = IsolationForest(
        n_estimators=100,
        contamination=CONTAMINATION,
        random_state=RANDOM_STATE
    )

    predictions = model.fit_predict(X)

    # -1 means anomaly; 1 means normal.
    df["IsolationForest_Prediction"] = np.nan
    df["IsolationForest_Anomaly"] = False
    df["Anomaly_Score"] = np.nan

    df.loc[
        valid_mask, "IsolationForest_Prediction"
    ] = predictions

    df.loc[
        valid_mask, "IsolationForest_Anomaly"
    ] = predictions == -1

    # Higher scores indicate more unusual observations.
    anomaly_scores = -model.decision_function(X)

    df.loc[
        valid_mask, "Anomaly_Score"
    ] = anomaly_scores

    anomaly_count = int(
        (predictions == -1).sum()
    )

    print(f"\nRecords analyzed: {len(X)}")
    print(f"Contamination setting: {CONTAMINATION}")
    print(f"Anomalies detected: {anomaly_count}")
    print(
        f"Normal records: {int((predictions == 1).sum())}"
    )

    return df, model


# --------------------------------------------------
# 5. COMPARE BOTH DETECTION METHODS
# --------------------------------------------------

def compare_methods(df):
    print("\n========== METHOD COMPARISON ==========")

    df["Anomaly_Method_Count"] = (
        df["IQR_Anomaly"].astype(int)
        + df["IsolationForest_Anomaly"].astype(int)
    )

    df["Anomaly_Consensus"] = (
        df["Anomaly_Method_Count"] == 2
    )

    total = len(df)

    iqr_count = int(df["IQR_Anomaly"].sum())

    isolation_count = int(
        df["IsolationForest_Anomaly"].sum()
    )

    consensus_count = int(
        df["Anomaly_Consensus"].sum()
    )

    summary = pd.DataFrame([
        {
            "Method": "IQR",
            "Anomaly_Count": iqr_count,
            "Percentage": iqr_count / total * 100
        },
        {
            "Method": "Isolation Forest",
            "Anomaly_Count": isolation_count,
            "Percentage": isolation_count / total * 100
        },
        {
            "Method": "Both Methods",
            "Anomaly_Count": consensus_count,
            "Percentage": consensus_count / total * 100
        }
    ])

    print(summary.to_string(index=False))

    summary.to_csv(
        OUTPUT_DIR / "anomaly_summary.csv",
        index=False
    )

    return df, summary


# --------------------------------------------------
# 6. SAVE ANOMALY RESULTS
# --------------------------------------------------

def save_results(df):
    print("\n========== SAVING RESULTS ==========")

    results_path = (
        OUTPUT_DIR / "anomaly_detection_results.csv"
    )

    df.to_csv(results_path, index=False)

    top_anomalies = (
        df[df["IsolationForest_Anomaly"]]
        .sort_values(
            by="Anomaly_Score",
            ascending=False
        )
        .head(20)
    )

    top_anomalies.to_csv(
        OUTPUT_DIR / "top_anomalies.csv",
        index=False
    )

    print(f"Saved: {results_path}")
    print(
        f"Saved top anomalies: "
        f"{OUTPUT_DIR / 'top_anomalies.csv'}"
    )


# --------------------------------------------------
# 7. VISUALIZE ANOMALIES
# --------------------------------------------------

def create_visualizations(df):
    print("\n========== CREATING VISUALIZATIONS ==========")

    # Plot 1: Amount vs Profit
    valid = df.dropna(
        subset=["Amount", "Profit"]
    ).copy()

    plt.figure(figsize=(10, 6))

    sns.scatterplot(
        data=valid,
        x="Amount",
        y="Profit",
        hue="IsolationForest_Anomaly",
        palette={
            False: "steelblue",
            True: "red"
        },
        alpha=0.75
    )

    plt.title(
        "Indian Business Orders: Amount vs Profit Anomalies"
    )
    plt.xlabel("Order Amount")
    plt.ylabel("Profit")
    plt.legend(title="Isolation Forest Anomaly")

    plt.tight_layout()

    scatter_path = (
        OUTPUT_DIR / "anomaly_detection_amount_profit.png"
    )

    plt.savefig(scatter_path, dpi=300)
    plt.close()

    # Plot 2: Boxplots for numerical features
    fig, axes = plt.subplots(
        1, 3, figsize=(15, 5)
    )

    for ax, feature in zip(axes, FEATURES):
        sns.boxplot(
            y=df[feature],
            ax=ax,
            color="skyblue"
        )

        ax.set_title(f"{feature} Distribution")

    fig.suptitle(
        "Boxplots of Business Order Features"
    )

    plt.tight_layout()

    boxplot_path = (
        OUTPUT_DIR / "anomaly_feature_boxplots.png"
    )

    plt.savefig(boxplot_path, dpi=300)
    plt.close()

    # Plot 3: Compare anomaly counts
    counts = [
        int(df["IQR_Anomaly"].sum()),
        int(df["IsolationForest_Anomaly"].sum()),
        int(df["Anomaly_Consensus"].sum())
    ]

    labels = [
        "IQR",
        "Isolation Forest",
        "Both Methods"
    ]

    plt.figure(figsize=(9, 5))

    sns.barplot(
        x=labels,
        y=counts,
        hue=labels,
        palette="viridis",
        legend=False
    )

    plt.title("Anomaly Detection Method Comparison")
    plt.xlabel("Detection Method")
    plt.ylabel("Number of Anomalies")

    plt.tight_layout()

    comparison_path = (
        OUTPUT_DIR / "anomaly_method_comparison.png"
    )

    plt.savefig(comparison_path, dpi=300)
    plt.close()

    # Copy plots into evidence folder.
    for plot_path in [
        scatter_path,
        boxplot_path,
        comparison_path
    ]:
        evidence_path = EVIDENCE_DIR / plot_path.name

        evidence_path.write_bytes(
            plot_path.read_bytes()
        )

        print(f"Saved visualization: {plot_path}")
        print(f"Saved evidence: {evidence_path}")


# --------------------------------------------------
# 8. MAIN EXECUTION
# --------------------------------------------------

def main():
    print("\n========================================")
    print(" W10D3 - ANOMALY DETECTION PROJECT")
    print(" Indian Business Orders Dataset")
    print("========================================")

    df = load_dataset()

    df, iqr_summary = detect_iqr_anomalies(df)

    df, model = detect_isolation_forest(df)

    df, anomaly_summary = compare_methods(df)

    save_results(df)

    create_visualizations(df)

    print("\n========== FINAL SUMMARY ==========")

    print(f"Total dataset records: {len(df)}")

    print(
        f"IQR anomalies: {df['IQR_Anomaly'].sum()}"
    )

    print(
        "Isolation Forest anomalies: "
        f"{df['IsolationForest_Anomaly'].sum()}"
    )

    print(
        f"Agreed anomalies: {df['Anomaly_Consensus'].sum()}"
    )

    print("\nAll W10D3 analysis tasks completed!")
    print(f"Check your results folder: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
