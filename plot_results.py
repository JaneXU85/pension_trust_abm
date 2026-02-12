# plot_results.py
"""
Publication-ready plots for extended pension trust ABM experiment.
Uses 'extended_experiment_all_runs.csv' with columns:
- spillover_fraction
- initial_trust
- final_trust
- participation_rate
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# ───────────────────────
# 1. Load and prepare data
# ───────────────────────
df = pd.read_csv("extended_experiment_all_runs.csv")

# Map spillover_fraction to labels
spillover_map = {0.0: "No Spillover", 0.5: "Partial Spillover", 1.0: "Full Spillover"}
df["spillover_label"] = df["spillover_fraction"].map(spillover_map)
df["spillover_label"] = pd.Categorical(
    df["spillover_label"],
    categories=["No Spillover", "Partial Spillover", "Full Spillover"],
    ordered=True
)

# Set publication-ready style
sns.set(style="whitegrid", font_scale=1.2)
plt.rcParams.update({
    "font.family": "Arial",
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "axes.linewidth": 0.8,
})

# Create figures directory
os.makedirs("figures", exist_ok=True)

# ───────────────────────
# 2. Figure 1: Participation Rate by Spillover (Boxplot)
# ───────────────────────
plt.figure(figsize=(7, 5))
ax = sns.boxplot(
    data=df,
    x="spillover_label",
    y="participation_rate",
    hue="initial_trust",
    palette="Set2",
    width=0.7,
    linewidth=0.8
)

plt.title("Participation Rate Across Spillover Conditions", fontsize=14, pad=15)
plt.xlabel("")
plt.ylabel("Participation Rate", fontsize=12)
plt.ylim(-0.05, 1.05)
plt.legend(title="Initial Trust", title_fontsize=11, fontsize=10, loc="upper right")
plt.tight_layout()
plt.savefig("figures/fig1_participation_boxplot.png", bbox_inches="tight")
plt.close()

# ───────────────────────
# 3. Figure 2: Heatmap of Average Participation Rate
# ───────────────────────
heatmap_data = df.groupby(["initial_trust", "spillover_fraction"])["participation_rate"].mean().unstack()
# Ensure column order
heatmap_data = heatmap_data[[0.0, 0.5, 1.0]]

plt.figure(figsize=(6, 4))
sns.heatmap(
    heatmap_data,
    annot=True,
    fmt=".2f",
    cmap="viridis_r",
    cbar_kws={"label": "Avg. Participation Rate"},
    linewidths=0.5,
    square=True
)

plt.title("Average Participation Rate\n(by Initial Trust and Spillover)", fontsize=13, pad=12)
plt.xlabel("Spillover Fraction", fontsize=11)
plt.ylabel("Initial Trust", fontsize=11)
plt.xticks(ticks=[0.5, 1.5, 2.5], labels=["0.0", "0.5", "1.0"])
plt.yticks(ticks=[0.5, 1.5, 2.5], labels=["0.3", "0.6", "0.9"])
plt.tight_layout()
plt.savefig("figures/fig2_participation_heatmap.png", bbox_inches="tight")
plt.close()

# ───────────────────────
# 4. Figure 3: Final Trust vs Participation Rate (Scatter)
# ───────────────────────
plt.figure(figsize=(6, 5))
sns.scatterplot(
    data=df,
    x="final_trust",
    y="participation_rate",
    hue="spillover_label",
    style="initial_trust",
    s=60,
    alpha=0.8,
    palette=["#2ca02c", "#ff7f0e", "#d62728"]
)

plt.title("System Collapse: Trust vs Participation", fontsize=14, pad=15)
plt.xlabel("Final Trust", fontsize=12)
plt.ylabel("Participation Rate", fontsize=12)
plt.xlim(-0.05, 1.05)
plt.ylim(-0.05, 1.05)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(title="Condition", title_fontsize=11, fontsize=9, loc="lower left")
plt.tight_layout()
plt.savefig("figures/fig3_trust_vs_participation.png", bbox_inches="tight")
plt.close()

# ───────────────────────
# 5. Done!
# ───────────────────────
print("✅ All figures saved to 'figures/' directory:")
print("   - fig1_participation_boxplot.png")
print("   - fig2_participation_heatmap.png")
print("   - fig3_trust_vs_participation.png")