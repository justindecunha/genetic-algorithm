'''
This class parses the TSP data file, and stores the data in memory to be used by
the rest of the program.
'''


class TSPParser:
    def __init__(self, file_name):
        self.cities = []
        self.distance_dictionary = {}
        with open(file_name, 'r') as file:
            for line in file:
                if line.startswith('NAME'):
                    self.name = line[6:]
                elif line.startswith('DIMENSION'):
                    self.dimension = int(line[11:])
                elif line[0].isdigit():
                    split = line.split()
                    self.cities.append(City(float(split[1]), float(split[2])))


class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y