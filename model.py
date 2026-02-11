# model.py

from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from agents import Stakeholder
import random


class CollaborativeGovernanceModel(Model):
    def __init__(self, N=10, initial_trust_A=0.5, initial_trust_B=0.5,
                 enable_negative_spillover=False, max_steps=50):
        # 🔥 必须首先调用父类初始化（解决 _time 和 _steps 问题）
        super().__init__()

        self.num_agents = N
        self.max_steps = max_steps
        self.step_count = 0
        self.running = True
        self.enable_negative_spillover = enable_negative_spillover  # 👈 新增参数

        # 调度器
        self.schedule = RandomActivation(self)
        
        # 创建中介 (ID=0)
        broker = Stakeholder(0, self, is_broker=True)
        self.schedule.add(broker)
        
        # 创建其他主体（A组：奇数ID，B组：偶数ID）
        for i in range(1, N):
            trust = initial_trust_A if i % 2 == 1 else initial_trust_B
            agent = Stakeholder(i, self, trust_level=trust)
            self.schedule.add(agent)
        
        # 初始化信任关系（指向中介）
        for agent in self.schedule.agents:
            if not agent.is_broker:
                agent.initialize_trust_with_broker(broker, agent.trust_level)
        
        # 数据收集器
        self.datacollector = DataCollector(
            model_reporters={"Step": lambda m: m.step_count},
            agent_reporters={"Trust": "trust_level", "Group": "group"}
        )
        self.datacollector.collect(self)

    def step(self):
        self.step_count += 1
        
        # 🔁 更新每个非中介主体的信任水平
        for agent in self.schedule.agents:
            if not agent.is_broker:
                # 基础信任随时间轻微衰减（模拟不确定性）
                agent.trust_level = max(0.0, agent.trust_level - 0.01)
                
                # 负面溢出效应：如果启用且超过第10步
                if self.enable_negative_spillover and self.step_count > 10:
                    agent.trust_level = max(0.0, agent.trust_level - 0.02)
        
        # 执行调度器步骤（目前无个体行为，但保留扩展性）
        self.schedule.step()
        
        # 收集数据
        self.datacollector.collect(self)
        
        # 终止条件
        if self.step_count >= self.max_steps:
            self.running = False