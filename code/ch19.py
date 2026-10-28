"""Original exact enumeration of a finite random sum."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product

counts = [(0, F(1, 2)), (2, F(1, 2))]
severities = [(1, F(1, 2)), (3, F(1, 2))]
aggregate = defaultdict(F)
for n, pn in counts:
    for outcomes in product(severities, repeat=n):
        amount, probability = 0, pn
        for value, p in outcomes:
            amount += value
            probability *= p
        aggregate[amount] += probability
assert sum(aggregate.values()) == 1
mean = sum(s * p for s, p in aggregate.items())
second = sum(s**2 * p for s, p in aggregate.items())
assert mean == 2
assert second - mean**2 == 5
print("Aggregate law: " + ", ".join(
    f"{s}: {p}" for s, p in sorted(aggregate.items())))
print(f"Aggregate mean, variance: {mean}, {second - mean**2}")
rate, q, mp, rp = F(12), F(2, 5), F(300), F(180000)
assert rate * (q * mp) == (rate * q) * mp == 1440
assert rate * (q * rp) == (rate * q) * rp == 864000
print("Both Poisson count bases: mean=1440, variance=864000")
