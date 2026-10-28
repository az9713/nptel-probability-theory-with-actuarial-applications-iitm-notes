"""Computed answers and consistency checks for the thirty source mock mechanisms."""
from fractions import Fraction
from math import comb, erf, exp, isclose, sqrt


def phi(z):
    return (1 + erf(z / sqrt(2))) / 2


answers = {
    1: Fraction(6, 14), 2: 2.0,
    3: 1 - 0.8 ** 10 - 10 * 0.2 * 0.8 ** 9,
    4: 0.4 - 0.7 * 0.6, 5: 1 / (1 / 5 + 1 / 10),
    6: 3.0, 7: 4 / 0.8 ** 2, 8: 1 - 64 / 16 ** 2,
    9: 1 - phi(1), 10: 500 * exp(-0.4),
    11: Fraction(comb(6, 3) * comb(4, 2), comb(10, 5)),
    12: 1.5, 13: phi(2), 14: 25 + 16 + 2 * 0.5 * 5 * 4,
    15: 'density exp(-y), y>0', 16: 10 * 500,
    17: 5.0, 18: 100 / 400,
    19: 1 - phi((214.5 - 200) / 10), 20: 40 - 40 ** 2 / 200,
    21: 0.5 * 0.05 + 0.3 * 0.1 + 0.2 * 0.2,
    22: 1 - (2 ** 2 - 1) / 8, 23: exp(-2) * 2 ** 2 / 2,
    24: 0.5 + 0.5 ** 2 - 0.5 ** 3,
    25: 'density 6*y**5, 0<y<1', 26: 2 + 1,
    27: 1 - phi((33 - 30) / sqrt(4 + 5)),
    28: phi((90.5 - 100) / 10),
    29: 100 * (exp(-0.5) - exp(-2)), 30: 5 * 4000,
}
assert isclose(sum([0.1, 0.2, 0.3, 0.4]), 1)
assert isclose(answers[4], -0.02)
assert answers[11] == Fraction(10, 21)
assert isclose(answers[9], answers[27])
assert isclose(answers[21], 0.095)
assert isclose(answers[24], 0.625)
assert answers[30] == 20000
# Simpson's rule is exact for each polynomial in this joint-density check.
def integrate(f, a, b):
    return (b - a) * (f(a) + 4 * f((a + b) / 2) + f(b)) / 6


def marginal(x):
    return integrate(lambda y: 2 * (x + y), x, 1)


assert isclose(integrate(marginal, 0, 1), 1)
assert isclose(integrate(marginal, 0, 0.5), answers[24])
for number, value in answers.items():
    shown = f'{float(value):.6f}' if not isinstance(value, str) else value
    print(f'Q{number:02d}: {shown}')
