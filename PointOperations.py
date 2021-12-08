from EllipticCurve import EllipticCurve
from Point import Point
from abc import ABC
from abc import abstractmethod


class PointOperations(ABC):

    @staticmethod
    @abstractmethod
    def is_point_belong(curve: EllipticCurve, point: Point):
        pass

    @staticmethod
    @abstractmethod
    def points_sum(curve: EllipticCurve, point1: Point, point2: Point):
        pass

    @staticmethod
    @abstractmethod
    def points_mul(curve: EllipticCurve, point: Point, mul: int):
        pass

