from xml.dom.minidom import parse, parseString

def main():

    document = parse("graf.xml")
    root = document.documentElement
    cities = document.getElementsByTagName("node")
    nodes = []
    for city in cities:
        nodes.append(city.getAttribute('id'))
    print(nodes)
    print("")

    links = document.getElementsByTagName("link")
    links_dict = {}
    for link in links:
        source = link.getElementsByTagName('source')[0].firstChild.nodeValue
        target = link.getElementsByTagName('target')[0].firstChild.nodeValue
        links_dict[link.getAttribute("id")] = (source,target)
    print(links_dict)
    print("")

    demands_dict = {}
    paths_dict = {}
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

    print(demands_dict)
    print("")
    print(paths_dict)



if __name__=="__main__":
    main()

