from __future__ import annotations
from Gene import Gene
import random

class Population:
    def __init__(self, popSize: int, mutationProb: int, crossProb: int, pathCount: int, modularity: int, iterCount: int) -> None:
        self.genes = None
        self.demandPaths = None
        self.demands = None
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

    def cross(self, gene: Gene) -> tuple[Gene, Gene]:
        subFunctions = (self._cross_aB, self._cross_Ab)
        function = random.choice(subFunctions)
        return function(gene)

    def _cross_aB(self, gene: Gene) -> tuple[Gene, Gene]:
        pass

    def _cross_Ab(self, gene: Gene) -> tuple[Gene, Gene]:
        pass

    def mutate(self) -> None:
        pass

    def calcFitness(self) -> None:
        pass

    def initPopulation(self) -> None:
        pass

    def tournamentSelection(self) -> None:
        pass