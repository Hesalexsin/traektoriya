import numpy as np
from numpy import inf


class PairPoints:
    def __init__(self, id1: int, id2: int, is_include: bool):
        self.id1 = id1
        self.id2 = id2
        self.is_include = is_include


class Plan:
    def __init__(self, mat: np.array, lower_limit: int, lst_edges=None, first_id=None,):
        self.mat = mat.copy()
        self.lower_limit = lower_limit
        if lst_edges is None:
            self.lst_edges = {}
        else:
            self.lst_edges = lst_edges.copy()  # {} if lst_edges is None else lst_edges.copy()

        if first_id is None:
            self.first_id = mat[0, 1]
        else:
            self.first_id = first_id

    def __copy__(self):
        return Plan(self.mat.copy(), self.lower_limit,
                    self.lst_edges.copy(), self.first_id)

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
        if edge.is_include:
            if not (edge.id1 in self.lst_edges.keys()):
                self.lst_edges[edge.id1] = edge.id2

    def inc_limit(self, val: int):
        self.lower_limit += val

    # Function for completing list with points -> track
    def do_array_ids(self, id_airport: int):
        key = self.first_id
        track = [int(key)]
        while key in self.lst_edges.keys():
            track.append(int(self.lst_edges[key]))
            copy_key = key
            key = self.lst_edges[key]
            del self.lst_edges[copy_key]

            if not (key in self.lst_edges.keys()) and len(self.lst_edges) != 0:
                new_key = min(self.lst_edges)
                if new_key < 0:
                    key = new_key
        for i in range(len(track)):
            if track[i] < 0:
                track[i] = int(id_airport)
        return track
