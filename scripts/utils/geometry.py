import math

# All units in mm!

class Point2D():
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y

    @property
    def x(self)->float:
        return self._x

    @x.setter
    def x(self, val: float) -> None:
        self._x = val

    @property
    def y(self)->float:
        return self._y

    @y.setter
    def y(self, val: float) -> None:
        self._y = val


# Distance calculations
def euclidian_distance(point1: Point2D, point2: Point2D):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

def manhatten_distance():
    pass

def minkowski_distance():
    pass

def cosine_distance():
    pass