from EllipticCurve import EllipticCurve
from Point import Point
from PointOperations import PointOperations


class PointOperationsZp(PointOperations):

    @staticmethod
    def _extended_gcd(prime: int, num: int):
        coef, old_coef = 0, 1
        rest, old_rest = prime, num

        while rest != 0:
            quotient = old_rest // rest

            old_rest, rest = rest, old_rest - quotient * rest
            old_coef, coef = coef, old_coef - quotient * coef

        return old_coef % prime

    @staticmethod
    def is_point_belong(curve: EllipticCurve, point: Point):
        x = point.x
        y = point.y

        return (y ** 2) % curve.p == (x ** 3 + curve.a * x + curve.b) % curve.p

    @staticmethod
    def points_sum(curve: EllipticCurve, point1: Point, point2: Point):
        if not PointOperationsZp.is_point_belong(curve, point1):
            return f"Точка ({point1.x}, {point1.y}) не принадлежит кривой"
        elif not PointOperationsZp.is_point_belong(curve, point2):
            return f"Точка ({point2.x}, {point2.y}) не принадлежит кривой"
        else:
            return PointOperationsZp._points_sum(curve, point1, point2)

    @staticmethod
    def _points_sum(curve: EllipticCurve, point1: Point, point2: Point):
        x1 = point1.x
        y1 = point1.y
        x2 = point2.x
        y2 = point2.y

        if point1.is_infinity():
            return point2
        elif point2.is_infinity():
            return point1
        elif x1 == x2:
            if (y1 + y2) % curve.p == 0:
                return Point(0, 0)
            k = (3 * x1 ** 2 + curve.a) * PointOperationsZp._extended_gcd(curve.p, 2 * y1)
        else:
            k = (y2 - y1) * PointOperationsZp._extended_gcd(curve.p, x2 - x1)

        x3 = (k ** 2 - x1 - x2) % curve.p
        y3 = (y1 + k * (x3 - x1)) % curve.p

        return Point(x3, -y3 % curve.p)

    @staticmethod
    def points_mul(curve: EllipticCurve, point: Point, mul: int):
        if not PointOperationsZp.is_point_belong(curve, point):
            return f"Точка ({point.x}, {point.y}) не принадлежит кривой"

        res_point = point

        for bit in bin(mul)[3:]:
            res_point = PointOperationsZp._points_sum(curve, res_point, res_point)
            if bit == '1':
                res_point = PointOperationsZp._points_sum(curve, res_point, point)

        return res_point
