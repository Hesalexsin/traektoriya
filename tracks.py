import copy
import logging
import math
from abc import ABC, abstractmethod
from datetime import datetime

import edges
import matplotlib.patches
import matplotlib.pyplot as plt
import numpy as np

#global fig, ax
#plt.rcParams.update({'figure.figsize': (5, 5)})
#fig, ax = plt.subplots()


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def args(self):
        return self.x, self.y

    def __del__(self):
        pass


def distance(p1: Point, p2: Point):
    return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5


class Fragment:

    def __init__(self, length: float):
        self.length = length

    def draw(self, ax):
        pass

    def intersect_fl(self, obst):
        pass

    def intersect_fz(self, obst):
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

    def __eq__(self, other):
        if self.d1 == other.d1 and self.d2 == other.d2:
            return True
        else:
            return False

    def draw(self, ax):
        if self.length != np.inf:
            ax.plt.plot(self.d1.args(), self.d2.args())

    def is_inf(self):
        return (self.length == np.inf)


class Arc(Fragment):
    def __init__(self, d1: Point, d2: Point, c: Point, path='short'):
        self.c = c
        self.r = distance(d1, c)
        self.d1 = d1
        self.d2 = d2
        if d1.y >= c.y:
            alpha = math.degrees(math.acos((d1.x - c.x) / self.r))
        else:
            alpha = 360 + math.degrees(math.acos((d1.x - c.x) / self.r))

        if d2.y >= c.y:
            beta = math.degrees(math.acos((d2.x - c.x) / self.r))
        else:
            beta = 360 + math.degrees(math.acos((d2.x - c.x )/ self.r))
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
        self.length = math.pi * 2 * self.r * ((self.beta - self.alpha) / 360)

    def __eq__(self, other):
        if self.d1 == other.d1 and self.d2 == other.d2 and self.c == other.c:
            return True
        else:
            return False

    def intersect_fz(self, obst):
        pass

    def draw(self, ax):
        ax.addpatches(matplotlib.patches.Arc(xy=(self.c.x, self.c.y), width=self.r * 2, height=self.r * 2,
                                             theta1=self.alpha, theta2=self.beta, color='r'))


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
        if useless_part is None:
            return
        i = self.fragments.index(useless_part)
        lens = [x.length for x in new_parts]
        new_trek = self.fragments[:i] + new_parts + self.fragments[i + 1:]
        self.fragments = copy.deepcopy(new_trek)
        self.length = self.length - useless_part.length + sum(lens)

    def find_path(self, obst: dict):
        while True:
            changes = 0
            previous = copy.deepcopy(self.fragments)
            for part in self.fragments:
                # part.intersect_fl(obst['fls'])
                ans = None
                if part is Line:
                    ans= intersect_fz(part, obst['fzs'])
                if ans is not None:
                    self.update(part, ans)
                    changes += 1
            if changes == 0:
                return


def draw(track: Track):
    for x in track.fragments:
        plt.rcParams.update({'figure.figsize': (5, 5)})
        fig, ax = plt.subplots()
        x.draw(ax)
        output_filename = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + '_test_one_circle.png'
        fig.savefig(output_filename, dpi=300)
        logging.info(f"{output_filename} created")


def _find_dodge(self):
    pass


def _fl_dodge_path(self):
    pass


def dodge_fz(line: Line, circ: Arc):
    l1x = circ.c.x - line.d1.x
    l1y = circ.c.y - line.d1.y
    l1 = (l1x ** 2 + l1y ** 2) ** 0.5
    l2x = circ.c.x - line.d2.x
    l2y = circ.c.y - line.d2.y
    l2 = (l2x ** 2 + l2y ** 2) ** 0.5
    t11x = circ.r * math.sin(math.atan2(l1y, l1x) - math.asin(circ.r / l1)) + circ.c.x
    t11y = circ.r * (-1) * math.cos(math.atan2(l1y, l1x) - math.asin(circ.r / l1)) + circ.c.y
    t12x = circ.r * (-1) * math.sin(math.atan2(l1y, l1x) + math.asin(circ.r / l1)) + circ.c.x
    t12y = circ.r * math.cos(math.atan2(l1y, l1x) + math.asin(circ.r / l1)) + circ.c.y
    t21x = circ.r * math.sin(math.atan2(l2y, l2x) - math.asin(circ.r / l2)) + circ.c.x
    t21y = circ.r * (-1) * math.cos(math.atan2(l2y, l2x) - math.asin(circ.r / l2)) + circ.c.y
    t22x = circ.r * (-1) * math.sin(math.atan2(l2y, l2x) + math.asin(circ.r / l2)) + circ.c.x
    t22y = circ.r * math.cos(math.atan2(l2y, l2x) + math.asin(circ.r / l2)) + circ.c.y
    p1, p2, p3, p4 = Point(t11x, t11y), Point(t12x, t12y), Point(t21x, t21y), Point(t22x, t22y)
    a1, a2, a3, a4 = Arc(p1, p3), Arc(p1, p4), Arc(p2, p3), Arc(p2, p4)
    if a1.length == min(a1.length, a2.length, a3.length, a4.length):
        return [Line(line.d1, p1), a1, Line(p3, line.d2)]
    if a2.length == min(a1.length, a2.length, a3.length, a4.length):
        return [Line(line.d1, p1), a2, Line(p4, line.d2)]
    if a3.length == min(a1.length, a2.length, a3.length, a4.length):
        return [Line(line.d1, p2), a3, Line(p3, line.d2)]
    if a4.length == min(a1.length, a2.length, a3.length, a4.length):
        return [Line(line.d1, p2), a4, Line(p4, line.d2)]
    return None


def intersect_fz(line: Line, obst:Arc):
    for circ in obst:
        p1x = line.d1.x - circ.c.x
        p1y = line.d1.y - circ.c.y
        p2x = line.d2.x - circ.c.x
        p2y = line.d2.y - circ.c.y
        a = (p2x - p1x) ** 2 + (p2y - p1y) ** 2
        k = (p2x - p1x) * p1x + (p2y - p1y) * p1y
        c = p1x ** 2 + p1y ** 2 - circ.r ** 2
        d1 = k ** 2 - a * c
        x1 = (-1 * k - d1 ** 0.5) / a
        x2 = (-1 * k + d1 ** 0.5) / a
        if 0 <= x1 <= 1 and 0 <= x2 <= 1:
            return dodge_fz(line, circ)


