import random

from solution import Solution
from evaluation import evaluate_soln
from utils import find_slot


class GASearch:
    def __init__(self, pop_size=1000, mutation_rate=0.05, xover_rate=0.75, soln_len=32, top_n=10):
        self._pop_size = pop_size
        self._mutation_rate = mutation_rate
        self._xover_rate = xover_rate
        self._soln_len = soln_len
        self._top_n = top_n

    def search(self, num_epochs):
        def print_epoch_stats(epoch_num, epoch_fitness, best_fitness):
            print("epoch: {:05d}  avg. fitness: {:0.5f}  best fitness: {:0.5f}".format(epoch_num, epoch_fitness, best_fitness))

        def print_population(population, fitness_values):
            for i in range(len(population)):
                print("{}   {:0.4f}".format(Solution.as_string(population[i]), fitness_values[i]))

        population = self._init_population()
        fitness_values = self._eval_population_fitness(population)
        print_epoch_stats(0, sum(fitness_values) / len(fitness_values), max(fitness_values))
        #print_population(population, fitness_values)

        for epoch_num in range(1, num_epochs + 1):
            #print("at start of epoch {}".format(epoch_num))
            #print_population(population, fitness_values)

            # Reproduction Selection
            parent_indices = self._select_parents(population, fitness_values)

            # Crossover or copy
            child_population = []
            for p1_index, p2_index in parent_indices:
                child1, child2 = Solution.cross(population[p1_index], population[p2_index], r=self._xover_rate)
                child_population.append(child1)
                child_population.append(child2)

            #print("after crossover and copy")
            #print_population(population + child_population, fitness_values + [0.0]*len(child_population))

            # Mutate and repair
            for child in child_population:
                Solution.mutate(child, r=self._mutation_rate)
                Solution.repair(child)

            #print("after mutate and repair")
            #print_population(population + child_population, fitness_values + [0.0] * len(child_population))

            # Evaluate Fitness
            population += child_population
            fitness_values += self._eval_population_fitness(child_population)

            #print("after evaluating fitness")
            #print_population(population, fitness_values)

            # Replacement Selection
            population, fitness_values = self._apply_replacement(population, fitness_values, self._top_n)

            #print("after replacement")
            #print_population(population, fitness_values)
            #print("")

            # Report
            print_epoch_stats(epoch_num, sum(fitness_values) / len(fitness_values), max(fitness_values))
            #print_population(population, fitness_values)

        # Final Report
        print_population(population[:self._top_n], fitness_values[:self._top_n])

    def _init_population(self):
        """
        Initialize a population
        """
        return [Solution.rand(self._soln_len) for _ in range(self._pop_size)]

    @staticmethod
    def _eval_population_fitness(population):
        """
        Evaluate each member fitness for the population.
        Return a list of fitness values for the population.
        """
        return [evaluate_soln(s) for s in population]

    @staticmethod
    def _select_parents(population, fitness_values):
        """
        Selects parent pairs for reproduction using roulette wheel selection.
        Given a population size of N, we select N/2 parent pairs.
        Returns list of pairs of indices (parent1, parent2).
        """
        # Normalize the fitness values so they sum to 1.0
        fitness_normalization_factor = sum(fitness_values)
        normalized_fitness_values = [v / fitness_normalization_factor for v in fitness_values]

        # Sort the solutions and fitness values by decreasing fitness value
        solution_indices_and_fitness_values = list(zip(range(len(population)), normalized_fitness_values))
        solution_indices_and_fitness_values.sort(key=lambda p: p[1], reverse=True)

        # Build the roulette wheel
        roulette_wheel = []
        accumulated_value = 0.0
        for i in range(len(solution_indices_and_fitness_values)):
            accumulated_value += solution_indices_and_fitness_values[i][1]
            roulette_wheel.append(accumulated_value)
        roulette_wheel[-1] = 1.0

        # Select the parent pairs
        parents = []
        while len(parents) < len(population) // 2:
            parents.append((
                solution_indices_and_fitness_values[find_slot(roulette_wheel, 0, len(roulette_wheel) - 1, random.random())][0],
                solution_indices_and_fitness_values[find_slot(roulette_wheel, 0, len(roulette_wheel) - 1, random.random())][0]))

        return parents

    @staticmethod
    def _apply_replacement(population, fitness_values, top_n=1):
        """
        Keeps top n best solutions + uniformly selected random subset of remaining such that total is half of previous.
        Returns the new population and its corresponding fitness values.
        """
        n_to_keep = len(population) // 2 - top_n

        indices_and_fitness_values = sorted(zip(range(len(fitness_values)), fitness_values), key=lambda x: x[1], reverse=True)
        indices_elite = []
        elite_solns = set()
        i = 0
        while len(indices_elite) < top_n:
            soln_index = indices_and_fitness_values[i][0]
            soln = Solution.as_string(population[soln_index])
            if soln not in elite_solns:
                elite_solns.add(soln)
                indices_elite.append(soln_index)
            i += 1

        indices_not_elite = list(set(range(len(population))) - set(indices_elite))
        to_keep = random.sample(indices_not_elite, n_to_keep)
        return [population[i] for i in indices_elite + to_keep], [fitness_values[i] for i in indices_elite + to_keep]
