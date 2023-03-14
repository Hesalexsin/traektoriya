import numpy as np
from travelling_salesmans_task import travel_salesmans_task
import pytest


@pytest.mark.parametrize('matrix, result',
                         [(np.array([[0, 1, 2, 3, 4, 5],
                                     [1, np.inf, 20, 18, 12, 8],
                                     [2, 5, np.inf, 14, 7, 11],
                                     [3, 12, 18, np.inf, 6, 11],
                                     [4, 11, 17, 11, np.inf, 12],
                                     [5, 5, 5, 5, 5, np.inf]]),
                           [1, 5, 3, 4, 2, 1]),
                          (np.array([[0, 1001, 2002, 3003, 4004, 5005],
                                     [1001, np.inf, 20, 18, 12, 8],
                                     [2002, 5, np.inf, 14, 7, 11],
                                     [3003, 12, 18, np.inf, 6, 11],
                                     [4004, 11, 17, 11, np.inf, 12],
                                     [5005, 5, 5, 5, 5, np.inf]]),
                            [1001, 5005, 3003, 4004, 2002, 1001]),
                          (np.array([[0, 111, 222, 333, 444, 555],
                                     [111, np.inf, 90, 80, 40, 100],
                                     [222, 60, np.inf, 40, 50, 70],
                                     [333, 50, 30, np.inf, 60, 20],
                                     [444, 10, 70, 20, np.inf, 50],
                                     [555, 20, 40, 50, 20, np.inf]]),
                           [111, 444, 333, 555, 222, 111]),
                          (np.array([[0, 11, 22, 33, 44, 55],
                                     [11, np.inf, 20, 18, 12, 8],
                                     [22, 5, np.inf, 14, 7, 11],
                                     [33, 12, 18, np.inf, 6, 11],
                                     [44, 11, 17, 11, np.inf, 12],
                                     [55, 5, 5, 5, 5, np.inf]]),
                           [11, 55, 33, 44, 22, 11]),
                          (np.array([[0, 1, 22, 333, 444, 55, 6],
                                     [1, np.inf, 4, 4, 5, 4, 3],
                                     [22, 2, np.inf, 7, 1, 1, 6],
                                     [333, 2, 3, np.inf, 9, 4, 5],
                                     [444, 1, 3, 2, np.inf, 3, 1],
                                     [55, 7, 4, 1, 1, np.inf, 4],
                                     [6, 2, 3, 4, 7, 9, np.inf]]),
                           [1, 22, 55, 444, 6, 333, 1]),
                          ])
def test_travel_salesmans_task(matrix, result):
    assert travel_salesmans_task(matrix) == result


@pytest.mark.parametrize("expected_exception, wrong_mat",
                         [(TypeError,
                           np.array([[0, 1, 2, '3', 4, 5],
                                     [1, np.inf, 20, 18, 12, 8],
                                     ['2', 5, np.inf, 14, 7, 11],
                                     [3, 12, 18, np.inf, 6, 11],
                                     ['4', 11, 17, 11, np.inf, 12],
                                     [5, 5, 5, 5, 5, np.inf]])),

                          ])
def test_travel_salesmans_with_error(expected_exception, wrong_mat):
    with pytest.raises(expected_exception):
        travel_salesmans_task(wrong_mat)
