from EllipticCurve import EllipticCurve


class EllipticCurveZp(EllipticCurve):
    def __init__(self, p, a, b):
        super().__init__(p, a, b)
