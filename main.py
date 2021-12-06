from xml.dom.minidom import parse, parseString
import numpy as np

EDGE_COUNT = 12
DEMAND_COUNT = 66
DEMAND_PATHS = np.zeros([])
DEMNADS = np.zeros([])
PATH_COUNT = 2
MODULARITY = 0

nodes = []
links_dict = {}
demands_dict = {}
paths_dict = {}

def main():
    parseXMLFile("graf.xml")

    print(nodes)
    print("")
    print(links_dict)
    print("")
    print(demands_dict)
    print("")
    print(paths_dict)
    print("")
def parseXMLFile(fileName):

    document = parse("graf.xml")
    root = document.documentElement
    cities = document.getElementsByTagName("node")
    
    for city in cities:
        nodes.append(city.getAttribute('id'))

    links = document.getElementsByTagName("link")
    
    for link in links:
        source = link.getElementsByTagName('source')[0].firstChild.nodeValue
        target = link.getElementsByTagName('target')[0].firstChild.nodeValue
        links_dict[link.getAttribute("id")] = (source,target)
    
    demands = document.getElementsByTagName("demand")
    for demand in demands:
        source = demand.getElementsByTagName('source')[0].firstChild.nodeValue
        target = demand.getElementsByTagName('target')[0].firstChild.nodeValue
        demandValue = demand.getElementsByTagName('demandValue')[0].firstChild.nodeValue
        demands_dict[(source,target)] = demandValue
        
        admissiblePaths = demand.getElementsByTagName('admissiblePath')
        paths = []
        for admissiblePath in admissiblePaths:
            path = []
            for link in admissiblePath.getElementsByTagName('linkId'):
                path.append(link.firstChild.nodeValue)
            paths.append(path)
        paths_dict[(source,target)] =paths

if __name__=="__main__":
    main()

