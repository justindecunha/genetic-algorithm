import pylab as pl
from matplotlib import collections as mc


class Grapher:
    def __init__(self, tsp_data):
        self.x = []
        self.y = []
        self.lc = None
        self.fig, self.ax = pl.subplots()
        for i in tsp_data.cities:
            self.x.append(i.x)
            self.y.append(i.y)
        self.ax.plot(self.x, self.y, 'ko', markersize=4, c='k')
        self.ax.autoscale()
        self.ax.margins(0.1)
        pl.ion()

    def ioff(self):
        pl.ioff()

    def draw_lines_for_city_list(self, city_list, i):
        pl.title("Generation: {}".format(i))
        lines = []
        if self.lc is not None:
            self.lc.remove()
        for i in range(-1, len(city_list) - 1):
            x1 = self.x[city_list[i]]
            y1 = self.y[city_list[i]]
            x2 = self.x[city_list[i + 1]]
            y2 = self.y[city_list[i + 1]]
            lines.append([(x1, y1), (x2, y2)])
        self.lc = mc.LineCollection(lines, color='r', linewidths=1)
        self.ax.add_collection(self.lc)
        pl.pause(0.001)
