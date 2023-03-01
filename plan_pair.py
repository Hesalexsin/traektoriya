import numpy as np
from numpy import inf


'''class Point:
    def __init__(self, id_val=0, x_val=0, y_val=0):
        self.__id = id_val
        self.x = x_val
        self.y = y_val

    ''''''def __init__(self, pnt: Point):
        self.x = pnt.get_x()
        self.y = pnt.get_y()
        self.id = pnt.get_id()''''''

    def get_x(self): return self.x

    def get_y(self): return self.y

    def get_id(self): return self.__id

'''
'''
class Edge:
    def __init__(self, start_pnt=Point(), end_pnt=Point()):
        self.start = Point(start_pnt.get_x(), start_pnt.get_y(), start_pnt.get_id())
        self.end = Point(end_pnt.get_x(), end_pnt.get_y(), end_pnt.get_id())

    def distance(self):
        return ((self.start.get_x() - self.end.get_x()) ** 2 +
                (self.start.get_y() - self.end.get_y()) ** 2) ** 0.5


class Edge_alg(Edge):
    def __init__(self, is_include: bool):
        super.__init__(self)
        self.is_include = is_include

    def is_included(self):
        return self.is_include
'''
'''

def distance(pnt1: Point, pnt2: Point) -> float:
    return ((pnt1.get_x() - pnt2.get_x()) ** 2 +
            (pnt1.get_y() - pnt2.get_y()) ** 2) ** 0.5

'''
class PairPoints:
    def __init__(self, id1: int, id2: int, is_include: bool):
        self.id1 = id1
        self.id2 = id2
        self.is_include = is_include

    def is_included(self):
        return self.is_include

    def id_1(self):
        return self.id1

    def id_2(self):
        return self.id2


class Plan:
    def __init__(self, mat: np.array, lower_limit: int, lst_edges: list, lst_no_edges: list):
        self.mat = mat.copy()
        self.lower_limit = lower_limit
        self.lst_edges = lst_edges.copy()
        self.lst_not_edges = lst_no_edges.copy()

    def __copy__(self):
        return Plan(self.matrix().copy(), self.lower_limit,
                    self.lst_edges.copy(), self.lst_not_edges.copy())

    def low_limit(self):
        return self.lower_limit

    def matrix(self):
        return self.mat

    def edges(self):
        return self.lst_edges

    def app(self, edge: PairPoints):
        if edge.is_included():
            self.lst_edges.append(edge)
        else:
            self.lst_not_edges.append(edge)

    def inc_limit(self, val: int):
        self.lower_limit += val

    def is_in_lst_not_edges(self, edge: PairPoints):
        return edge in self.lst_not_edges


def is_less(plan1: Plan, plan2: Plan):
    return plan1.low_limit() < plan2.low_limit()


def index_min_plan(lst_plans: list):
    index, min_limit = -1, inf
    for i in range(len(lst_plans)):
        if lst_plans[i].low_limit() < min_limit:
            index, min_limit = i, lst_plans[i].low_limit()
    return index

# Press the green button in the gutter to run the script.
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
