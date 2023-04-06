import math

import matplotlib.patches


class Point:
    def __init__(self,x:float,y:float):
        self.x = x
        self.y = y

    def __del__(self):
        pass




def distance(p1:Point, p2:Point):
    return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**0.5
class Fragment:

    def __init__(self, length:float):
        self.length = length

class Line(Fragment):
    def __init__(self, d1:Point, d2:Point):
        self.d1 = d1
        self.d2 = d2
        self.length = distance(d1,d2)

    def draw(self):
        pass
class Arc(Fragment):
    def __init__(self, d1:Point, d2:Point, c:Point, path = 'short' ):
        self.c = c
        self.r = distance(d1,c)
        if d1.y >= c.y:
            alpha = math.acos(d1.x-c.x/ self.r)
        else:
            alpha = 2* math.pi - math.acos(d1.x-c.x/ self.r)

        if d2.y >= c.y:
            beta = math.acos(d2.x - c.x / self.r)
        else:
            beta = 2 * math.pi - math.acos(d2.x - c.x / self.r)
        if path == 'short'and alpha < beta and beta - alpha <= math.pi:
            self.d1 = d1
            self.d2 = d2
            self.alpha = alpha
            self.beta = beta
        elif path != 'short'and alpha > beta and alpha - beta > math.pi:
            self.d1 = d1
            self.d2 = d2
            self.alpha = alpha
            self.beta = beta

    def draw(self):
        return matplotlib.patches.Arc(xy= (self.c.x,self.c.y), width= self.r * 2, height= self.r *2,
                                      theta1=self.alpha, theta2=self.beta, color= 'r')


class Trek:
    def __init__(self, *parts:Fragment):
        self.fragments = []
        self.length = 0
        for part in parts:
            self.fragments.append(part)
            self.length += part.length

    def update(self,useless_part, *new_parts):
        pass

def fl_dodge_path:
def find_path(edge:Trek):
    for part in edge.fragments:
        is intersect_fz(part) != None:
            edge.update(part, dodge_)
def is_intersect_fl(part:Fragment):
    pass
def is_intersect_fz(part:Fragment):
    pass

def is_intersect_geo(part:Fragment):
    pass