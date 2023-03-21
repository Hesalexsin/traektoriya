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
    def __init__(self, mat: np.array, lower_limit: int, lst_edges=[], track=[]):
        self.mat = mat.copy()
        self.lower_limit = lower_limit
        self.lst_edges = lst_edges.copy()
        self.track = track.copy()

        if len(self.lst_edges) > 0:
            self.do_array_ids()

    def __copy__(self):
        return Plan(self.mat.copy(), self.lower_limit,
                    self.lst_edges.copy(), self.track.copy())

    # Compare operands:
    def __verify_data(cls, other):
        if not isinstance(other, (int, Plan)):
            raise TypeError("Right operand must have int or Plan type")
        return other if isinstance(other, int) else other.lower_limit

    def __lt__(self, other):
        return self.lower_limit < self.__verify_data(other)

    def __le__(self, other):
        return self.lower_limit <= self.__verify_data(other)

    # Other:
    def app(self, edge: PairPoints):
        if edge.is_included():
            self.lst_edges.append(edge)

    def inc_limit(self, val: int):
        self.lower_limit += val

    # Functions for completing list with points -> track
    def add_edge_to_track(self, pair: PairPoints):
        if len(self.track) == 0:
            self.track.append(int(pair.id1))
            self.track.append(int(pair.id2))
            self.lst_edges.remove(pair)
        elif self.track[0] == pair.id2 and self.track[-1] != pair.id1:
            self.track = [int(pair.id1)] + self.track
            self.lst_edges.remove(pair)
        elif self.track[-1] == pair.id1 and self.track[0] != pair.id2:
            self.track.append(int(pair.id2))
            self.lst_edges.remove(pair)

    def do_array_ids(self):
        for i in range(len(self.lst_edges)):
            for pair in self.lst_edges:
                self.add_edge_to_track(pair)

    def make_right_order(self, first_id: int):
        for i in range(len(self.track)):
            if self.track[i] == first_id:
                self.track = self.track[i:] + self.track[:i+1]
                break

# Press the green button in the gutter to run the script.
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
