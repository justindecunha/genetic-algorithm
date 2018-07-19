import random
import heapq
from statistics import mean
from math import sqrt

#  This class is a representation of a bitmask using an unsigned integer
class RandomBitmask:
    def __repr__(self):
        r = ''
        for bit in range(self.length):
            r += str(1 & (self.mask >> bit))
        return r

    def __init__(self, length):
        self.length = length
        self.mask = random.getrandbits(length)

    # gets the boolean value of the bit specified by the position as a parameter
    def get_bit(self, bit):
        if bit >= self.length:
            raise AssertionError('Outside bounds, generate a longer mask if needed', bit)
        return bool(1 & (self.mask >> bit))


# Represents an individual inside the population
class Individual:
    def __init__(self, length, distance_dictionary):
        self._distance_dictionary = distance_dictionary # A hash table to quickly compute fitness
        self._length = length                           # Length of the individual
        self._fitness = 0                               # Fitness of the individual
        self._path = []                                 # Path of the individual

    def initialize(self):
        self._path = list(range(self._length))
        random.shuffle(self._path)  # Generates a random tsp path
        self.update_fitness()
        return self
    
    def get(self, i):
        return self._path[i]

    # Sets the path, ensures correct path length and updating of fitness
    def set_path(self, path):
        if len(path) != self._length:
            raise AssertionError("Path length is not correct")
        self._path = path
        self.update_fitness()

    # Updates the fitness value
    def update_fitness(self):
        self._fitness = 0
        for i in range(-1, self._length - 1):
            self._fitness += self._distance_dictionary[(self._path[i], self._path[i + 1])]

    # Reciprocal Exchange
    def mutate(self):
        city1 = random.randint(0, self._length - 1)
        city2 = random.randint(0, self._length - 1)
        self._path[city1], self._path[city2] = self._path[city2], self._path[city1]


