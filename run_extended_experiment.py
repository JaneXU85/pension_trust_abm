# run_extended_experiment.py
import os
import pandas as pd
from model import PensionTrustModel

os.makedirs("data", exist_ok=True)
results = []

for sp_frac in [0.0, 0.5, 1.0]:
    for init_trust in [0.3, 0.6, 0.9]:
        for rep in range(30):
            model = PensionTrustModel(
                num_citizens=100,
                num_brokers=5,
                initial_trust=init_trust,
                spillover_enabled=(sp_frac > 0),
                spillover_fraction=sp_frac,
                seed=rep + int(sp_frac * 1000) + int(init_trust * 100)
            )
            # 手动运行50步
            for _ in range(50):
                model.step()
            # 获取最终数据
            data = model.datacollector.get_model_vars_dataframe()
            last = data.iloc[-1]
            results.append({
                "spillover_fraction": sp_frac,
                "initial_trust": init_trust,
                "final_trust": last["Avg_Trust"],
                "participation_rate": last["Participation_Rate"]
            })

df = pd.DataFrame(results)
df.to_csv("data/extended_experiment_all_runs.csv", index=False)
print("✅ Done! File saved to data/extended_experiment_all_runs.csv")