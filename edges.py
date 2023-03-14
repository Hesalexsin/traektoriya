import json
import numpy as np


# forming a matrix for the traveling salesman algorithm from the input data
def make_array(points: dict):
    a, n = init_array(points)
    return fill_array(a, n, points)


# initializing an array using a template np.array([[0, 1, 2, 3, 4, 5],
#                                                 [1, np.inf, 0, 0, 0, 0],
#                                                 [2, 0, np.inf, 0, 0, 0],
#                                                 [3, 0, 0, np.inf, 0, 0],
#                                                 [4, 0, 0, 0, np.inf, 0],
#                                                 [5, 0, 0, 0, 0, np.inf]])
def init_array(points: dict):
    n = len(points)
    a = np.zeros((n, n))
    ids = list(points.keys())
    for i in range(n):
        a[i][i] = np.inf
        a[0][i] = ids[i]
        a[i][0] = ids[i]
    return a, n


# filling the array with calculated distances
def fill_array(a: np.array, n: int, points: dict):
    for i in range(1, n):
        for j in range(i + 1, n):
            r12 = distance(points.get(a[0][i]), points.get(a[j][0]))
            a[i][j] = r12
            a[j][i] = r12
    return a


# calculating distance between points using the pythagorean theorem
def distance(dot1:dict, dot2:dict):
    x1 = dot1.get('x')
    y1 = dot1.get('y')
    x2 = dot2.get('x')
    y2 = dot2.get('y')
    r12 = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return r12
