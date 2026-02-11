"""
Pension Trust ABM with Partial Spillover Support
Author: [xu jie]
Date: 2026
"""

import random
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import numpy as np


class Citizen(Agent):
    """A citizen who decides whether to contribute to the pension fund."""

    def __init__(self, unique_id, model, broker_id, initial_trust):
        super().__init__(unique_id, model)
        self.broker_id = broker_id
        self.trust = initial_trust  # Initial trust in assigned broker

    def step(self):
        """Decide whether to cooperate based on current trust."""
        if self.random.random() < self.trust:
            self.cooperated = True
        else:
            self.cooperated = False


class Broker(Agent):
    """A pension fund broker who may act opportunistically."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        """Broker behaves opportunistically with fixed probability."""
        # In this model, brokers always have incentive to defect
        # Punishment is handled at model level via audit
        pass


class PensionTrustModel(Model):
    """Main model class for pension trust simulation."""

    def __init__(
        self,
        num_citizens=100,
        num_brokers=5,
        initial_trust=0.5,
        spillover_enabled=False,
        spillover_fraction=1.0,  # NEW: fraction of neighbors affected [0.0, 1.0]
        seed=None
    ):
        super().__init__(seed=seed)
        self.num_citizens = num_citizens
        self.num_brokers = num_brokers
        self.initial_trust = initial_trust
        self.spillover_enabled = spillover_enabled
        self.spillover_fraction = max(0.0, min(1.0, spillover_fraction))  # Clamp to [0,1]

        # Scheduler
        self.schedule = RandomActivation(self)

        # Create brokers
        for i in range(self.num_brokers):
            broker = Broker(i, self)
            self.schedule.add(broker)

        # Assign citizens to brokers (balanced)
        citizens_per_broker = self.num_citizens // self.num_brokers
        extra = self.num_citizens % self.num_brokers

        citizen_id = self.num_brokers
        for broker_id in range(self.num_brokers):
            n = citizens_per_broker + (1 if broker_id < extra else 0)
            for _ in range(n):
                citizen = Citizen(citizen_id, self, broker_id, self.initial_trust)
                self.schedule.add(citizen)
                citizen_id += 1

        # Data collector
        self.datacollector = DataCollector(
            model_reporters={
                "FinalTrust": lambda m: np.mean([
                    a.trust for a in m.schedule.agents if isinstance(a, Citizen)
                ]),
                "FinalCooperation": lambda m: np.mean([
                    getattr(a, 'cooperated', False) for a in m.schedule.agents
                    if isinstance(a, Citizen)
                ])
            }
        )

    def punish_broker(self, broker_id):
        """Simulate punishment (e.g., audit reveals misconduct)."""
        # In this model, we assume every broker is punished once per run
        # to trigger spillover mechanism
        self.update_trust_after_punishment(broker_id)

    def update_trust_after_punishment(self, broker_id):
        """Update trust of connected citizens based on spillover fraction."""
        if not self.spillover_enabled:
            return

        # Get all citizens connected to this broker
        affected_citizens = [
            agent for agent in self.schedule.agents
            if isinstance(agent, Citizen) and agent.broker_id == broker_id
        ]

        if not affected_citizens:
            return

        # Determine how many to affect
        num_to_affect = int(len(affected_citizens) * self.spillover_fraction)
        # Ensure at least one if fraction > 0 and there are citizens
        if self.spillover_fraction > 0 and num_to_affect == 0 and affected_citizens:
            num_to_affect = 1

        # Randomly select citizens to lose trust
        selected_citizens = self.random.sample(affected_citizens, num_to_affect)

        for citizen in selected_citizens:
            citizen.trust = 0.0

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()

        # Simulate one punishment event per step (for simplicity)
        # In a more complex model, this could be probabilistic
        punished_broker = self.random.choice(range(self.num_brokers))
        self.punish_broker(punished_broker)

    def run_model(self, n_steps=50):
        """Run the model for n_steps and collect final data."""
        for _ in range(n_steps):
            self.step()
        self.datacollector.collect(self)