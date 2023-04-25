from travelling_salesman_problem import travel_salesman_problem
import numpy as np


class MatrixDistances:
    def __init__(self, mat: np.array):
        self.mat = mat
        self.firstID = mat[0, 1]
        self.count_add_drones = 0

    def fill_departure_line(self, num: int):
        """
        The function adds line number num to matrix and numerates it
        by NEGATIVE number to mark line, corresponding to the airport
        :param num: number of the added drone/line
        """
        line = self.mat[num, :]
        line[0] = -self.firstID - num
        line[1:self.count_add_drones + 1].fill(np.inf)
        line[self.count_add_drones + 1:] = self.mat[self.count_add_drones + 1, self.count_add_drones + 1:]

    def fill_departure_column(self, num: int):
        """
        The function adds column number num to matrix and numerates it
        by NEGATIVE number to mark line, corresponding to the airport
        :param num: number of the added drone/column
        """
        column = self.mat[:, num]
        column[0] = -self.firstID - num
        column[1:self.count_add_drones + 1] = np.inf
        column[self.count_add_drones + 1:] = self.mat[self.count_add_drones + 1:, self.count_add_drones + 1]

    def matrix_multi_transformation(self, count_drones):
        """
        The function adds needed counts of lines and columns ot matrix for multi_tsp
        :param count_drones: count of AADed drones/ADDed lines sand columns in matrix for multi_tsp
        """
        if count_drones > 0:
            self.mat[0, 1], self.mat[1, 0] = -self.firstID, -self.firstID
            new_mat = np.zeros((len(self.mat) + count_drones, len(self.mat) + count_drones))
            new_mat[0, count_drones + 1:] = self.mat[0, 1:]
            new_mat[count_drones + 1:, 0] = self.mat[1:, 0]
            new_mat[count_drones + 1:, count_drones + 1:] = self.mat[1:, 1:]
            self.mat = new_mat
            self.count_add_drones += count_drones
            for i in range(1, count_drones + 1):
                self.fill_departure_line(i)
                self.fill_departure_column(i)
