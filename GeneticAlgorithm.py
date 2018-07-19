from GeneticObjects import Population
from TSPParser import TSPParser
import random

display = True  # Set true if you want to display paths and statistical data graphically

if display is True:
    import GAStatDisplay
    from GUI3 import Grapher

seed = random.random()  # Randomly generated seed
random.seed(seed)  # Sets the seed, can use randomly generated one, or set this parameter yourself
k = 2  # The number of contenders in the tournament selection
max_gen = 500  # The number of generations to run the GA for
pop_size = 500  # The size of the population used in the GA
elitism = int(pop_size * 0.1)  # The number of elite to copy into the next generation use int(pop_size*float) to get %'s
x_type = 'UOX'  # The type of crossover used - OX for ordered, UOX for uniform-order
m_type = 'RE'  # The type of mutation used - currently only supports reciprocal exchange
x_chance = 1  # The chance crossover occurs
m_chance = 0.01  # The chance mutation occurs
file_name = 'dj38.tsp'  # The name of the file to use - should be formatted similar to the example files

tsp_data = TSPParser('datasets//' + file_name)  # Parse file data

if display is True:
    displayer = Grapher(tsp_data)  # the displayer

# Population initialized as p
p = Population(max_gen, pop_size, tsp_data, x_type, x_chance, m_type, m_chance, elitism, k)

print("GA Parameters:")
print('k: ', k)
print('Max Generations: ', max_gen)
print('Population Size: ', pop_size)
print('Number of elite: ', elitism)
print('Crossover Type: ', x_type)
print('Crossover Chance: ', x_chance)
print('Mutation Chance: ', m_chance)
print('Data Set: ', tsp_data.name)
print('Average fitness of initialized population:', p.get_average_fitness())

#  The GA generational loop
for i in range(max_gen):
    p.next_generation()
    if display is True:
        displayer.draw_lines_for_city_list(p.population[0]._path, i)

print('Average fitness of population after evolution: ', p.get_average_fitness())
if display is True:
    displayer.ioff()
    GAStatDisplay.graph_data(p.best_data, p.average_data)
