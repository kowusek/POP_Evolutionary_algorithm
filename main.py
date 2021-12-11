from Population import Population
import numpy as np
import time
import cProfile
def main():
    p = Population(100, 0.1, 0.05, 0, 1, 100)
    p.startEvolution()

if __name__=="__main__":
    #cProfile.run('main()')
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))

