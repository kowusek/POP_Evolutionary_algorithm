from __future__ import annotations
import random
class Gene:
    def __init__(self, calculateFitness: function, mutation: function, crossover: function, init: function) -> None:
        self.data = None
        self.fitness = 0
        self.calculateFitness = calculateFitness
        self.mutation = mutation
        self.crossover = crossover
        init(self)
        self.calcFitness()

    def calcFitness(self) -> None:
        self.fitness = random.randint(1, 100)
        #self.calculateFitness(self)

    def mutate(self) -> None:
        self.mutation(self)

    def cross(self, gene: Gene) -> tuple[Gene, Gene]:
        return self.crossover(self, gene)