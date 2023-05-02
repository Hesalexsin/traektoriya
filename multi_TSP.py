from travelling_salesman_problem import travel_salesman_problem
from matrix_processing import MatrixDistances
import numpy as np


def split_into_tracks(tracks: list, id_airport: int) -> list:
    lst_tracks = []
    idx_list = [idx for idx, val in enumerate(tracks) if val == id_airport]
    for k in range(len(idx_list) - 1):
        index1, index2 = idx_list[k], idx_list[k+1]
        lst_tracks.append(tracks[index1: index2 + 1])
    return lst_tracks


def multi_tsp(dist_matrix: np.array, count_drones: int):
    """
    :param dist_matrix: matrix of distances (like in travel_salesman_problem())
    :param count_drones: count of flying apparatus
    :return: array of arrays with tracks for all apparatus
    """
    if count_drones >= len(dist_matrix) - 1:
        raise RuntimeError("Too many drones for this count of control points")
    work_matrix = MatrixDistances(dist_matrix)
    work_matrix.matrix_multi_transformation(count_drones - 1)
    tracks = travel_salesman_problem(work_matrix.mat, work_matrix.firstID)
    return split_into_tracks(tracks, work_matrix.firstID)
