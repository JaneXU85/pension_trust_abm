# stat_test.py

import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("experiment_all_runs.csv")

print("🔍 使用 180 次独立运行进行统计检验...\n")

# 统计检验
no_spill_A = df[df['negative_spillover'] == False]['avg_trust_A_final']
with_spill_A = df[df['negative_spillover'] == True]['avg_trust_A_final']

t_A, p_A = stats.ttest_ind(no_spill_A, with_spill_A)
print(f"📊 Group A: p = {p_A:.5f} (n={len(no_spill_A)} per group)")

no_spill_B = df[df['negative_spillover'] == False]['avg_trust_B_final']
with_spill_B = df[df['negative_spillover'] == True]['avg_trust_B_final']

t_B, p_B = stats.ttest_ind(no_spill_B, with_spill_B)
print(f"📊 Group B: p = {p_B:.5f} (n={len(no_spill_B)} per group)")

# ================== LaTeX 表格 ==================
print("\nLaTeX 表格:")
summary = []
for group in ['A', 'B']:
    for spill in [False, True]:
        col = f'avg_trust_{group}_final'
        subset = df[df['negative_spillover'] == spill][col]
        summary.append({
            'Group': group,
            'Condition': 'No Spillover' if not spill else 'With Spillover',
            'Mean': f"{subset.mean():.3f}",
            'SD': f"{subset.std():.3f}",
            'N': len(subset)
        })

table_df = pd.DataFrame(summary)
print(table_df.to_latex(index=False))

# ================== 箱线图 ==================
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
sns.boxplot(data=df, x='negative_spillover', y='avg_trust_A_final')
plt.title('Group A: Final Trust Distribution')

plt.subplot(1, 2, 2)
sns.boxplot(data=df, x='negative_spillover', y='avg_trust_B_final')
plt.title('Group B: Final Trust Distribution')

plt.tight_layout()
plt.savefig("boxplot_trust.png", dpi=300, bbox_inches='tight')
print("\n✅ 箱线图已保存为 boxplot_trust.png")