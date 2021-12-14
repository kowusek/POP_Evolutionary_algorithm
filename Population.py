from __future__ import annotations
from Gene import Gene
import copy
from xml.dom.minidom import parse
import numpy as np
import math

class Population:
    def __init__(self, popSize: int, agregation: bool) -> None:
        self.best = None
        self.nodes = []
        self.links = []
        self.demands = []
        self.demandPaths = []
        self.genes = []
        self.demandKeys = []
        self.probabilities = []
        self.choices = [0] * (popSize - int(popSize / 10))
        self.popSize = popSize
        self.calculateProbabilities(1,10)
        self.loadData()
        self.initPopulation(agregation)

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
        index = np.random.choice(len(gene.data), 1)[0]
        tmp = gene2.data[:index].copy()
        gene2.data[:index], gene.data[:index] = gene.data[:index], tmp

    def mutate(self, gene: Gene) -> None:
        elemToMutate = int(len(gene.data) * self.mutationProb)
        indecies = np.random.choice(len(gene.data), elemToMutate, replace = False)
        for index in indecies:
            # temp = np.random.uniform(low=0.0, high=10.0, size=len(gene.data[index])).astype(int)
            # temp = temp / temp.sum(0)
            # gene.data[index] = temp
            gene.data[index] = np.random.dirichlet(np.ones(len(gene.data[index])),size=1).squeeze()

    def mutateAgregation(self, gene: Gene) -> None:
        elemToMutate = int(len(gene.data) * self.mutationProb)
        indecies = np.random.choice(len(gene.data), elemToMutate, replace = False)
        for index in indecies:
            temp = np.zeros(len(gene.data[index]))
            indexToFlip = np.random.choice(len(gene.data[index]), 1)
            temp[indexToFlip] = 1
            gene.data[index] = temp

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
                # temp = np.random.uniform(low=0.0, high=10.0, size=len(paths)).astype(int)
                # temp = temp / temp.sum(0)
                # demands.append(temp)
                demands.append(np.random.dirichlet(np.ones(len(paths)),size=1).squeeze())
        gene.data = np.array(demands)
    
    def initGeneAgregation(self, gene: Gene) -> None:
        demands = []
        for paths in self.demandPaths:
                index = np.random.choice(len(paths), 1)
                temp = np.zeros(len(paths))
                temp[index] = 1
                demands.append(temp)
        gene.data = np.array(demands)

    def initPopulation(self, agregation: bool) -> None:
        if agregation:
            for i in range(self.popSize):
                self.genes.append(Gene(self.calcFitness, self.mutateAgregation, self.cross, self.initGeneAgregation))
        else:
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
        chosen = np.random.choice(len(self.genes), howMany*2, p=self.probabilities)
        i = 0
        for x in range(0,howMany*2,2):
            if(self.genes[chosen[x]].fitness < self.genes[chosen[x+1]].fitness):
                self.choices[i] = self.genes[chosen[x]]
            else:
                self.choices[i] = self.genes[chosen[x+1]]
            i = i+1
        #for x in range(howMany):
        #    index1 = np.random.choice(len(self.genes), 1, p=self.probabilities)[0]
        #    index2 = np.random.choice(len(self.genes), 1, p=self.probabilities)[0]
        #    choice1 = self.genes[index1]
        #    choice2 = self.genes[index2]
        #    if(choice1.fitness < choice2.fitness):
        #        self.choices[x] = choice1
        #    else:
        #        self.choices[x] = choice2
        #print("Turniej:")
        #print(self.choices)

    def pairwise(self, iterable):
        a = iter(iterable)
        return zip(a, a)

    def startEvolution(self, mutationProb: float, crossProb: float, iterCount: int, modularity: int):
        self.mutationProb = mutationProb
        self.crossProb = crossProb
        self.iterCount = iterCount
        self.modularity = modularity
        bestGenes = []

        for gene in self.genes:
            gene.calcFitness()

        best = self.genes[0]
        
        for i in range(self.iterCount):
            self.tournamentSelection(self.popSize - int(self.popSize / 10))
            bestGenes = copy.deepcopy(self.genes[:int(self.popSize / 10)])
            self.genes = copy.deepcopy(self.choices)
            elemToCross = int(len(self.genes) * self.crossProb)
            indices = np.random.choice(len(self.genes), elemToCross)
            for a, b in self.pairwise(indices):
                self.genes[a].cross(self.genes[b])
            for gene in self.genes:
                gene.mutate()
                gene.calcFitness()
                if gene.fitness < best.fitness:
                    best = gene
            self.genes += bestGenes
        self.best = best
        return best.fitness

    def evolution(self, mutationProb: float, crossProb: float, iterCount: int, modularity: int):
        self.mutationProb = mutationProb
        self.crossProb = crossProb
        self.iterCount = iterCount
        self.modularity = modularity

        for gene in self.genes:
            gene.calcFitness()

        bestFitness = self.genes[0].fitness

        for i in range(self.iterCount):
            self.tournamentSelection(self.popSize - int(self.popSize / 10))
            bestGenes = copy.deepcopy(self.genes[:int(self.popSize / 10)])
            self.genes = copy.deepcopy(self.choices)
            elemToCross = int(len(self.genes) * self.crossProb)
            indices = np.random.choice(len(self.genes), elemToCross)
            for a, b in self.pairwise(indices):
                self.genes[a].cross(self.genes[b])
            for gene in self.genes:
                gene.mutate()
                gene.calcFitness()
                if gene.fitness < bestFitness:
                    bestFitness = gene.fitness
            self.genes += bestGenes
            yield i, 
    def printBest(self):
        idx = 0
        for demands,keys in zip(self.best.data,self.demandKeys):
            print(self.nodes[keys[0]] +" : "+self.nodes[keys[1]])
            for i,demand in enumerate(demands):
                print("Path "+str(i) +" : "+str(math.ceil(self.demands[idx]*demand)) +" * "+str(len(self.demandPaths[idx][i])) +" = " + str(math.ceil(self.demands[idx]*demand)*len(self.demandPaths[idx][i])))
            idx = idx +1

if __name__ == "__main__":

    def main():
        p = Population(100, 10, 50, 3, 1, 1000)
        p.tournamentSelection(100)
        print("----------------------------")
        for c in p.choices:
            print(c.fitness)
    if __name__=="__main__":
        main()