#  Class representing the population
class Population:
    def __init__(self, max_gen, pop_size, tsp_data,
                 x_type='UOX', x_chance=1,
                 m_type='RE', m_chance=0.1,
                 elitism=True, k=2):
        #  See Genetic Algorithm for a description of these parameters
        self.max_gen = max_gen
        self.pop_size = pop_size
        self.m_type = m_type
        self.m_chance = m_chance
        self.x_type = x_type
        self.x_chance = x_chance
        self.elitism = elitism
        self.k = k

        # TSP data extraction
        self.name = tsp_data.name
        self.length = tsp_data.dimension

        self.distance_dictionary = {}
        self.population = []

        #  Data collected for graphing
        self.best_data = []
        self.average_data = []

        #  Initialize the fitness calculation hash table
        for i in range(self.length):
            for j in range(self.length):
                self.distance_dictionary[(i, j)] = sqrt((tsp_data.cities[i].x - tsp_data.cities[j].x) ** 2 +
                                                        (tsp_data.cities[i].y - tsp_data.cities[j].y) ** 2)

        #  Initialize the population array
        for i in range(pop_size):
            self.population.append(Individual(self.length, self.distance_dictionary).initialize())

    #  Gets the average fitness
    def get_average_fitness(self):
        return mean(individual._fitness for individual in self.population)

    #  Preforms tournament selection
    def tournament_selection(self, k):
        contenders = random.sample(self.population, k)
        return min(contenders, key=lambda x: x._fitness)

    #  Uniform order crossover
    def UOX(self, parent1, parent2):

        # Initializes child paths to same length as parent
        child1_path = [-1] * self.length
        child2_path = [-1] * self.length

        # Initializes two sets to track what cities have been stored so far
        child1_set = set()
        child2_set = set()

        # These two lists are used to fill in the missing spots after to "repair" the paths
        child1_repair = []
        child2_repair = []

        #  Generate a random bitmask
        mask = RandomBitmask(self.length)

        # When a 1 is found in the bitmask, puts value at parent path in child path, and adds said city to the set
        for i in range(self.length):
            if mask.get_bit(i):
                child1_path[i] = parent1.get(i)
                child2_path[i] = parent2.get(i)
                child1_set.add(parent1.get(i))
                child2_set.add(parent2.get(i))

        # In any of the missing positions indicated by -1, sees if we can place the opposite parents position i to the
        # corresponding position in the child, if not, add to the repair list
        for i in range(self.length):
            if parent2.get(i) not in child1_set:
                if child1_path[i] == -1:
                    child1_path[i] = parent2.get(i)
                else:
                    child1_repair.append(parent2.get(i))
            if parent1.get(i) not in child2_set:
                if child2_path[i] == -1:
                    child2_path[i] = parent1.get(i)
                else:
                    child2_repair.append(parent1.get(i))

        # Iterates through the repair list and places it as close as it can to where it should have been in the child
        for i in range(self.length):
            if child1_path[i] == -1:
                child1_path[i] = child1_repair.pop(0)
            if child2_path[i] == -1:
                child2_path[i] = child2_repair.pop(0)

        # adds the paths inside the Individual wrapper to create the children of the parents
        child1 = Individual(self.length, self.distance_dictionary)
        child1.set_path(child1_path)
        child2 = Individual(self.length, self.distance_dictionary)
        child2.set_path(child2_path)

        return [child1, child2]

    def OX(self, parent1, parent2):

        #  Randomly selects start and end points
        start_point = random.randint(0, self.length - 1)
        end_point = random.randint(0, self.length - 1)

        #  ensures start point is always before end point
        if start_point > end_point:
            start_point, end_point = end_point, start_point

        child1_path = [-1] * self.length
        child2_path = [-1] * self.length

        child1_set = set()
        child2_set = set()

        #  Copies values from parent to child from start --> end
        for i in range(start_point, end_point):
                child1_path[i] = parent1.get(i)
                child2_path[i] = parent2.get(i)
                child1_set.add(parent1.get(i))
                child2_set.add(parent2.get(i))

        # Used to remember position where child needs to be placed
        ptr1 = end_point
        ptr2 = end_point

        #  loops through the entire parent list, using the end point as a starting place, going back to beginning when
        #  off the list
        for i in range(end_point, end_point + self.length):
            next_parent2 = parent2.get(i % self.length) #  modulus to loop around when off the list
            if next_parent2 not in child1_set:          #  if its not in the child, add to the next spot in child indicated by prt's
                child1_set.add(next_parent2)
                child1_path[ptr1] = next_parent2
                ptr1 = (ptr1 + 1) % self.length

            next_parent1 = parent1.get(i % self.length)
            if next_parent1 not in child2_set:
                child2_set.add(next_parent1)
                child2_path[ptr2] = next_parent1
                ptr2 = (ptr2 + 1) % self.length

        child1 = Individual(self.length, self.distance_dictionary)
        child1.set_path(child1_path)
        child2 = Individual(self.length, self.distance_dictionary)
        child2.set_path(child2_path)

        return [child1, child2]

    # creates the next generation based on the previous generation, using all the methods above to achieve this
    def next_generation(self):
        next_gen = []

        #  Elitism, adds # of populations fittest members to the next generation for being so elite
        if self.elitism != 0:
            next_gen = heapq.nsmallest(self.elitism, self.population, key=lambda x: x._fitness)

        # loops until population is filled
        while len(next_gen) < self.pop_size:
            # Selects parents based on a tournament held between k members of population
            parent1 = self.tournament_selection(self.k)
            parent2 = self.tournament_selection(self.k)

            #  Preforms crossover on selected parents, if it procs based on x_chance
            if random.random() < self.x_chance:
                if self.x_type == 'UOX':
                    children = self.UOX(parent1, parent2)
                elif self.x_type == 'OX':
                    children = self.OX(parent1, parent2)
            else:
                children = [parent1, parent2]

            #  Mutates the children if it procs based on m_chance
            for child in children:
                if random.random() < self.m_chance:
                    child.mutate()
                next_gen.append(child)

        # Best and avg data stored for graphing and analysis purposes
        self.best_data.append(self.population[0]._fitness)
        self.average_data.append(self.get_average_fitness())

        #  finally sets the newly generated population as the actual population, preparing for the next generation
        self.population = next_gen


