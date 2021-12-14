from Population import Population
import numpy as np
import time
import cProfile
def main():
    p = Population(10, False)
    p.startEvolution(0.02, 8.0, 100, 1)
    p.printBest()

if __name__=="__main__":
    #cProfile.run('main()')
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))

