import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# Create results folder if it does not exist
os.makedirs("results", exist_ok=True)

# Load example data
data = pd.read_csv("data/example_cfos_data.csv")

# Calculate mean and SEM
summary = (
    data.groupby(["region", "group"])["cfos_positive_cells"]
    .agg(["mean", "sem"])
    .reset_index()
)

print("Group summary:")
print(summary)

# Statistical comparison by region
for region in data["region"].unique():
    subset = data[data["region"] == region]

    control = subset[subset["group"] == "Control"]["cfos_positive_cells"]
    morphine = subset[subset["group"] == "Morphine"]["cfos_positive_cells"]

    t_stat, p_value = stats.ttest_ind(control, morphine)

    print(f"{region}: t = {t_stat:.3f}, p = {p_value:.4f}")

# Generate plots
for region in data["region"].unique():
    subset = summary[summary["region"] == region]

    plt.figure()
    plt.bar(
        subset["group"],
        subset["mean"],
        yerr=subset["sem"],
        capsize=5
    )
    plt.ylabel("c-Fos-positive cells")
    plt.title(f"c-Fos quantification in {region}")
    plt.tight_layout()
    plt.savefig(f"results/cfos_{region}_comparison.png", dpi=300)
    plt.close()
