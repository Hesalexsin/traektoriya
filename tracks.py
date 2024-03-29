import copy
import logging
import math
from abc import ABC, abstractmethod
from datetime import datetime

import edges
import matplotlib.patches
import matplotlib.pyplot as plt
import numpy as np



#global fig, ax
#plt.rcParams.update({'figure.figsize': (5, 5)})
#fig, ax = plt.subplots()


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def args(self):
        return [self.x, self.y]

    def __del__(self):
        pass


def distance(p1: Point, p2: Point):
    return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5

def angle_in_range(angle: int):
    while angle > 360:
        angle = angle - 360
    return angle


class Fragment:

    def __init__(self, length: float):
        self.length = length

    def draw(self, ax):
        pass

    def intersect_fl(self, obst):
        pass

    def intersect_fz(self, obst):
        pass


class Line(Fragment):
    def __init__(self,color, d1: Point, d2: Point, is_inf=False):
        #print(is_inf)
        self.color = color
        if not is_inf:
            #print(is_inf)
            self.d1 = d1
            self.d2 = d2
            self.length = distance(d1, d2)
            #print(1)
        else:
            #print(is_inf)
            self.d1 = np.inf
            self.d2 = np.inf
            self.length = np.inf
            #print(2)

    def __eq__(self, other):
        if self.d1 == other.d1 and self.d2 == other.d2:
            return True
        else:
            return False

    def draw(self, ax, color):
        if self.length != np.inf:
            X = np.array([self.d1.x,self.d2.x])
            Y = np.array([self.d1.y,self.d2.y])
            print(X,Y)
            print(self.d1.args(), self.d2.args())

            #ax.plot(X,Y)
            print('array',np.array([self.d1.args(),self.d2.args()]))
            cords = np.array([self.d1.args(),self.d2.args()])

            ax.add_patch(matplotlib.patches.Polygon(cords,closed= False,edgecolor= color,fill= False ))

    def is_inf(self):
        return (self.length == np.inf)


class Arc(Fragment):
    def __init__(self, d1: Point, d2: Point, c: Point, path='short'):
        self.c = c
        self.r = distance(d1, c)
        self.d1 = d1
        self.d2 = d2
        if d1.y >= c.y:
            alpha = math.degrees(math.acos((d1.x - c.x) / self.r))
        else:
            alpha = 360 -  math.degrees(math.acos((d1.x - c.x) / self.r))

        if d2.y >= c.y:
            beta = math.degrees(math.acos((d2.x - c.x) / self.r))
        else:
            beta =  360 - math.degrees(math.acos((d2.x - c.x )/ self.r))
        if path == 'short':  # TODO shorter comparison
            if  alpha  <= beta: #alpha - beta <= 180
                self.alpha = alpha
                self.beta = beta
            else:
                self.alpha = beta
                self.beta = alpha
            if (abs(self.beta - self.alpha) / 360) < 0.5:
                self.length = math.pi * 2 * self.r * (abs(self.beta - self.alpha) / 360)
            else:
                print('wow!')

                self.length = math.pi * 2 * self.r * (1 - ((abs(self.beta - self.alpha) / 360)))
                print('wow', self.length, self.alpha, self.beta, (self.beta - self.alpha),
                      abs(self.beta - self.alpha) / 360)
                self.alpha,self.beta = self.beta,self.alpha

        else:
            if alpha  <= beta:
                self.alpha = beta
                self.beta = alpha
            else:
                self.alpha = alpha
                self.beta = beta
            if (abs(self.beta - self.alpha) / 360) > 0.5:
                self.length = math.pi * 2 * self.r * (abs(self.beta - self.alpha) / 360)
            else:
                self.length = math.pi * 2 * self.r * (1 - ((abs(self.beta - self.alpha) / 360)))
                self.alpha = beta
                self.beta = alpha
        #TODO fix lenght calculation


        print('arc-init',self.length, self.alpha, self.beta, (self.beta - self.alpha),abs(self.beta - self.alpha) / 360)

    def __eq__(self, other):
        if self.d1 == other.d1 and self.d2 == other.d2 and self.c == other.c:
            return True
        else:
            return False


    def draw(self, ax, color):
        #TODO fix drawing
        ax.add_patch(matplotlib.patches.Arc(xy=(self.c.x, self.c.y), width=self.r * 2, height=self.r * 2,
                                             theta1=self.alpha, theta2= self.beta, color= color))

