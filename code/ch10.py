"""Enumerate an independent convolution and check its moments."""
from collections import defaultdict
from fractions import Fraction as F
from math import isclose


def moments(pmf):
    mean = sum(x*p for x, p in pmf.items())
    variance = sum((x-mean)**2*p for x, p in pmf.items())
    return mean, variance


def trapezoid_density(x):
    return max(0, min(1, x)-max(0, x-2))/2


left = {0: F(3, 4), 1: F(1, 4)}
right = {0: F(1, 2), 1: F(1, 2)}
total = defaultdict(F)
for x, px in left.items():
    for y, py in right.items():
        total[x+y] += px*py
assert sum(total.values()) == 1
mean, variance = moments(total)
assert mean == moments(left)[0] + moments(right)[0]
assert variance == moments(left)[1] + moments(right)[1]
count = 30000
width = 3/count
area = width*sum(trapezoid_density((i+.5)*width) for i in range(count))
assert isclose(area, 1, abs_tol=1e-9)
print("sum pmf = " + ", ".join(f"{x}:{total[x]}" for x in sorted(total)))
print(f"sum mean = {mean}; variance = {variance}")
print(f"uniform trapezoid density area = {area:.8f}")
