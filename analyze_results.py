# analyze_results.py

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 读取实验结果
df = pd.read_csv("experiment_summary.csv")

print("📊 实验结果概览:")
print(df.head())

# 设置绘图风格
sns.set(style="whitegrid")
plt.figure(figsize=(14, 5))

# 图1: 初始A信任 vs 最终A信任（按溢出效应分色）
plt.subplot(1, 2, 1)
sns.scatterplot(
    data=df,
    x='trust_A_initial', y='avg_trust_A_final',
    hue='negative_spillover',
    style='trust_B_initial',
    palette='Set1',
    s=100
)
plt.title('Group A: Initial vs Final Trust')
plt.xlabel('Initial Trust (A)')
plt.ylabel('Final Average Trust (A)')

# 图2: 初始B信任 vs 最终B信任（按溢出效应分色）
plt.subplot(1, 2, 2)
sns.scatterplot(
    data=df,
    x='trust_B_initial', y='avg_trust_B_final',
    hue='negative_spillover',
    style='trust_A_initial',
    palette='Set2',
    s=100
)
plt.title('Group B: Initial vs Final Trust')
plt.xlabel('Initial Trust (B)')
plt.ylabel('Final Average Trust (B)')

plt.tight_layout()
plt.savefig("trust_analysis.png", dpi=300, bbox_inches='tight')
plt.show()

print("\n✅ 分析图表已保存为 trust_analysis.png")