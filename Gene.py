from __future__ import annotations

class Gene:
    def __init__(self, calculateFitness: function, mutation: function, crossover: function, init: function) -> None:
        self.gene = None
        self.fintess = 0
        self.calculateFitness = calculateFitness
        self.mutation = mutation
        self.crossover = crossover
        init(self)
        self.calcFitness()

    def calcFitness(self) -> None:
        self.calculateFitness(self)

    def mutate(self) -> None:
        self.mutation(self)

    def cross(self, gene) -> tuple[Gene, Gene]:
        return self.crossover(self, gene)