class Circle(Fragment):
    def __init__(self,  c: Point, r: int):
        self.c = c
        self.r = r
        self.length = 2 * math.pi * self.r

    def __eq__(self, other):
        if self.r == other.r and  self.c == other.c:
            return True
        else:
            return False

    def intersect_fz(self, obst):
        pass

    def draw(self, ax, color):
        ax.add_patch(matplotlib.patches.Circle(xy=(self.c.x, self.c.y), radius= self.r, fill= False, edgecolor= color))

class Relief(Fragment):
    def __init__(self, vertex:list):
        self.points = []
        self.length = 0
        print(vertex)
        for p in vertex:
            print(p)
            self.points.append(p)
        for i in range(len(self.points)):
            print(self.points, 'points',self.points[i- 1], self.points[i])
            self.length += distance(self.points[i- 1], self.points[i])



    def draw(self, ax, color):
        #X = np.array([p.x for p in self.points])
        #Y = np.array([p.y for p in self.points])


        # ax.plot(X,Y)
        #print('array', np.array([self.d1.args(), self.d2.args()]))
        cords = np.array([p.args() for p in self.points])

        ax.add_patch(matplotlib.patches.Polygon(cords, closed=True, edgecolor= color, fill=False))






class Track:
    def __init__(self, color, *parts: Fragment, is_inf=False):
        #print(is_inf)
        self.color = color
        if not is_inf:
            self.fragments = []
            self.length = 0
            for part in parts:
                self.fragments.append(part)
                self.length += part.length
        else:
            self.fragments = [Line(0, 0, True)]
            self.length = np.inf

    def update(self, useless_part:Fragment, new_parts:list):
        if useless_part is None:
            return
        i = self.fragments.index(useless_part)
        print(1,new_parts)
        print([x.length for x in new_parts])
        lens = [x.length for x in new_parts]
        new_trek = self.fragments[:i] + new_parts + self.fragments[i + 1:]
        self.fragments = copy.deepcopy(new_trek)
        self.length = self.length - useless_part.length + sum(lens)

    def find_path(self, obst: dict):
        while True:
            changes = 0
            previous = copy.deepcopy(self.fragments)
            for part in self.fragments:
                # part.intersect_fl(obst['fls'])
                ans = None
                #print(1, type(part) is tracks.Line )
                if type(part) is Line and obst['fzs'] != []:
                    ans= intersect_fz(part, obst['fzs'])
                    print(ans)
                if type(part) is Line and obst['relief'] != []:
                    ans= intersect_relief(part, obst['relief'])
                    print(ans)
                if ans is not None:
                    self.update(part, ans)
                    changes += 1
            if changes == 0:
                return


def draw(output_filename,*tracks: Track):
    plt.rcParams.update({'figure.figsize': (5, 5)})
    fig, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='box')
    ax.plot([1, 1], [1, 1])
    for track in tracks:
        print(1)
        for x in track.fragments:
            print(2,x)

            x.draw(ax, track.color)
    #ax.add_patch(matplotlib.patches.Polygon(np.array([[1,1],[2,2],[3,3]]),closed= False))


    #tracks[0].fragments[1].draw(ax)

    #ax.add_patch(matplotlib.patches.Polygon(np.array([[1, 1], [2, 2], [3, 3]]), closed=False))
    output_filename = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + output_filename
    fig.savefig('res/' + output_filename, dpi=300)
    logging.info(f"{ output_filename}  created")


def _find_dodge(self):
    pass


def _fl_dodge_path(self):
    pass


