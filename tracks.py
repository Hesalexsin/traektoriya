import copy
import math
from abc import ABC, abstractmethod
import edges
import matplotlib.patches
import matplotlib.pyplot as plt
import numpy as np

global fig, ax
plt.rcParams.update({'figure.figsize': (5, 5)})
fig, ax = plt.subplots()


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def args(self):
        return self.x, self.y

    def __del__(self):
        pass


def distance(p1: Point, p2: Point):
    return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5


class Fragment:

    def __init__(self, length: float):
        self.length = length

    def draw(self):
        pass


class Line(Fragment):
    def __init__(self, d1: Point, d2: Point, is_inf=False):
        if not is_inf:
            self.d1 = d1
            self.d2 = d2
            self.length = distance(d1, d2)
        else:
            self.d1 = np.inf
            self.d2 = np.inf
            self.length = np.inf

    def draw(self):
        if self.length != np.inf:
            return plt.plot(self.d1.args(), self.d2.args())
        else:
            return None

    def is_inf(self):
        return (self.length == np.inf)


class Arc(Fragment):
    def __init__(self, d1: Point, d2: Point, c: Point, path='short'):
        self.c = c
        self.r = distance(d1, c)
        self.d1 = d1
        self.d2 = d2
        if d1.y >= c.y:
            alpha = math.degrees(math.acos(d1.x - c.x / self.r))
        else:
            alpha = 360 + math.degrees(math.acos(d1.x - c.x / self.r))

        if d2.y >= c.y:
            beta = math.degrees(math.acos(d2.x - c.x / self.r))
        else:
            beta = 360 + math.degrees(math.acos(d2.x - c.x / self.r))
        if path == 'short':  # TODO shorter comparison
            if alpha - beta <= 180:
                self.alpha = alpha
                self.beta = beta
            else:
                self.alpha = beta
                self.beta = alpha
        else:
            if alpha - beta <= 180:
                self.alpha = beta
                self.beta = alpha
            else:
                self.alpha = alpha
                self.beta = beta

    def draw(self):
        global ax
        return matplotlib.patches.Arc(xy=(self.c.x, self.c.y), width=self.r * 2, height=self.r * 2,
                                      theta1=self.alpha, theta2=self.beta, color='r')


class Track:
    def __init__(self, is_inf=False, *parts: Fragment):
        if not is_inf:
            self.fragments = []
            self.length = 0
            for part in parts:
                self.fragments.append(part)
                self.length += part.length
        else:
            self.fragments = [Line(0, 0, True)]
            self.length = np.inf

    def update(self, useless_part, *new_parts):

        i = self.fragments.index(useless_part)
        lens = [x.length for x in new_parts]
        new_trek = self.fragments[:i] + new_parts + self.fragments[i + 1:]
        self.fragments = copy.deepcopy(new_trek)
        self.length = self.length - useless_part.length + sum(lens)

    def find_path(self, obst: dict):
        while True:
            changes = 0
            for part in self.fragments:
                ans = is_intersect_fl(part,obst['fls'])
                if ans is not None:
                    changes += 1
                    self.update(part, ans)
                ans = is

    def draw(self):
        return [x.draw() for x in self.fragments]
    def _find_dodge(self):
        pass

    def _fl_dodge_path(self):
        pass

def is_intersect_fz(part: Fragment):
        pass

def _is_intersect_geo(part: Fragment):
        pass




def is_intersect_fl(part: Line, fls: dict):
    for fl in fls:
        if edges.is_intersect(part.d1, part.d2, fl.d1, fl.d2):
            if Track(part.d1, fl.d1).length + Track(fl.d1, part.d2).length < Track(part.d1, fl.d2).length + Track(fl.d2,
                                                                                                                  part.d2).length:
                return [Track(part.d1, fl.d1), Track(fl.d1, part.d2)]
            else:
                return [Track(part.d1, fl.d2), Track(fl.d2, part.d2)]
        else:
            return None

