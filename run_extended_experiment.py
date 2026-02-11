"""
Extended experiment script for Pension Trust ABM with partial spillover.
Runs simulations across:
  - 3 initial trust levels: 0.3, 0.6, 0.9
  - 3 spillover conditions: Off (0.0), Partial (0.5), Full (1.0)
  - 30 replications per condition

Total runs: 3 × 3 × 30 = 270
Outputs: extended_experiment_all_runs.csv
"""

from model import PensionTrustModel
import pandas as pd
import numpy as np

# ----------------------------
# Configuration
# ----------------------------
INITIAL_TRUST_VALUES = [0.3, 0.6, 0.9]
SPILLOVER_CONDITIONS = [
    {"enabled": False, "fraction": 0.0, "label": "No Spillover"},
    {"enabled": True,  "fraction": 0.5, "label": "Partial Spillover"},
    {"enabled": True,  "fraction": 1.0, "label": "Full Spillover"},
]
REPLICATIONS = 30
NUM_STEPS = 50
SEED_BASE = 42  # For reproducibility

# ----------------------------
# Run experiments
# ----------------------------
results = []

print("🚀 Starting extended experiment (270 runs)...")
run_id = 0

for init_trust in INITIAL_TRUST_VALUES:
    for sp_cond in SPILLOVER_CONDITIONS:
        for rep in range(REPLICATIONS):
            run_id += 1
            seed = SEED_BASE + run_id  # Unique seed per run
            
            model = PensionTrustModel(
                num_citizens=100,
                num_brokers=5,
                initial_trust=init_trust,
                spillover_enabled=sp_cond["enabled"],
                spillover_fraction=sp_cond["fraction"],
                seed=seed
            )
            
            model.run_model(n_steps=NUM_STEPS)
            data = model.datacollector.get_model_vars_dataframe()
            
            results.append({
                "replication_id": run_id,
                "initial_trust": init_trust,
                "spillover_enabled": sp_cond["enabled"],
                "spillover_fraction": sp_cond["fraction"],
                "spillover_label": sp_cond["label"],
                "final_trust": data["FinalTrust"].iloc[-1],
                "final_cooperation": data["FinalCooperation"].iloc[-1]
            })
            
            if run_id % 30 == 0:
                print(f"✅ Completed {run_id}/270 runs")

# ----------------------------
# Save to CSV
# ----------------------------
df = pd.DataFrame(results)
df.to_csv("extended_experiment_all_runs.csv", index=False)

print("\n🎉 All runs completed!")
print(f"📊 Data saved to 'extended_experiment_all_runs.csv'")
print("\nSummary by condition:")
summary = df.groupby(["spillover_label", "initial_trust"])[["final_trust", "final_cooperation"]].agg(["mean", "std"])
print(summary.round(4))