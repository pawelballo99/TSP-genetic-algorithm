import glob
import os
import random
import numpy as np
import tsplib95

from individual import Individual


def distance(city_A, city_B):
    return np.sqrt(np.square(city_A[0] - city_B[0]) + np.square(city_A[1] - city_B[1]))


def load_cities(nr_file):
    try:
        city_file = glob.glob(os.getcwd() + "/data_cities/*.tsp")[nr_file]
        city = tsplib95.load(city_file)
        return city.node_coords

    except IndexError:
        print("List of files is too small")


class Population:
    def __init__(self, nr_file, mutation_rate, nr_individuals):
        self.n = nr_individuals
        self.mutation_rate = mutation_rate
        self.current_best = 0
        self.current_best_route = []
        self.global_best = 0
        self.global_best_route = []
        self.all_cities = load_cities(nr_file)
        self.population = self.create_population()
        self.parents = []

    def create_population(self):
        individuals = []
        for i in range(self.n):
            individuals.append(Individual(len(self.all_cities)))
        return individuals

    def fitness_calculation(self):
        for ind in self.population:
            dist = 0
            for i in range(1, len(ind.genome)):
                dist += distance(self.all_cities[ind.genome[i - 1]], self.all_cities[ind.genome[i]])
            dist += distance(self.all_cities[ind.genome[-1]], self.all_cities[ind.genome[0]])
            ind.cost = 1 / dist
        self.current_best = max([ind.cost for ind in self.population])
        idx = [ind.cost for ind in self.population].index(self.current_best)
        self.current_best_route = [self.all_cities[city] for city in self.population[idx].genome]
        if self.current_best > self.global_best:
            self.global_best = self.current_best
            self.global_best_route = self.current_best_route

    def selection(self):
        ranks = [[y for y in self.population if y.cost == x] for x in
                 sorted(set(map(lambda x: x.cost, self.population)))]
        N = len(ranks)

        probabilities = []
        for i in range(N):
            probabilities.append((i + 1) / ((N + 1) * N / 2))
        cum_sum = list(np.array(probabilities).cumsum())
        for i in range(self.n):
            r = random.uniform(0, 1)
            for elem in cum_sum:
                if r <= elem:
                    self.parents.append(random.choice(ranks[cum_sum.index(elem)]))
                    break

    def crossing(self):
        self.population = []
        for i in range(int(self.n / 2)):
            parent1 = random.choice(self.parents)
            self.parents.remove(parent1)
            parent2 = random.choice(self.parents)
            self.parents.remove(parent2)
            if random.uniform(0, 1) < 0.75:
                offspring1, offspring2 = self.offspring(parent1, parent2)
                self.population.append(offspring1)
                self.population.append(offspring2)
            else:
                self.population.append(parent1)
                self.population.append(parent2)

    def ox_crossover(self, parent_A, parent_B):
        offspring_genome_A = len(self.all_cities) * [None]
        offspring_genome_B = len(self.all_cities) * [None]
        pkt1, pkt2 = int(random.random() * len(parent_A.genome)), int(random.random() * len(parent_A.genome))
        start_gen, stop_gen = min(pkt1, pkt2), max(pkt1, pkt2)
        offspring_genome_A[start_gen:stop_gen] = parent_A.genome[start_gen:stop_gen]
        offspring_genome_B[start_gen:stop_gen] = parent_B.genome[start_gen:stop_gen]

        parent_B_genome = list(filter(lambda a: a not in parent_A.genome[start_gen:stop_gen], parent_B.genome))
        parent_A_genome = list(filter(lambda a: a not in parent_B.genome[start_gen:stop_gen], parent_A.genome))

        offspring_genome_A[stop_gen:] = parent_B_genome[:(len(self.all_cities)-stop_gen)]
        offspring_genome_A[:start_gen] = parent_B_genome[(len(self.all_cities)-stop_gen):]
        offspring_genome_B[stop_gen:] = parent_A_genome[:(len(self.all_cities) - stop_gen)]
        offspring_genome_B[:start_gen] = parent_A_genome[(len(self.all_cities) - stop_gen):]

        return offspring_genome_A, offspring_genome_B

    def offspring(self, parent_A, parent_B):
        offspring_genome_A, offspring_genome_B = self.ox_crossover(parent_A, parent_B)
        parent_A.genome = offspring_genome_A
        parent_B.genome = offspring_genome_B
        if random.uniform(0, 1) < self.mutation_rate:
            parent_A.mutate()
        if random.uniform(0, 1) < self.mutation_rate:
            parent_B.mutate()

        return parent_A, parent_B
