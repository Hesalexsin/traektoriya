import json
import numpy as np


def make_array(data):

    n = len(data)
    return fill_array(n, data )
def init_array(n):
    a = np.zeros((n,n))
    for i in range(n):
        a[i][i] = np.inf
        a[0][i] = i
        a[i][0] = i
    return a

def fill_array(n,points):
    a = init_array(n)
    for i in range(1,n):
        for j in range (i+1,n):
            r12 = distanse(points[i],points[j])
            a[i][j] = r12
            a[j][i] = r12
    return a

def distanse(dot1, dot2):
    x1 = dot1.get('x')
    y1 = dot1.get('y')
    x2 = dot2.get('x')
    y2 = dot2.get('y')
    r12 = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return r12

#print(make_array("data.json"))
#print(data.get('data_points')[0].get('x'))
"""
a = np.array([[0, 1, 2, 3, 4, 5],
                  [1, np.inf, 20, 18, 12, 8],
                  [2, 5, np.inf, 14, 7, 11],
                  [3, 12, 18, np.inf, 6, 11],
                  [4, 11, 17, 11, np.inf, 12],
                  [5, 5, 5, 5, 5, np.inf]])
"""