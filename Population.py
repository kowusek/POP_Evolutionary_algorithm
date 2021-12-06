from _typeshed import NoneType
from __future__ import annotations
import numpy as np
from Gene import Gene

class Population:
    def __init__(self, popSize: int, mutationProb: int, crossProb: int, pathCount: int, modularity: int, iterCount: int) -> None:
        self.genes = np.array([])
        self.demandPaths = np.zeros([])
        self.demands = np.zeros([])
        self.popSize = popSize
        self.mutationProb = mutationProb
        self.crossProb = crossProb
        self.pathCount = pathCount
        self.modularity = modularity
        self.iterCount = iterCount
        self.loadData()
        self.initPopulation()

    def loadData(self) -> None:
        pass

    def cross(self, gene) -> tuple[Gene, Gene]:
        pass

    def mutate(self) -> None:
        pass

    def calcFitness(self) -> None:
        pass

    def initPopulation(self) -> None:
        pass

    def tournamentSelection(self) -> None:
        pass