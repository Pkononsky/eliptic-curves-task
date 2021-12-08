class Polynomial:

    _irreducible = {
        0: [0],                     # 1
        1: [1],                     # x
        2: [2, 1, 0],               # x^2+x+1
        3: [3, 1, 0],               # x^3+x+1,
        4: [4, 1, 0],               # x^4+x+1
        5: [5, 2, 0],               # x^5+x^2+1
        6: [6, 1, 0],               # x^6+x+1
        7: [7, 3, 0],               # x^7+x^3+1
        8: [8, 4, 3, 2, 0],         # x^8+x^4+x^3+x^2+1
        9: [9, 4, 0],               # x^9+x^4+1
        10: [10, 3, 0],             # x^10+x^3+1
        11: [11, 2, 0],             # x^11+x^2+1
        12: [12, 6, 4, 1, 0],       # x^12+x^6+x^4+x+1
        13: [13, 4, 3, 1, 0],       # x^13+x^4+x^3+x+1
        14: [14, 10, 6, 1, 0],      # x^14+x^10+x^6+x+1
        15: [15, 1, 0],             # x^15+x+1
        16: [16, 12, 3, 1, 0],      # x^16+x^12+x^3+x+1
        17: [17, 3, 0],             # x^17+x^3+1
        18: [18, 7, 0],             # x^18+x^7+1
        19: [19, 5, 2, 1, 0],       # x^19+x^5+x^2+x+1
        20: [20, 3, 0],             # x^20+x^3+1
        21: [21, 2, 0],             # x^21+x^2+1
        22: [22, 1, 0],             # x^22+x+1
        23: [23, 5, 0],             # x^23+x^5+1
        24: [24, 7, 2, 1, 0],       # x^24+x^7+x^2+x+1
        25: [25, 3, 0],             # x^25+x^3+1
        26: [26, 6, 2, 1, 0],       # x^26+x^6+x^2+x+1
        27: [27, 5, 2, 1, 0],       # x^27+x^5+x^2+x+1
        28: [28, 3, 0],             # x^28+x^3+1
        29: [29, 2, 0],             # x^29+x^2+1
        30: [30, 23, 2, 1, 0],      # x^30+x^23+x^2+x+1
        31: [31, 3, 1],             # x^31+x^3+1
        32: [32, 22, 2, 1, 0],      # x^32+x^22+x^2+x+1
        # 33 - 35
        36: [36, 11, 0],            # x^36+x^11+1
        # 37 - 39
        40: [40, 9, 3, 1, 0],       # x^40+x^9+x^3+x+1
        # 41 - 47
        48: [48, 28, 3, 1, 0],      # x^48+x^28+x^3+x+1
        # 49 - 55
        56: [56, 42, 2, 1, 0],      # x^56+x^42+x^2+x+1
        163: [163, 7, 6, 3, 0],     # x^163+x^7+x^6+x^3+1
        233: [233, 74, 0],          # x^233+x^74+1
        283: [283, 12, 7, 5, 0],    # x^283+x^12+x^7+x^5+1
        409: [409, 87, 0],          # x^409+x^87+1
        571: [571, 10, 5, 2, 0],    # x^571+x^10+x^5+x^2+1
    }

    @staticmethod
    def to_bits(exponents: list):
        return sum([1 << x for x in exponents])

    def clone(self):
        return Polynomial(self.bin_present)

    @staticmethod
    def from_exponent(exponent: int):
        return Polynomial(Polynomial.to_bits(Polynomial._irreducible.get(exponent)))

    def __index__(self):
        return self.bin_present

    def __init__(self, bits):
        self.bin_present = bits

    def __eq__(self, other: 'Polynomial'):
        return self.bin_present == other.bin_present

    def __add__(self, other: 'Polynomial'):
        return Polynomial(self.bin_present ^ other.bin_present)

    def __len__(self):
        return self.bin_present.bit_length()

    def __mul__(self, other: 'Polynomial'):
        result = Polynomial(0)
        addend = self.clone()
        otherbits = other.bin_present
        while otherbits:
            shift = otherbits & 1
            if shift:
                result += addend
            addend = Polynomial(addend.bin_present << 1)
            otherbits >>= 1

        return result

    def __mod__(self, other: 'Polynomial'):
        first = self.clone()
        while len(first) >= len(other):
            len_dif = len(first) - len(other)
            first += Polynomial(other.bin_present << len_dif)

        return first

    def __floordiv__(self, divisor):
        quotient = Polynomial(0)
        remainder = self.clone()
        while len(remainder) >= len(divisor):
            product = Polynomial(1 << (len(remainder) - len(divisor)))
            quotient += product
            remainder += product * divisor

        return quotient
