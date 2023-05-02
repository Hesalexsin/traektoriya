import numpy as np
import travelling_salesman_problem as t
import actions_with_matrixes as a
import pytest


def length_of_track(track: list, mat: np.array):
    res = 0
    for k in range(1, len(track)):
        res += float(mat[a.arr_index(mat, [track[k - 1], track[k]])])
    return res

@pytest.mark.parametrize('matrix, result, expected_matrix',
                         [(np.array([[0, 1, 2, 3, 4, 5],
                                     [1, np.inf, 20, 18, 12, 8],
                                     [2, 5, np.inf, 14, 7, 11],
                                     [3, 12, 18, np.inf, 6, 11],
                                     [4, 11, 17, 11, np.inf, 12],
                                     [5, 5, 5, 5, 5, np.inf]]),
                           35,
                           np.array([[0, 1, 2, 3, 4, 5],
                                     [1, np.inf, 12, 10, 4, 0],
                                     [2, 0, np.inf, 9, 2, 6],
                                     [3, 6, 12, np.inf, 0, 5],
                                     [4, 0, 6, 0, np.inf, 1],
                                     [5, 0, 0, 0, 0, np.inf]])),

                          (np.array([[0, 111, 222, 333, 444, 555],
                                     [111, np.inf, 90, 80, 40, 100],
                                     [222, 60, np.inf, 40, 50, 70],
                                     [333, 50, 30, np.inf, 60, 20],
                                     [444, 10, 70, 20, np.inf, 50],
                                     [555, 20, 40, 50, 20, np.inf]]),
                           140,
                           np.array([[0, 111, 222, 333, 444, 555],
                                     [111, np.inf, 40, 40, 0, 60],
                                     [222, 20, np.inf, 0, 10, 30],
                                     [333, 30, 0, np.inf, 40, 0],
                                     [444, 0, 50, 10, np.inf, 40],
                                     [555, 0, 10, 30, 0, np.inf]])),

                          (np.array([[0, 1, 22, 333, 444, 55, 6],
                                     [1, np.inf, 4, 4, 5, 4, 3],
                                     [22, 2, np.inf, 7, 1, 1, 6],
                                     [333, 2, 3, np.inf, 9, 4, 5],
                                     [444, 1, 3, 2, np.inf, 3, 1],
                                     [55, 7, 4, 1, 1, np.inf, 4],
                                     [6, 2, 3, 4, 7, 9, np.inf]]),
                           11,
                           np.array([[0, 1, 22, 333, 444, 55, 6],
                                     [1, np.inf, 0, 1, 2, 1, 0],
                                     [22, 1, np.inf, 6, 0, 0, 5],
                                     [333, 0, 0, np.inf, 7, 2, 3],
                                     [444, 0, 1, 1, np.inf, 2, 0],
                                     [55, 6, 2, 0, 0, np.inf, 3],
                                     [6, 0, 0, 2, 5, 7, np.inf]]))
                          ])
def test_reduction(matrix, result, expected_matrix):
    assert a.reduction(matrix) == result
    assert matrix.all() == expected_matrix.all()


@pytest.mark.parametrize('matrix, result',
                         [(np.array([[0, 1, 2, 3, 4, 5],
                                     [1, np.inf, 12, 10, 4, 0],
                                     [2, 0, np.inf, 9, 2, 6],
                                     [3, 6, 12, np.inf, 0, 5],
                                     [4, 0, 6, 0, np.inf, 1],
                                     [5, 0, 0, 0, 0, np.inf]]),
                           [5, 2]),

                          (np.array([[0, 111, 222, 333, 444, 555],
                                     [111, np.inf, 40, 40, 0, 60],
                                     [222, 20, np.inf, 0, 10, 30],
                                     [333, 30, 0, np.inf, 40, 0],
                                     [444, 0, 50, 10, np.inf, 40],
                                     [555, 0, 10, 30, 0, np.inf]]),
                           [111, 444]),

                          (np.array([[0, 1, 22, 333, 444, 55, 6],
                                     [1, np.inf, 0, 1, 2, 1, 0],
                                     [22, 1, np.inf, 6, 0, 0, 5],
                                     [333, 0, 0, np.inf, 7, 2, 3],
                                     [444, 0, 1, 1, np.inf, 2, 0],
                                     [55, 6, 2, 0, 0, np.inf, 3],
                                     [6, 0, 0, 2, 5, 7, np.inf]]),
                           [22, 55]),
                          ])
