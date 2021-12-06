import numpy as np
from __future__ import annotations
from main import DEMNADS, EDGE_COUNT, DEMAND_COUNT, PATH_COUNT

class Gene:
    def __init__(self, calculateFitness: function, mutation: function, crossover: function) -> None:
        self.gene = np.array([])
        self.fintess = 0
        self.calculateFitness = calculateFitness
        self.mutation = mutation
        self.crossover = crossover


    def calcFitness(self) -> None:
        self.calculateFitness(self)

    def mutate(self) -> None:
        self.mutation(self)

    def cross(self, gene) -> tuple[Gene, Gene]:
        return self.crossover(self, gene)