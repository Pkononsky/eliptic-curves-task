from Polynomial import Polynomial


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return self.to_string(False)

    def to_string(self, is_gf):
        if is_gf:
            return f"(x={bin(self.x.bin_present)}, y={bin(self.y.bin_present)})\t(x={self.x.bin_present}, y={self.y.bin_present})\t(x={hex(self.x.bin_present)}, y={hex(self.y.bin_present)})"
        else:
            return f"(x={bin(self.x)}, y={bin(self.y)})\t(x={self.x}, y={self.y})\t(x={hex(self.x)}, y={hex(self.y)})"

    def is_infinity(self, is_gf=False):
        if is_gf:
            return self.x == Polynomial(0) and self.y == Polynomial(0)
        else:
            return self.x == 0 and self.y == 0