def dodge_fz(line: Line, circ: Circle):
    print('circ', circ.c.x, circ.c.y,circ.r)
    print('line',line.d1.args(), line.d2.args())
    l1x = circ.c.x - line.d1.x
    l1y = circ.c.y - line.d1.y
    l1 = (l1x ** 2 + l1y ** 2) ** 0.5
    l2x = circ.c.x - line.d2.x
    l2y = circ.c.y - line.d2.y
    l2 = (l2x ** 2 + l2y ** 2) ** 0.5
    t11x = circ.r * math.sin(math.atan2(l1y, l1x) - math.asin(circ.r / l1)) + circ.c.x
    print('t11x',t11x)
    t11y = circ.r * (-1) * math.cos(math.atan2(l1y, l1x) - math.asin(circ.r / l1)) + circ.c.y
    print('t11y', t11y)
    t12x = circ.r * (-1) * math.sin(math.atan2(l1y, l1x) + math.asin(circ.r / l1)) + circ.c.x

    t12y = circ.r * math.cos(math.atan2(l1y, l1x) + math.asin(circ.r / l1)) + circ.c.y
    print('t21x',l2y, l2x,circ.r, l2)
    print(math.atan2(l2y, l2x) - math.asin(circ.r / l2))
    t21x = circ.r * math.sin(math.atan2(l2y, l2x) - math.asin(circ.r / l2)) + circ.c.x

    t21y = circ.r * (-1) * math.cos(math.atan2(l2y, l2x) - math.asin(circ.r / l2)) + circ.c.y
    print('t21',t21x, t21y)
    t22x = circ.r * (-1) * math.sin(math.atan2(l2y, l2x) + math.asin(circ.r / l2)) + circ.c.x

    t22y = circ.r * math.cos(math.atan2(l2y, l2x) + math.asin(circ.r / l2)) + circ.c.y
    print('t22', t22x, t22y)
    p1, p2, p3, p4 = Point(t11x, t11y), Point(t12x, t12y), Point(t21x, t21y), Point(t22x, t22y)
    # a1, a2, a3, a4 = Arc(p1, p3, circ.c), Arc(p1, p4, circ.c), Arc(p2, p3, circ.c), Arc(p2, p4, circ.c)
    # if a1.length == min(a1.length, a2.length, a3.length, a4.length):
    #     print(1111111111111111)
    #     #print( p1.args(),a1.d1.args(),a1.d2.args(),p3.args())
    #     return [Line(line.d1, p1), a1, Line(p3, line.d2)]
    # if a2.length == min(a1.length, a2.length, a3.length, a4.length):
    #     print(2222222222222222)
    #     return [Line(line.d1, p1), a2, Line(p4, line.d2)]
    # if a3.length == min(a1.length, a2.length, a3.length, a4.length):
    #     print(3333333333)
    #     return [Line(line.d1, p2), a3, Line(p3, line.d2)]
    # if a4.length == min(a1.length, a2.length, a3.length, a4.length):
    #     print(44444444)
    #     return [Line(line.d1, p2), a4, Line(p4, line.d2)]
    # return None
    a1, a2=  Arc(p1, p4, circ.c), Arc(p2, p3, circ.c)
    if a1.length == min(a1.length, a2.length):
        print(1111111111111111)
        #print( p1.args(),a1.d1.args(),a1.d2.args(),p3.args())
        return [Line(line.d1, p1), a1, Line(p4, line.d2)]
    if a2.length == min(a1.length, a2.length):
        print(2222222222222222)
        return [Line(line.d1, p2), a2, Line(p3, line.d2)]
    return None


def intersect_fz(line: Line, obst:list):
    for circ in obst:
        p1x = line.d1.x - circ.c.x
        p1y = line.d1.y - circ.c.y
        p2x = line.d2.x - circ.c.x
        p2y = line.d2.y - circ.c.y
        a = (p2x - p1x) ** 2 + (p2y - p1y) ** 2
        k = (p2x - p1x) * p1x + (p2y - p1y) * p1y
        c = p1x ** 2 + p1y ** 2 - circ.r ** 2
        d1 = k ** 2 - a * c

        if   a!=0:
            x1 = (-1 * k - d1 ** 0.5) / a
            x2 = (-1 * k + d1 ** 0.5) / a
            print('x1x2',x1, x2)
            if (type(x1) is not complex or type(x2) is not complex):
                if (0 <= x1 <= 0.999999 and 0 <= x2 <= 0.999999):
                    return dodge_fz(line, circ)

