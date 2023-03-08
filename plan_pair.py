import numpy as np
from numpy import inf


class PairPoints:
    def __init__(self, id1: int, id2: int, is_include: bool):
        self.id1 = id1
        self.id2 = id2
        self.is_include = is_include

    def is_included(self):
        return self.is_include


class Plan:
    def __init__(self, mat: np.array, lower_limit: int, lst_edges: list): # , lst_no_edges: list
        # mat: np.array, lower_limit: int, lst_edges: list, lst_no_edges: list
        self.mat = mat.copy()
        self.lower_limit = lower_limit
        self.lst_edges = lst_edges.copy()

        # self.lst_not_edges = lst_no_edges.copy()

    def __copy__(self):
        return Plan(self.mat.copy(), self.lower_limit,
                    self.lst_edges.copy())  # , self.lst_not_edges.copy()

    # new
    def __verify_data(cls, other):
        if not isinstance(other, (int, Plan)):
            raise TypeError("Right operand must have int or Plan type")
        return other if isinstance(other, int) else other.lower_limit

    # new
    def __lt__(self, other):
        return self.lower_limit < self.__verify_data(other)

    def app(self, edge: PairPoints):
        if edge.is_included():
            self.lst_edges.append(edge)
        # else: self.lst_not_edges.append(edge)

    def inc_limit(self, val: int):
        self.lower_limit += val

    '''def do_array_ids(self):
        array_ids = []
        for k in range(len(self.lst_edges)):
            for pair in self.lst_edges:
                if len(array_ids) == 0:
                    array_ids.append(pair.id1)
                    array_ids.append(pair.id2)
                    break
                if array_ids[-1] == pair.id1:
                    array_ids.append(pair.id2)
                elif array_ids[0] == pair.id2:
                    array_ids = [pair.id1] + array_ids
        return array_ids'''




# Press the green button in the gutter to run the script.
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
