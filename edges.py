import json
import logging
import tracks
import numpy as np


# forming a matrix for the traveling salesman algorithm from the input data
def make_array_len(points: dict):
    a, n = init_array(points)
    return fill_array(a, n, points)

# initializing an array using a template np.array([[0, 1, 2, 3, 4, 5],
#                                                 [1, np.inf, 0, 0, 0, 0],
#                                                 [2, 0, np.inf, 0, 0, 0],
#                                                 [3, 0, 0, np.inf, 0, 0],
#                                                 [4, 0, 0, 0, np.inf, 0],
#                                                 [5, 0, 0, 0, 0, np.inf]])

def init_track_matrix(points:dict):
    n = len(points)
    track_m = [[None for x in range(n)]]*n
    for i in range(n):
        for j in range(n):
            if i == j:
                track_m[i][j] = tracks.Track(is_inf=True)
    return track_m

def fill_track_matrix(track_m:list, points:dict): #TODO check
    ids = list(points.keys())
    for i in range(len(points)):
        for j in range(len(points)):
            if i != j:
                track_m[i][j] = tracks.Track(tracks.Line(tracks.Point(points[ids[i]][0], points[ids[i]][1]), tracks.Point(points[ids[j]][0], points[ids[j]][1])))

def update_tracks(track_m:list):
    for line in track_m:
        for track in line:
            track.update()





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
    x1, y1, x2, y2 = dot1['x'], dot1['y'], dot2['x'], dot2['y']
    r12 = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return r12


# calculating length of edges allow intersections with FLs (need strategy of realisation)
def update_edges_with_fl(a: np.array, n: int, points: dict, data_forbidden_lines: dict):
    ids = list(points.keys())
    indexes = a[0]
    for fl in data_forbidden_lines:
        id1, id2 = fl['id1'], fl['id2']
        ind1, ind2 = np.where(indexes == id1)[0][0], np.where(indexes == id2)[0][0]
#TODO write comments
        a[ind1][ind2], a[ind2][ind1] = np.inf, np.inf

        check = ids.copy()
        logging.debug(check)
        check.remove(0)
        check.remove(id1)
        check.remove(id2)
        for id3 in check:
            for id4 in check:
                if id3 != id4:
                    is_intersection_exist = is_intersect(points[id1], points[id2], points[id3], points[id4])
                    logging.debug(points[id1], points[id2], points[id3], points[id4])
                    logging.debug(indexes, np.where(indexes == 1007))
                    logging.debug(np.where(indexes == id3), np.where(indexes == id4), id4)
                    ind3, ind4 = np.where(indexes == id3)[0][0], np.where(indexes == id4)[0][0]
                    if is_intersection_exist:
                        a[ind3][ind4], a[ind4][ind3] = np.inf, np.inf
                    elif is_intersection_exist == 'invalid data':
                        return a, 'invalid_data'
    return a, 'OK'


# checking intersections of one of the edges and one of the FLs (need more compact func)
#TODO more compact, comments, rename
def is_intersect(dot1: tracks.Point, dot2: tracks.Point, dot3: tracks.Point, dot4: tracks.Point):
    x1, x2, x3, x4 = dot1.x, dot2.x, dot3.x, dot4.x
    orient1 = check_orientation(dot1, dot2, dot3)
    orient2 = check_orientation(dot1, dot2, dot4)
    orient3 = check_orientation(dot3, dot4, dot1)
    orient4 = check_orientation(dot3, dot4, dot2)
    if orient1 != orient2 and orient3 != orient4:
        return True
    elif orient1 == 0 and ((x1 > x3 > x2) or (x1 < x3 < x2)):
        return 'invalid data'
    elif orient2 == 0 and ((x1 > x4 > x2) or (x1 < x4 < x2)):
        return 'invalid data'
    elif orient3 == 0 and ((x3 > x1 > x4) or (x3 < x1 < x4)):
        return 'invalid data'
    elif orient4 == 0 and ((x3 > x2 > x4) or (x3 < x2 < x4)):
        return 'invalid data'
    else:
        return False


# checks the orientation of triples of points (reformat to more compact func)
def check_orientation(dot1: tracks.Point, dot2: tracks.Point, dot3: ):
    x1, y1  = dot1.args()
    x2, y2 = dot2.args()
    x3, y3 = dot3.args()
    orient = (y2 - y1) * (x3 - x2) - (x2 - x1) * (y3 - y2)
    if orient > 0:
        return 1
    elif orient < 0:
        return -1
    else:
        return 0

#TODO comm
def update_with_fz(a: np.array, n: int, points: dict, data_forbidden_lines: list):
    if not check_points_in_fz(points, data_forbidden_lines):
        return 'invalid data', a
    return 'ok', a

#TODO comm
def check_points_in_fz(points: dict, fz: list):
    ids = list(points.keys())
    for id in ids:
        for z in fz:
            p = points[id]
            x_z = z['x']
            y_z = z['y']
            x_p = p['x']
            y_p = p['y']
            r = z['r']
            if (x_p - x_z) ** 2 + (y_p - y_z) ** 2 <= r ** 2:
                return False
    return True
