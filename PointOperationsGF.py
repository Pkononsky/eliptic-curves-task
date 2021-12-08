from EllipticCurve import EllipticCurve
from EllipticCurveGF import EllipticCurveGF
from Point import Point
from PointOperations import PointOperations
from Polynomial import Polynomial


class PointOperationsGF(PointOperations):

    @staticmethod
    def _extended_gcd(irreducible: Polynomial, pol: Polynomial):
        coef, old_coef = Polynomial(0), Polynomial(1)
        rest, old_rest = irreducible, pol

        while rest != Polynomial(0):
            quotient = old_rest // rest

            old_rest, rest = rest, old_rest + quotient * rest
            old_coef, coef = coef, old_coef + quotient * coef

        return old_coef % irreducible

    @staticmethod
    def is_point_belong(curve: EllipticCurveGF, point: Point):
        return (point.y * point.y + curve.a * point.x * point.y) % curve.p == (point.x * point.x * point.x + curve.b * point.x * point.x + curve.c) % curve.p

    @staticmethod
    def points_sum(curve: EllipticCurveGF, point1: Point, point2: Point, *args):
        """
            args[0] - is_nn
        """
        if not PointOperationsGF.is_point_belong(curve, point1):
            return f"Точка ({point1.x.bin_present}, {point1.y.bin_present}) не принадлежит кривой"
        elif not PointOperationsGF.is_point_belong(curve, point2):
            return f"Точка ({point2.x.bin_present}, {point2.y.bin_present}) не принадлежит кривой"
        else:
            if args[0]:
                return PointOperationsGF._points_sum_nn(curve, point1, point2)
            else:
                return PointOperationsGF._points_sum_ns(curve, point1, point2)

    # несуперсингулярный
    @staticmethod
    def _points_sum_nn(curve: EllipticCurve, point1: Point, point2: Point):
        x1 = point1.x
        y1 = point1.y
        x2 = point2.x
        y2 = point2.y

        if point1.is_infinity(True):
            return point2
        elif point2.is_infinity(True):
            return point1
        if x1 == x2:
            if (y1 + y2) % curve.p == curve.a * x1:
                return Point(Polynomial(0), Polynomial(0))
            k = (curve.a * y1 + x1 * x1) * PointOperationsGF._extended_gcd(curve.p, curve.a * x1) % curve.p
        else:
            k = (y2 + y1) * PointOperationsGF._extended_gcd(curve.p, x2 + x1) % curve.p

        x3 = (k * k + k * curve.a + curve.b + x1 + x2) % curve.p

        y3 = (y1 + k * (x3 + x1)) % curve.p

        return Point(x3, (y3 + curve.a * x3) % curve.p)

    # суперсингулярный
    @staticmethod
    def _points_sum_ns(curve: EllipticCurve, point1: Point, point2: Point):
        x1 = point1.x
        y1 = point1.y
        x2 = point2.x
        y2 = point2.y

        if point1.is_infinity(True):
            return point2
        elif point2.is_infinity(True):
            return point1
        elif x1 == x2:
            if (y1 + y2) % curve.p == curve.a:
                return Point(Polynomial(0), Polynomial(0))
            k = (curve.b + x1 * x1) * PointOperationsGF._extended_gcd(curve.p, curve.a) % curve.p
        else:
            k = (y2 + y1) * PointOperationsGF._extended_gcd(curve.p, x2 + x1) % curve.p

        x3 = (k * k + x1 + x2) % curve.p
        y3 = (y1 + k * (x3 + x1)) % curve.p

        return Point(x3, (y3 + curve.a * x3) % curve.p)

    @staticmethod
    def points_mul(curve: EllipticCurveGF, point: Point, mul: int, *args):
        """
            args[0] - is_nn
        """
        if args[0]:
            return PointOperationsGF._points_mul(curve, point, mul, PointOperationsGF._points_sum_nn)
        else:
            return PointOperationsGF._points_mul(curve, point, mul, PointOperationsGF._points_sum_ns)

    @staticmethod
    def _points_mul(curve: EllipticCurveGF, point: Point, mul: int, func):
        if not PointOperationsGF.is_point_belong(curve, point):
            return f"Точка ({point.x.bin_present}, {point.y.bin_present}) не принадлежит кривой"

        res_point = point

        for bit in bin(mul)[3:]:
            res_point = func(curve, res_point, res_point)
            if bit == '1':
                res_point = func(curve, res_point, point)

        return res_point

