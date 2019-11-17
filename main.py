from algorithm import RankedBasedSelection
import numpy as np
from io import StringIO

POPULATION_NUMBER = 10
MAX_ITERATIONS = 5000

def main():
    file = open("p01_d.txt", 'r')
    content = StringIO(f"{file.read()}")

    distances = np.loadtxt(content, dtype = int)
    algorithm = RankedBasedSelection(distances, POPULATION_NUMBER, MAX_ITERATIONS, 1.2)

    print(algorithm.commit())

if __name__ == "__main__":
    main()