from EllipticCurve import EllipticCurve
from EllipticCurveGF import EllipticCurveGF
from EllipticCurveZp import EllipticCurveZp
from Point import Point
from PointOperationsGF import PointOperationsGF
from PointOperationsZp import PointOperationsZp
from Polynomial import Polynomial
from os import listdir
from os.path import isfile, join

curve_map = {
    'ZP': EllipticCurveZp,
    'GF2NS': (EllipticCurveGF, False),
    'GF2NN': (EllipticCurveGF, True)
}


def parse_str_with_base(string: str):
    if string.startswith('0b'):
        return int(string, 2)
    elif string.startswith('0x'):
        return int(string, 16)
    else:
        return int(string)


def compute_in_zp(lines, res):
    p = parse_str_with_base(lines[1])
    a = parse_str_with_base(lines[2])
    b = parse_str_with_base(lines[3])

    curve = EllipticCurveZp(p, a, b)

    for line in lines[4:]:
        line = line.replace('\n', '')
        split = line.split(' ')
        operation = split[0]

        if operation.lower() == 'a':
            point1_str = split[1].replace('(', '').replace(',', ' ').replace(')', '').split(' ')
            point2_str = split[2].replace('(', '').replace(',', ' ').replace(')', '').split(' ')

            point1 = Point(parse_str_with_base(point1_str[0]), parse_str_with_base(point1_str[1]))
            point2 = Point(parse_str_with_base(point2_str[0]), parse_str_with_base(point2_str[1]))

            res.write(f'{line} = {PointOperationsZp.points_sum(curve, point1, point2)}\n')
        elif operation.lower() == 'm':
            point1_str = split[1].replace('(', '').replace(',', ' ').replace(')', '').split(' ')
            mul = int(split[2])

            point1 = Point(parse_str_with_base(point1_str[0]), parse_str_with_base(point1_str[1]))

            res.write(f'{line} = {PointOperationsZp.points_mul(curve, point1, mul)}\n')


def compute_in_gf(lines, res):
    p = Polynomial.from_exponent(parse_str_with_base(lines[1]))
    a = Polynomial(parse_str_with_base(lines[2]))
    b = Polynomial(parse_str_with_base(lines[3]))
    c = Polynomial(parse_str_with_base(lines[4]))

    curve = EllipticCurveGF(p, a, b, c)

    is_nn = lines[0].startswith('GF2NN')

    for line in lines[4:]:
        line = line.replace('\n', '')
        split = line.split(' ')
        operation = split[0]

        if operation.lower() == 'a':
            point1_str = split[1].replace('(', '').replace(',', ' ').replace(')', '').split(' ')
            point2_str = split[2].replace('(', '').replace(',', ' ').replace(')', '').split(' ')

            point1 = Point(Polynomial(parse_str_with_base(point1_str[0])), Polynomial(parse_str_with_base(point1_str[1])))
            point2 = Point(Polynomial(parse_str_with_base(point2_str[0])), Polynomial(parse_str_with_base(point2_str[1])))

            res.write(f'{line} = {PointOperationsGF.points_sum(curve, point1, point2, is_nn).to_string(True)}\n')
        elif operation.lower() == 'm':
            point1_str = split[1].replace('(', '').replace(',', ' ').replace(')', '').split(' ')
            mul = int(split[2])

            point1 = Point(Polynomial(parse_str_with_base(point1_str[0])), Polynomial(parse_str_with_base(point1_str[1])))

            res.write(f'{line} = {PointOperationsGF.points_mul(curve, point1, mul, is_nn).to_string(True)}\n')

def main():
    files = [f for f in listdir('tests') if isfile(join('tests', f))]

    with open('result.txt', mode='w+', encoding='utf-8') as res:
        for file in files:
            res.write(f'===\t\t{file}\t\t===\n')
            with open(f'tests\\{file}', mode='r+') as f:
                lines = f.readlines()


                if lines[0].startswith('ZP'):
                    compute_in_zp(lines, res)
                if lines[0].startswith('GF2'):
                    compute_in_gf(lines, res)

                res.write('\n\n')


if __name__ == '__main__':
    main()
