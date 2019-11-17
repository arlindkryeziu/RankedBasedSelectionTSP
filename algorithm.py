import random
import numpy as np
class RankedBasedSelection:
    def __init__(self, domain, number_of_population, max_iterations, rank):
        self._domain = domain
        self._number_of_population = number_of_population
        self._max_iterations = max_iterations
        self._rank = rank

    def random_population(self):
        """ Get a random population to evaluate """
        population = []

        for i in range(self._number_of_population):
            cities = [i for i in range(self._domain.shape[0])]
            random.shuffle(cities)
            population.append(cities)

        return population

    def distance(self, city1, city2):
        """ Get the distance between two cities """
        return self._domain[city1][city2]

    def fitness(self, solution):
        temp_solution = 0

        for index in range(len(solution)):
            try:
                temp_solution += self.distance(solution[index], solution[index+1])
            except IndexError:
                temp_solution += self.distance(solution[index], solution[0])
        
        return temp_solution



    def cummulative_probability(self, population):
        cummulative_probability = []
        
        current_population_fitness = sorted([self.fitness(population[i]) for i in range(len(population))])
        
        # Create a list without losing the sort of the population with its cummulative probability calculations
        for i in range(self._number_of_population):
            for j in range(self._number_of_population):
                if self.fitness(population[i]) == current_population_fitness[j]:
                    if i == 0:
                        cummulative_probability.append(((j+1)**self._rank)/(self._number_of_population**self._rank))
                    else:
                        cummulative_probability.append(cummulative_probability[i-1] + (((j+1)**self._rank)/(self._number_of_population**self._rank)))
                    break

        return cummulative_probability


    def commit(self):
        global MAX_ITERATIONS

        global_result = 1000
        global_solution = []
        iteration_normalizer = 0

        while iteration_normalizer < self._max_iterations:
            current_population = self.random_population()

            selected_people = self.rank_selection(current_population)
            currents_population_fitnesses = [self.fitness(selected_people[i]) for i in range(len(selected_people))]
            selected_peoples_best_fitness = min(currents_population_fitnesses)
            current_solution = currents_population_fitnesses.index(selected_peoples_best_fitness)

            if selected_peoples_best_fitness < global_result:
                print(f"""
                ====================
                Improvements 
                Current population: {selected_people}
                ====================
                Best selected: {selected_people[current_solution]}
                Its fitness: {selected_peoples_best_fitness}""")

                global_result = selected_peoples_best_fitness
                global_solution = selected_people[current_solution]
            else:
                iteration_normalizer += 1

        return (global_result, global_solution)

    def rank_selection(self, current_population):
        selected_population = []
        cummulative_probability = self.cummulative_probability(current_population)
        
        # Get a list of population's length with random numbers between first and last cummulative values
        selected_indexes = np.random.uniform(cummulative_probability[0], 
                                                cummulative_probability[len(cummulative_probability)-1], 
                                                self._number_of_population) 

        # Pick the members that the randomized number is between the now and next cummulative probability
        # otherwise get the first element 
        for i in range(self._number_of_population):
            flag = 0
            for j in range(self._number_of_population - 1):
                if cummulative_probability[j] < selected_indexes[i] and cummulative_probability[j+1] >= selected_indexes[i]:
                    selected_population.append(current_population[j])
                    flag = 1
                    break
            
            if flag == 0:
                selected_population.append(current_population[0])

        return selected_population
