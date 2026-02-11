# run_experiments.py (save all 180 runs)

import pandas as pd
from model import CollaborativeGovernanceModel

trust_A_values = [0.1, 0.5, 0.9]
trust_B_values = [0.2, 0.6, 0.8]
spillover_options = [True, False]
repetitions = 10

all_runs = []  # ← 存储每一次运行，不是平均值

exp_id = 0
for trust_A in trust_A_values:
    for trust_B in trust_B_values:
        for spillover in spillover_options:
            exp_id += 1
            print(f"🧪 Exp {exp_id}/18: A={trust_A}, B={trust_B}, Spill={spillover}")
            
            for rep in range(repetitions):
                model = CollaborativeGovernanceModel(
                    N=10,
                    initial_trust_A=trust_A,
                    initial_trust_B=trust_B,
                    enable_negative_spillover=spillover,
                    max_steps=50
                )
                while model.running:
                    model.step()
                
                df = model.datacollector.get_agent_vars_dataframe()
                final_step = df.index.get_level_values('Step').max()
                final_data = df.xs(final_step, level='Step')
                
                avg_A = final_data[final_data['Group'] == 'A']['Trust'].mean()
                avg_B = final_data[final_data['Group'] == 'B']['Trust'].mean()
                
                # 👇 保存每一次运行，带完整条件
                all_runs.append({
                    'trust_A_initial': trust_A,
                    'trust_B_initial': trust_B,
                    'negative_spillover': spillover,
                    'rep': rep,
                    'avg_trust_A_final': avg_A,
                    'avg_trust_B_final': avg_B
                })

pd.DataFrame(all_runs).to_csv("experiment_all_runs.csv", index=False)
print("\n✅ 所有 180 次运行完成！数据已保存到 experiment_all_runs.csv")