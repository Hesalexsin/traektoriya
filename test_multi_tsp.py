import numpy as np
from matrix_processing import MatrixDistances
import pytest


@pytest.mark.parametrize('dist_matrix, count_add_drones, expected_matrix',
                         [(MatrixDistances(np.array([[0, 1, 2, 3, 4, 5],
                                     [1, np.inf, 20, 18, 12, 8],
                                     [2, 5, np.inf, 14, 7, 11],
                                     [3, 12, 18, np.inf, 6, 11],
                                     [4, 11, 17, 11, np.inf, 12],
                                     [5, 5, 5, 5, 5, np.inf]])),
                           2,
                           np.array([[0, -2, -3, -1, 2, 3, 4, 5],
                                     [-2, np.inf, np.inf, np.inf, 20, 18, 12, 8],
                                     [-3, np.inf, np.inf, np.inf, 20, 18, 12, 8],
                                     [-1, np.inf, np.inf, np.inf, 20, 18, 12, 8],
                                     [2, 5, 5, 5, np.inf, 14, 7, 11],
                                     [3, 12, 12, 12, 18, np.inf, 6, 11],
                                     [4, 11, 11, 11, 17, 11, np.inf, 12],
                                     [5, 5, 5, 5, 5, 5, 5, np.inf]])),

                          (MatrixDistances(np.array([[0, 111, 222, 333, 444, 555],
                                     [111, np.inf, 90, 80, 40, 100],
                                     [222, 60, np.inf, 40, 50, 70],
                                     [333, 50, 30, np.inf, 60, 20],
                                     [444, 10, 70, 20, np.inf, 50],
                                     [555, 20, 40, 50, 20, np.inf]])),
                           3,
                           np.array([[0, -112, -113, -114, -111, 222, 333, 444, 555],
                                     [-112, np.inf, np.inf, np.inf, np.inf, 90, 80, 40, 100],
                                     [-113, np.inf, np.inf, np.inf, np.inf, 90, 80, 40, 100],
                                     [-114, np.inf, np.inf, np.inf, np.inf, 90, 80, 40, 100],
                                     [-111, np.inf, np.inf, np.inf, np.inf, 90, 80, 40, 100],
                                     [222, 60, 60, 60, 60, np.inf, 40, 50, 70],
                                     [333, 50, 50, 50, 50, 30, np.inf, 60, 20],
                                     [444, 10, 10, 10, 10, 70, 20, np.inf, 50],
                                     [555, 20, 20, 20, 20, 40, 50, 20, np.inf]])),

                          (MatrixDistances(np.array([[0, 1, 22, 333, 444, 55, 6],
                                     [1, np.inf, 4, 4, 5, 4, 3],
                                     [22, 2, np.inf, 7, 1, 1, 6],
                                     [333, 2, 3, np.inf, 9, 4, 5],
                                     [444, 1, 3, 2, np.inf, 3, 1],
                                     [55, 7, 4, 1, 1, np.inf, 4],
                                     [6, 2, 3, 4, 7, 9, np.inf]])),
                           1,
                           np.array([[0, -2, -1, 22, 333, 444, 55, 6],
                                     [-2, np.inf, np.inf, 4, 4, 5, 4, 3],
                                     [-1, np.inf, np.inf, 4, 4, 5, 4, 3],
                                     [22, 2, 2, np.inf, 7, 1, 1, 6],
                                     [333, 2, 2, 3, np.inf, 9, 4, 5],
                                     [444, 1, 1, 3, 2, np.inf, 3, 1],
                                     [55, 7, 7, 4, 1, 1, np.inf, 4],
                                     [6, 2, 2, 3, 4, 7, 9, np.inf]]))
                          ])
def test_matrix_multi_transformation(dist_matrix, count_add_drones, expected_matrix):
    dist_matrix.matrix_multi_transformation(count_add_drones)
    assert dist_matrix.mat.all() == expected_matrix.all()