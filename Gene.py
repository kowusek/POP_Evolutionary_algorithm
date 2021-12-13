from __future__ import annotations
import random
import copy
class Gene:
    def __init__(self, calculateFitness: function, mutation: function, crossover: function, init: function) -> None:
        self.data = None
        self.fitness = 0
        self.calculateFitness = calculateFitness
        self.mutation = mutation
        self.crossover = crossover
        init(self)
        #self.calcFitness()
    
    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        result.data = copy.deepcopy(self.data)
        result.fitness = copy.deepcopy(self.fitness)
        result.calculateFitness = self.calculateFitness
        result.mutation = self.mutation
        result.crossover = self.crossover
        return result

    def calcFitness(self) -> None:
        self.calculateFitness(self)

    def mutate(self) -> None:
        self.mutation(self)

    def cross(self, gene: Gene) -> None:
        return self.crossover(self, gene)