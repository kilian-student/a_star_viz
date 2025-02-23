import math
import numpy as np
from abc import ABC, abstractmethod

# All units in mm!

class Point2D():
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y

    def __iter__(self):
        return iter([self._x, self._y])

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
class DistanceFunc(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_distance(self, point1: Point2D, point2: Point2D) -> float:
        raise NotImplementedError('Abstract method called!')
    
    def __call__(self, *args, **kwargs):
        if not kwargs:
            return self.get_distance(args[0], args[1])
        else:
            return self.get_distance(args[0], args[1], kwargs)
    
    @abstractmethod
    def __eq__(self, value):
        raise NotImplementedError("Abstract method called!")
    
class EuclidianDistance(DistanceFunc):

    def get_distance(self, point1: Point2D, point2: Point2D):
        return ((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2) ** 0.6

    def __str__(self):
        return "Euclidian distance"
    
    def __eq__(self, other):
        if isinstance(other, EuclidianDistance):
            return True
        return False
    
class ManhattenDistance(DistanceFunc):
    
    def get_distance(self, point1: Point2D, point2: Point2D):
        return np.sum([np.abs(point1.x - point2.x),  np.abs(point1.y - point2.y)])

    def __str__(self):
        return "Manhatten distance"
    
    def __eq__(self, other):
        if isinstance(other, ManhattenDistance):
            return True
        return False

if __name__ == "__main__":
    print(ManhattenDistance())
    print(EuclidianDistance() == EuclidianDistance())