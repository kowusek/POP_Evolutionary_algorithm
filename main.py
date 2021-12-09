from Population import Population
import numpy as np
def main():
    p = Population(100, 10, 50, 3, 1, 1000)
    elements = [1.1, 2.2, 3.3,4.4]
    probabilities = [1, 2, 3,4]
    for i,p in enumerate(probabilities):
        probabilities[i] = probabilities[i]/10
    print(np.random.choice(elements, 10, p=probabilities))

if __name__=="__main__":
    main()