def test_find_degrees_of_zeros(matrix, result):
    res_expected_mat = a.find_degrees_of_zeros(matrix)
    assert res_expected_mat[0] == result[0] and res_expected_mat[1] == result[1]


@pytest.mark.parametrize('matrix, first_id, result',
                         [(np.array([[0, 1, 2, 3, 4, 5],
                                     [1, np.inf, 20, 18, 12, 8],
                                     [2, 5, np.inf, 14, 7, 11],
                                     [3, 12, 18, np.inf, 6, 11],
                                     [4, 11, 17, 11, np.inf, 12],
                                     [5, 5, 5, 5, 5, np.inf]]),
                           1,
                           [1, 5, 3, 4, 2, 1]),
                          (np.array([[0, 1001, 1002, 1003, 1004, 1005],
                                     [1001, np.inf, 10, 25, 25, 10],
                                     [1002, 1, np.inf, 10, 15, 2],
                                     [1003, 8, 9, np.inf, 20, 10],
                                     [1004, 14, 10, 24, np.inf, 15],
                                     [1005, 10, 8, 25, 27, np.inf]]),
                           1001,
                           [1001, 1005, 1002, 1003, 1004, 1001]),
                          (np.array([[0, 1001, 2002, 3003, 4004, 5005],
                                     [1001, np.inf, 20, 18, 12, 8],
                                     [2002, 5, np.inf, 14, 7, 11],
                                     [3003, 12, 18, np.inf, 6, 11],
                                     [4004, 11, 17, 11, np.inf, 12],
                                     [5005, 5, 5, 5, 5, np.inf]]),
                           1001,
                           [1001, 5005, 3003, 4004, 2002, 1001]),
                          (np.array([[0, 111, 222, 333, 444, 555],
                                     [111, np.inf, 90, 80, 40, 100],
                                     [222, 60, np.inf, 40, 50, 70],
                                     [333, 50, 30, np.inf, 60, 20],
                                     [444, 10, 70, 20, np.inf, 50],
                                     [555, 20, 40, 50, 20, np.inf]]),
                           111,
                           [111, 444, 333, 555, 222, 111]),
                          (np.array([[0, 11, 22, 33, 44, 55],
                                     [11, np.inf, 20, 18, 12, 8],
                                     [22, 5, np.inf, 14, 7, 11],
                                     [33, 12, 18, np.inf, 6, 11],
                                     [44, 11, 17, 11, np.inf, 12],
                                     [55, 5, 5, 5, 5, np.inf]]),
                           11,
                           [11, 55, 33, 44, 22, 11]),
                          (np.array([[0, 1, 22, 333, 444, 55, 6],
                                     [1, np.inf, 4, 4, 5, 4, 3],
                                     [22, 2, np.inf, 7, 1, 1, 6],
                                     [333, 2, 3, np.inf, 9, 4, 5],
                                     [444, 1, 3, 2, np.inf, 3, 1],
                                     [55, 7, 4, 1, 1, np.inf, 4],
                                     [6, 2, 3, 4, 7, 9, np.inf]]),
                           1,
                           [1, 55, 333, 22, 444, 6, 1]),
                          (np.array([[0, 1001, 1002, 1003, 1004, 1005, 1006],
                                     [1001, np.inf, 10, 5, 9, 16, 8],
                                     [1002, 6, np.inf, 11, 8, 18, 19],
                                     [1003, 7, 13, np.inf, 3, 4, 14],
                                     [1004, 5, 9, 6, np.inf, 12, 17],
                                     [1005, 5, 4, 11, 6, np.inf, 14],
                                     [1006, 17, 7, 12, 13, 16, np.inf]]),
                           1001,
                           [1001, 1006, 1002, 1004, 1003, 1005, 1001]),
                          ])
def test_travel_salesman_problem(matrix, first_id, result):
    track = t.travel_salesman_problem(matrix.copy(), first_id)
    assert length_of_track(track, matrix) == length_of_track(result, matrix)


@pytest.mark.parametrize("expected_exception, wrong_mat, first_id",
                         [(TypeError,
                           np.array([[0, 1, 2, '3', 4, 5],
                                     [1, np.inf, 20, 18, 12, 8],
                                     ['2', 5, np.inf, 14, 7, 11],
                                     [3, 12, 18, np.inf, 6, 11],
                                     ['4', 11, 17, 11, np.inf, 12],
                                     [5, 5, 5, 5, 5, np.inf]]),
                           1),

                          ])
def test_travel_salesman_with_error(expected_exception, wrong_mat, first_id):
    with pytest.raises(expected_exception):
        t.travel_salesman_problem(wrong_mat, first_id)
