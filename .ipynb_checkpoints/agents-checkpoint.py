import random
from mesa import Agent

class Stakeholder(Agent):
    def __init__(self, unique_id, model, power=None, trust_level=0.5, is_broker=False):
        super().__init__(unique_id, model)
        self.power = power if power is not None else random.uniform(0.5, 1.5)
        self.trust_level = trust_level
        self.is_broker = is_broker
        self.group = "Broker" if is_broker else ("A" if unique_id % 2 == 1 else "B")
    
    def initialize_trust_with_broker(self, broker, initial_trust):
        self.trust_in_broker = initial_trust