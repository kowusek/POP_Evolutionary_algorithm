from __future__ import annotations
from Gene import Gene
from xml.dom.minidom import parse
import numpy as np
import math
from copy import deepcopy

class Population:
    def __init__(self, popSize: int, mutationProb: float, crossProb: float, pathCount: int, modularity: int, iterCount: int) -> None:
        self.nodes = []
        self.links = []
        self.demands = []
        self.demandPaths = []
        self.genes = []
        self.demandKeys = []
        self.probabilities = []
        self.choices = []
        for x in range(popSize):
            self.choices.append(None)
        self.popSize = popSize
        self.mutationProb = mutationProb
        self.crossProb = crossProb
        self.pathCount = pathCount
        self.modularity = modularity
        self.iterCount = iterCount
        self.calculateProbabilities(1,10)
        self.loadData()
        self.initPopulation()
        pass

    def loadData(self) -> None:
        document = parse("graf.xml")
    
        for city in document.getElementsByTagName("node"):
            # self.nodes: ["Warszawa", ...]
            self.nodes.append(city.getAttribute('id'))

        linksDict = {}
        for link in document.getElementsByTagName("link"):
            source = link.getElementsByTagName('source')[0].firstChild.nodeValue
            target = link.getElementsByTagName('target')[0].firstChild.nodeValue
            source = self.nodes.index(source)
            target = self.nodes.index(target)
            # linksDict: {"Link_0_10" : ("Warszawa", "Łódź"), ...}
            linksDict[link.getAttribute("id")] = (source,target)
            # self.links: [(0 - index in self.nodes, 1 - index in self.nodes), ...]
            self.links.append((source,target))

        for demand in document.getElementsByTagName("demand"):
            source = demand.getElementsByTagName('source')[0].firstChild.nodeValue
            target = demand.getElementsByTagName('target')[0].firstChild.nodeValue
            demandValue = demand.getElementsByTagName('demandValue')[0].firstChild.nodeValue
            source = self.nodes.index(source)
            target = self.nodes.index(target)
            # self.demandKeys: [(0 - index in self.nodes, 2 - index in self.nodes), ...]
            self.demandKeys.append((source, target))
            # self.demands: [100, ...]
            self.demands.append(int(demandValue.replace('.0', '')))

            paths = []
            for admissiblePath in demand.getElementsByTagName('admissiblePath'):
                path = []
                for link in admissiblePath.getElementsByTagName('linkId'):
                    tmpLink = linksDict[link.firstChild.nodeValue]
                    index = self.links.index(tmpLink)
                    path.append(index)
                paths.append(path)
            # self.demandPaths: [ path: [ 0 - index in self.links, ...], ...]
            self.demandPaths.append(paths)

    def cross(self, gene: Gene, gene2: Gene) -> None:
        index = np.random.choice(len(gene.data), 1, replace=False)[0]
        tmp = gene2.data[:index].copy()
        gene2.data[:index], gene.data[:index] = gene.data[:index], tmp

    def mutate(self, gene: Gene) -> None:
        elemToMutate = int(len(gene.data) * self.mutationProb)
        indecies = np.random.choice(len(gene.data), elemToMutate)
        for index in indecies:
            gene.data[index] = np.random.dirichlet(np.ones(len(gene.data[index])),size=1).squeeze()

    def calcFitness(self, gene: Gene) -> None:
        links = [0] * len(self.links)
        moduleCount = 0
        for demand, genePaths, paths in zip(self.demands, gene.data, self.demandPaths):
            for value, path in zip(genePaths, paths):
                for link in path:
                    links[link] += value * demand
        for link in links:
            moduleCount += math.ceil(link / self.modularity)
        gene.fitness = moduleCount

    def initGene(self, gene: Gene) -> None:
        demands = []
        for paths in self.demandPaths:
                if self.pathCount > 0 and self.pathCount < len(paths):
                    pathCount = self.pathCount
                else:
                    pathCount = len(paths)
                demands.append(np.random.dirichlet(np.ones(pathCount),size=1).squeeze())
        gene.data = np.array(demands)
    
    def initPopulation(self) -> None:
        for i in range(self.popSize):
            self.genes.append(Gene(self.calcFitness, self.mutate, self.cross, self.initGene))
    
    def calculateProbabilities(self,a,k):
        probabilitiesSum = 0
        for i in range(self.popSize):
            probability = a + k*(1-i/self.popSize)
            probabilitiesSum += probability
            self.probabilities.append(probability)
        for i in range(self.popSize):
            self.probabilities[i] /= probabilitiesSum
    
    def tournamentSelection(self,howMany) -> None:
        self.genes.sort(key=lambda x: x.fitness)
        for x in range(howMany):
            index1 = np.random.choice(len(self.genes), 1, p=self.probabilities, replace=False)[0]
            index2 = np.random.choice(len(self.genes), 1, p=self.probabilities, replace=False)[0]
            choice1 = self.genes[index1]
            choice2 = self.genes[index2]
            if(choice1.fitness < choice2.fitness):
                self.choices[x] = choice1
            else:
                self.choices[x] = choice2
        
    def startEvolution(self):
        bestGene = deepcopy(self.genes[0])
        bestFitness = self.genes[0].fitness
        for i in range(self.iterCount):
            self.tournamentSelection(self.popSize)
            self.genes = self.choices
            for gene in self.genes:
                gene.mutate()
                gene.calcFitness()
                if gene.fitness < bestFitness:
                    bestFitness = gene.fitness
                    bestGene = deepcopy(gene)
            self.genes[0] = bestGene
            print(bestFitness)




if __name__ == "__main__":

    def main():
        p = Population(100, 10, 50, 3, 1, 1000)
        p.tournamentSelection(100)
        print("----------------------------")
        for c in p.choices:
            print(c.fitness)
    if __name__=="__main__":
        main()
