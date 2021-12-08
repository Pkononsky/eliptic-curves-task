from abc import ABC


class EllipticCurve(ABC):
    def __init__(self, p, a, b):
        self.p = p
        self.a = a
        self.b = b
