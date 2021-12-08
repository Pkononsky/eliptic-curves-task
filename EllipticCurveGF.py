from EllipticCurve import EllipticCurve


class EllipticCurveGF(EllipticCurve):
    def __init__(self, p, a, b, c):
        super().__init__(p, a, b)
        self.c = c
