"""Exact finite compound model and a mixed Poisson moment comparison."""
from collections import defaultdict
from fractions import Fraction as F


def convolve(left, right):
    result = defaultdict(F)
    for x, px in left.items():
        for y, py in right.items():
            result[x+y] += px*py
    return dict(result)


severity = {1: F(1, 2), 2: F(1, 2)}
two_claims = convolve(severity, severity)
aggregate = {0: F(1, 2)}
aggregate.update({s: p/2 for s, p in two_claims.items()})
mean = sum(s*p for s, p in aggregate.items())
second = sum(s*s*p for s, p in aggregate.items())
variance = second-mean*mean
assert sum(aggregate.values()) == 1
assert mean == F(3, 2)
assert variance == F(5, 2)
rate_mean = F(4, 5)*1 + F(1, 5)*4
rate_var = F(4, 5)*(1-rate_mean)**2 + F(1, 5)*(4-rate_mean)**2
assert rate_mean + rate_var == F(76, 25)
print("aggregate pmf = " + ", ".join(
    f"{s}:{aggregate[s]}" for s in sorted(aggregate)))
print(f"aggregate mean = {mean}; variance = {variance}")
print(f"mixed Poisson mean = {float(rate_mean):.2f}")
print(f"mixed Poisson variance = {float(rate_mean+rate_var):.2f}")
