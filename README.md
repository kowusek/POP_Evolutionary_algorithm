# Genetic Algorithm for Network Demand Optimization

This repository contains a Python implementation of a genetic algorithm designed to optimize network demand routing. It models a population of candidate solutions (`Gene`s) representing different traffic distributions across admissible paths in a network. The algorithm evolves the population to minimize modular link usage, effectively balancing network load.

---

## Table of Contents

* [Overview](#overview)
* [Files](#files)
* [Installation](#installation)
* [Usage](#usage)
* [Algorithm Details](#algorithm-details)
* [Parameter Tuning and Experiments](#parameter-tuning-and-experiments)
* [Classes and Methods](#classes-and-methods)
* [Example](#example)

---

## Overview

The project uses a genetic algorithm to solve a network routing optimization problem. Each `Gene` represents a potential allocation of network traffic across multiple paths for different demands. The `Population` class manages a population of `Gene`s and applies genetic operators (mutation, crossover, and selection) to evolve solutions over multiple iterations.

Key features:

* Supports both probabilistic distribution (`dirichlet`) and aggregated path allocation.
* Implements tournament selection for parent selection.
* Calculates fitness based on modularity of network links.
* Allows visualization of evolution progress using `matplotlib`.

---

## Files

* **main.py**: Entry point of the program. Initializes a population, starts evolution, and prints the best solution.
* **Population.py**: Implements the `Population` class which manages genes, performs evolution, and computes fitness. Loads network topology and demand data from `graf.xml`.
* **Gene.py**: Implements the `Gene` class representing a candidate solution. Handles mutation, crossover, and fitness evaluation.

---

## Installation

1. Clone the repository:

```bash
git clone <repository_url>
cd <repository_directory>
```

2. Install dependencies (requires Python 3.8+):

```bash
pip install numpy matplotlib tqdm ipython
```

3. Ensure your network data file `graf.xml` is in the same directory as the scripts. It should define nodes, links, and demands.

---

## Usage

Run the main program:

```bash
python main.py
```

The program will:

1. Load the network topology and demand data from `graf.xml`.
2. Initialize a population of candidate solutions.
3. Perform genetic evolution over a specified number of iterations.
4. Print the best solution with path allocations and modularity cost.

### Real-time Visualization Example

You can visualize evolution progress using `matplotlib` and `tqdm`:

```python
from Population import Population
import matplotlib.pyplot as plt
from tqdm import tqdm
from IPython import display

population = Population(popSize=100, agregation=False)
moduleCount = []

for x, y in tqdm(population.evolution(mutationProb=0.1, crossProb=0.8, iterCount=10000, modularity=1), total=10000):
    moduleCount.append(y)
    if x % 100 == 0:
        display.clear_output(wait=True)
        plt.plot(moduleCount, label='Module count')
        plt.legend()
        plt.grid()
        plt.show()
```

This allows you to monitor the module count as the algorithm optimizes the network.

---

## Algorithm Details

1. **Initialization**:

   * Each `Gene` is initialized with a random traffic distribution across admissible paths.
   * `Population` holds `popSize` genes.

2. **Fitness Calculation**:

   * Fitness is computed as the sum of modular link usage, i.e., `ceil(link_load / modularity)` for all links.

3. **Selection**:

   * Tournament selection with probabilities favors fitter genes.

4. **Crossover and Mutation**:

   * Crossover exchanges parts of two genes.
   * Mutation modifies gene data randomly (`dirichlet` or aggregation).

5. **Evolution Loop**:

   * Selection → Crossover → Mutation → Fitness evaluation → Update best gene.

---

## Parameter Tuning and Experiments

Extensive experiments were performed to tune algorithm parameters:

1. **Population Size**

   * Boxplots showed that increasing population above 400 individuals did not significantly improve convergence speed or solution quality.
   * Optimal population size found to be around **800** for long runs.

2. **Mutation Probability**

   * Tested values from 0% to 10%.
   * Optimal mutation probability: **2%**.

3. **Crossover Probability**

   * Tested values from 0% to 200%.
   * Optimal crossover probability: **100%** or higher, depending on distribution scaling.

4. **Iteration Count**

   * Longer runs (`iterCount=10000`) allow the algorithm to better explore the solution space.

5. **Visualization of Progress**

   * Progress of module count over iterations is plotted for each run.
   * Boxplots and bar charts were used to analyze the effect of population size, mutation, and crossover on the final fitness values.

These experiments help determine the best combination of parameters for efficient convergence while minimizing runtime.

---

## Classes and Methods

### `Gene`

* **Methods**:

  * `calcFitness()`: Calculates the fitness of the gene.
  * `mutate()`: Applies mutation to the gene.
  * `cross(other_gene)`: Applies crossover with another gene.

### `Population`

* **Methods**:

  * `startEvolution(mutationProb, crossProb, iterCount, modularity)`: Evolves population and returns best fitness.
  * `evolution(mutationProb, crossProb, iterCount, modularity)`: Generator version of evolution with real-time progress tracking.
  * `printBest()`: Prints the best solution with paths and traffic allocations.

* **Internal Methods**:

  * `loadData()`: Loads network nodes, links, and demands from `graf.xml`.
  * `initPopulation()`: Initializes genes based on aggregation setting.
  * `calcFitness(gene)`: Computes fitness for a given gene.
  * `mutate(gene)`, `mutateAgregation(gene)`: Mutation operators.
  * `cross(gene1, gene2)`: Performs crossover.
  * `tournamentSelection(howMany)`: Performs tournament selection.

---

## Example Output

```
Warszawa : Łódź
Path 0 : 30 * 3 = 90
Path 1 : 70 * 2 = 140
...
```

This shows the allocation of demand for each node pair across admissible paths, along with the modular cost.