def on_poly_path(poly, start, stop):
    track1 = []
    track2 = []
    len1 = 0
    len2 = 0
    flag = False
    for i in range(len(poly.points)*2):
        if poly.points[i % len(poly.points)] == start and flag == False:
            flag = True
        elif poly.points[i% len(poly.points)] == start and flag == True:
            break
        elif poly.points[i% len(poly.points)] != start and flag == True:
            track1.append(Line(poly.points[(i - 1)% len(poly.points)], poly.points[i]))
            len1 += track1[-1].length
        if poly.points[i] == stop and flag == True:
            break
    for j in range(len(poly.points)*2, 0, -1):
        if poly.points[j % len(poly.points)] == start and flag == False:
            flag = True
        elif poly.points[j % len(poly.points)] == start and flag == True:
            break
        elif poly.points[j % len(poly.points)] != start and flag == True:
            track1.append(Line(poly.points[(j + 1)% len(poly.points)], poly.points[j]))
            len2 += track2[-1].length
        if poly.points[j] == stop and flag == True:
            break

    if len1 >= len2:
        return track1
    else:
        return track2

def check_sign_of_vector_prod(d1, d2, d3, d4):
    math.acos(((d2.x-d1.x )*(d3.x - d2.x) +(d2.y-d1.y )*(d3.y - d2.y))/((((d2.x-d1.x )**2 + (d2.y-d1.y )**2)**0.5)*(((d3.x - d2.x)**2 + (d3.y - d2.y)**2)**0.5)))
    return False

def check_prop(p1,p2,p3):
    if p2.x- p1.x/ p2.y- p1.y == p3.x- p1.x/ p3.y- p1.y:
        if distanse(p1,p2) >= distance(p1,p3):
            return p3
        else:
            return p2
def dodge_relief(line: Line, poly: Relief):
    d1_tangent_points =[]
    d2_tangent_points = []
    for i in range((len(poly.points)) ):
        if check_sign_of_vector_prod(line.d1, poly.points[i], poly.points[i-1], poli.points[(i+1) %(len(poly.points))]):
            d1_tangent_points.append(poly.points[i])
            if len(d1_tangent_points) >1:
                deleted_point = check_prop(line.d1, d1_tangent_points[-1], d1_tangent_points[-2])
                if not (deleted_point is None):
                    d1_tangent_points.remove(deleted_point)

        if check_sign_of_vector_prod(line.d2, poly.points[i], poly.points[i - 1], poli.points[(i + 1) % (len(poly.points))]):
            if check_sign_of_vector_prod(line.d2, poly.points[i], poly.points[i - 1],
                                         poli.points[(i + 1) % (len(poly.points))]):
                d2_tangent_points.append(poly.points[i])
                if len(d2_tangent_points) > 1:
                    deleted_point = check_prop(line.d2, d2_tangent_points[-1], d2_tangent_points[-2])
                    if not (deleted_point is None):
                        d2_tangent_points.remove(deleted_point)

    track1 = [Line(line.d1, d1_tangent_points[0])] + on_poly_path(poly,d1_tangent_points[0],d2_tangent_points[0]) + Line(d2_tangent_points[0],line.d2)
    track2 = [Line(line.d1, d1_tangent_points[0])] + on_poly_path(poly, d1_tangent_points[0],
                                                                  d2_tangent_points[1]) + Line(d2_tangent_points[1],
                                                                                               line.d2)
    track3 = [Line(line.d1, d1_tangent_points[1])] + on_poly_path(poly, d1_tangent_points[1],
                                                                  d2_tangent_points[0]) + Line(d2_tangent_points[0],
                                                                                               line.d2)
    track4 = [Line(line.d1, d1_tangent_points[1])] + on_poly_path(poly, d1_tangent_points[1],
                                                                  d2_tangent_points[1]) + Line(d2_tangent_points[1],
                                                                                               line.d2)
    dodge_paths = [track1, track2,track3,track4]
    lengths = [0,0,0,0]
    for i in range(4):
        for x in dodge_paths[i]:
            lengths[i] += x.length

    return dodge_paths[lengths.index(min(lengths))]

def intersect_relief(line: Line, obst:list):
    for poly in obst:
        intersections = 0
        for i in range(len(poly.points)):
            #print(poly.points, 'points', self.points[i - 1], self.points[i])
            if edges.is_intersect(line.d1,line.d2, poly.points[i-1], poly.points[i]):
                intersections += 1

        if   intersections!=0:
            return dodge_relief(line, poly)
        else:
            return None




