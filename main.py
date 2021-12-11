from Population import Population
import numpy as np
import cProfile
def main():
    p = Population(10, 0.1, 0.5, 3, 1, 100)
    p.startEvolution()

if __name__=="__main__":
    cProfile.run('main()')
    main()

