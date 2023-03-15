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
def distance(dot1: dict, dot2: dict):
    x1 = dot1.get('x')
    y1 = dot1.get('y')
    x2 = dot2.get('x')
    y2 = dot2.get('y')
    r12 = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return r12

# calculating length of edges allow intersections with FLs (need strategy of realisation)
def update_edges_with_fl(a: np.array, n: int, points: dict, data_forbidden_lines):
    pass


# checking intersections of one of the edges and one of the FLs (need more compact func)
def is_intersect(dot1: dict, dot2: dict, dot3: dict, dot4: dict):
    x1 = dot1.get('x')
    x2 = dot2.get('x')
    x3 = dot3.get('x')
    x4 = dot4.get('x')
    orient1 = check_orientation(dot1, dot2, dot3)
    orient2 = check_orientation(dot1, dot2, dot4)
    orient3 = check_orientation(dot3, dot4, dot1)
    orient4 = check_orientation(dot3, dot4, dot2)
    if orient1 != orient2 and orient3 != orient4:
        return True
    elif orient1 == 0 and ((x1 > x3 > x2) or (x1 < x3 < x2)):
        return True
    elif orient2 == 0 and ((x1 > x4 > x2) or (x1 < x4 < x2)):
        return True
    elif orient3 == 0 and ((x3 > x1 > x4) or (x3 < x1 < x4)):
        return True
    elif orient4 == 0 and ((x3 > x2 > x4) or (x3 < x2 < x4)):
        return True
    else:
        return False

# checks the orientation of triples of points (reformat to more compact func)
def check_orientation(dot1: dict, dot2: dict, dot3: dict):
    x1 = dot1.get('x')
    y1 = dot1.get('y')
    x2 = dot2.get('x')
    y2 = dot2.get('y')
    x3 = dot3.get('x')
    y3 = dot3.get('y')
    orient = (y2 - y1) * (x3 - x2) - (x2 - x1) * (y3 - y2)
    if orient > 0:
        return 1
    elif orient < 0:
        return -1
    else:
        return 0
