# model.py
"""
Voluntary Private Pension (Pillar III) Trust Model with Spillover Effects.
Key features:
- Citizens can switch brokers but cannot withdraw funds (locked-in).
- Citizens may pause contributions if trust falls below threshold.
- Spillover: punishment of one broker affects trust in others.
"""

import random
import numpy as np
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector


class Broker(Agent):
    """Pension product provider (e.g., fund company)."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.misconduct = False  # Whether this broker is punished in current step

    def commit_misconduct(self):
        """Simulate misconduct (e.g., fee misrepresentation)."""
        self.misconduct = True

    def reset(self):
        self.misconduct = False


class Citizen(Agent):
    """Saver in a voluntary pension scheme."""
    def __init__(self, unique_id, model, broker_id, initial_trust):
        super().__init__(unique_id, model)
        self.broker_id = broker_id
        self.trust = initial_trust
        self.is_active = True  # True = still contributing; False = paused (but account locked)

    def decide_participation(self):
        """Pause contributions if trust too low."""
        if self.is_active and self.trust < 0.2:
            self.is_active = False

    def maybe_switch_broker(self):
        """Switch to another broker if still active and conditions met."""
        if not self.is_active:
            return  # Paused citizens don't switch
        
        # Simple switching rule: not implemented here for focus on spillover
        # Could add later based on neighbor trust or performance

    def update_trust_after_punishment(self, spillover_fraction):
        """Update trust when a broker is punished."""
        if spillover_fraction <= 0:
            return

        # Determine if this citizen is affected by spillover
        num_neighbors = self.model.num_citizens // self.model.num_brokers
        num_affected = int(round(spillover_fraction * num_neighbors))
        
        # Simulate random selection of affected citizens per broker
        # For simplicity: use global random draw
        if random.random() < spillover_fraction:
            self.trust = max(0.0, self.trust - 0.1)


class PensionTrustModel(Model):
    def __init__(
        self,
        num_citizens=100,
        num_brokers=5,
        initial_trust=0.6,
        spillover_enabled=False,
        spillover_fraction=1.0,
        seed=None
    ):
        super().__init__()
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        self.num_citizens = num_citizens
        self.num_brokers = num_brokers
        self.initial_trust = initial_trust
        self.spillover_enabled = spillover_enabled
        self.spillover_fraction = spillover_fraction

        self.schedule = RandomActivation(self)
        self.running = True

        # Create brokers
        for i in range(self.num_brokers):
            broker = Broker(i, self)
            self.schedule.add(broker)

        # Assign citizens to brokers evenly
        citizens_per_broker = self.num_citizens // self.num_brokers
        remainder = self.num_citizens % self.num_brokers

        citizen_id = self.num_brokers
        for broker_id in range(self.num_brokers):
            n = citizens_per_broker + (1 if broker_id < remainder else 0)
            for _ in range(n):
                citizen = Citizen(citizen_id, self, broker_id, self.initial_trust)
                self.schedule.add(citizen)
                citizen_id += 1

        # Data collector
        self.datacollector = DataCollector(
            model_reporters={
                "Avg_Trust": lambda m: np.mean([
                    a.trust for a in m.schedule.agents if isinstance(a, Citizen)
                ]),
                "Participation_Rate": lambda m: np.mean([
                    float(a.is_active) for a in m.schedule.agents if isinstance(a, Citizen)
                ])
            }
        )

    def step(self):
        """Advance the model by one step."""
        # Reset all brokers
        for agent in self.schedule.agents:
            if isinstance(agent, Broker):
                agent.reset()

        # Randomly select one broker to punish (simulate scandal)
        broker_agents = [a for a in self.schedule.agents if isinstance(a, Broker)]
        punished_broker = self.random.choice(broker_agents)
        punished_broker.commit_misconduct()

        # Update citizen trust
        for agent in self.schedule.agents:
            if isinstance(agent, Citizen):
                if self.spillover_enabled:
                    agent.update_trust_after_punishment(self.spillover_fraction)
                # Note: even without spillover, direct punishment could reduce trust
                # But for focus, we assume only spillover matters

        # Citizens decide participation and switching
        for agent in self.schedule.agents:
            if isinstance(agent, Citizen):
                agent.decide_participation()
                agent.maybe_switch_broker()

        # Collect data
        self.datacollector.collect(self)