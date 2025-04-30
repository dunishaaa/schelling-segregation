import numpy as np
from enum import Enum
import matplotlib.pyplot as plt


class Race(Enum):
    BLACK = 0
    WHITE = 1
    YELLOW = 1


class Agent:
    def __init__(self, x,  y, race: Race):
        self.x = x
        self.y = y
        self.race: Race = race
        self.discomfort 

    def calculate_discomfort(self):
        return 0


POPULATION = 20
PROPORTION = 0.3

if __name__ == "__main__":
    for i in range(POPULATION*0.3):
        agents = [Agent(np.random.rand(1), np.random.rand(1), Race.BLACK)]

    for i in range(POPULATION*(1.0 - 0.3)):
        agents = [Agent(np.random.rand(1), np.random.rand(1), Race.BLACK)]
