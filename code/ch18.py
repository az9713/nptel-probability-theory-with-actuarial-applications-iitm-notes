"""Original layer check using exact step-survival integration."""
from fractions import Fraction as F
from math import exp

losses = [(0, F(1, 5)), (2, F(3, 10)), (5, F(1, 2))]
d, u, c = 1, 4, F(1, 2)
law = [(c * min(max(x - d, 0), u), p) for x, p in losses]
mean = sum(y * p for y, p in law)
second = sum(y**2 * p for y, p in law)
tail_mean = F(0)
tail_second = F(0)
for x, p in losses:
    width = min(max(x - d, 0), u)
    tail_mean += c * p * width
    tail_second += c**2 * p * width**2
assert mean == tail_mean == F(23, 20)
assert second == tail_second == F(83, 40)
variance = second - mean**2
assert 0 <= variance <= mean * (c * u - mean)
print(f"Discrete layer mean: {float(mean):.6f}")
print(f"Discrete layer second moment: {float(second):.6f}")
print(f"Discrete layer variance: {float(variance):.6f}")
theta, d, u, c = 2.0, 1.0, 2.0, 0.5
q, b = exp(-d / theta), u / theta
m = c * q * theta * (1 - exp(-b))
r = 2 * c**2 * q * theta**2 * (1 - (1 + b) * exp(-b))
assert 0 < r < c * u * m
print(f"Exponential layer mean, second moment: {m:.6f}, {r:.6f}")
