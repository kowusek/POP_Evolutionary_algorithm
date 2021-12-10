from __future__ import annotations
from Gene import Gene
import random
from xml.dom.minidom import parse
import numpy as np

class Population:
    def __init__(self, popSize: int, mutationProb: int, crossProb: int, pathCount: int, modularity: int, iterCount: int) -> None:
        self.nodes = []
        self.links = []
        self.demands = {}
        self.paths = {}
        self.genes = []
        self.popSize = popSize
        self.mutationProb = mutationProb
        self.crossProb = crossProb
        self.pathCount = pathCount
        self.modularity = modularity
        self.iterCount = iterCount
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
            # self.demands: {(0 - index in self.nodes, 2 - index in self.nodes) : 100}
            self.demands[(source, target)] = demandValue

            paths = []
            for admissiblePath in demand.getElementsByTagName('admissiblePath'):
                path = []
                for link in admissiblePath.getElementsByTagName('linkId'):
                    tmpLink = linksDict[link.firstChild.nodeValue]
                    index = self.links.index(tmpLink)
                    path.append(index)
                paths.append(path)
            # self.paths: {(0 - index in self.nodes, 2 - index in self.nodes) : [[ 0 - index in self.links, ...], ...]}
            self.paths[(source,target)] = paths

    def cross(self, gene: Gene) -> tuple[Gene, Gene]:
        subFunctions = (self._crossFirst, self._crossSecond)
        function = random.choice(subFunctions)
        return function(gene)

    def _crossFirst(self, gene: Gene, gene2: Gene) -> tuple[Gene, Gene]:
        pass

    def _crossSecond(self, gene: Gene, gene2: Gene) -> tuple[Gene, Gene]:
        pass

    def mutate(self, gene: Gene) -> None:
        pass

    def calcFitness(self, gene: Gene) -> None:
        links = np.zeros(len(self.links))
        for demand in gene.data:
            pass

    def initGene(self, gene: Gene) -> None:
        demands = []
        for demand in self.demands:
                if self.pathCount > 0 and self.pathCount < len(self.paths[demand]):
                    pathCount = self.pathCount
                else:
                    pathCount = len(self.paths[demand])
                demands.append(np.random.dirichlet(np.ones(pathCount),size=1).squeeze())
        gene.data = np.array(demands)
    
    def initPopulation(self) -> None:
        for i in range(self.popSize):
            self.genes.append(Gene(self.calcFitness, self.mutate, self.cross, self.initGene))

    def tournamentSelection(self,a,k,howMany) -> None:
        probabilities = []
        self.genes.sort(key=lambda x: x.fitness)
        probabilitiesSum = 0
        for idx,gene in enumerate(self.genes):
            probability = a + k*(1-idx/self.popSize)
            probabilitiesSum = probabilitiesSum+ probability
            probabilities.append(probability)
        for idx,probability in enumerate(probabilities):
            probabilities[idx] = probabilities[idx]/probabilitiesSum
        choices = []
        for x in range(howMany):
            choice1 = np.random.choice(self.genes, 1, p=probabilities).item(0)
            choice2 = np.random.choice(self.genes, 1, p=probabilities).item(0)
            if(choice1.fitness < choice2.fitness):
                choices.append(choice1)
            else:
                choices.append(choice2)
        return choices
        

if __name__ == "__main__":

    def main():
        p = Population(100, 10, 50, 3, 1, 1000)
        choices = p.tournamentSelection(1,10,10)
        print("----------------------------")
        for c in choices:
            print(c.fitness)
    if __name__=="__main__":
        main()
