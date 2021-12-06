from __future__ import annotations
from Gene import Gene
from xml.dom.minidom import parse

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
        document = parse("graf.xml")
        root = document.documentElement
        cities = document.getElementsByTagName("node")
    
        for city in cities:
            self.nodes.append(city.getAttribute('id'))

        links = document.getElementsByTagName("link")
    
        for link in links:
            source = link.getElementsByTagName('source')[0].firstChild.nodeValue
            target = link.getElementsByTagName('target')[0].firstChild.nodeValue
            self.links_dict[link.getAttribute("id")] = (source,target)
    
        demands = document.getElementsByTagName("demand")
        for demand in demands:
            source = demand.getElementsByTagName('source')[0].firstChild.nodeValue
            target = demand.getElementsByTagName('target')[0].firstChild.nodeValue
            demandValue = demand.getElementsByTagName('demandValue')[0].firstChild.nodeValue
            self.demands_dict[(source,target)] = demandValue
        
            admissiblePaths = demand.getElementsByTagName('admissiblePath')
            paths = []
            for admissiblePath in admissiblePaths:
                path = []
                for link in admissiblePath.getElementsByTagName('linkId'):
                    path.append(link.firstChild.nodeValue)
                paths.append(path)
            self.paths_dict[(source,target)] =paths

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