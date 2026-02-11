# run_model.py（可选更新）
from model import CollaborativeGovernanceModel

model = CollaborativeGovernanceModel(
    N=10,
    initial_trust_A=0.7,
    initial_trust_B=0.3,
    enable_negative_spillover=True,   # 👈 现在可以传入
    max_steps=30
)

while model.running:
    model.step()

df = model.datacollector.get_agent_vars_dataframe()
df.to_csv("output.csv")
print("✅ 模型运行完成！")