"""CDF jumps and a mixed loss distribution."""
from math import exp, isclose

atom = 0.7
rate = 0.5


def cdf(x):
    return 0.0 if x < 0 else atom + (1 - atom)*(1 - exp(-rate*x))


assert cdf(-1) == 0
assert cdf(0) == atom
assert isclose(1 - cdf(2), 0.3*exp(-1))
assert all(cdf(i/10) <= cdf((i + 1)/10) for i in range(-10, 100))
print(f"P(X = 0) = {cdf(0):.6f}")
print(f"P(X > 2) = {1 - cdf(2):.6f}")
print(f"P(0 < X <= 2) = {cdf(2) - cdf(0):.6f}")
