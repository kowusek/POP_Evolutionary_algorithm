from Population import Population
import numpy as np
import time
import cProfile
def main():
    p = Population(100, 0)
    p.startEvolution(0.1, 0.8, 10000, 1)

if __name__=="__main__":
    #cProfile.run('main()')
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))

