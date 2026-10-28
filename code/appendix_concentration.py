"""Exact algebraic bounds for an exponential sample mean; no simulation."""
from math import exp, log

mean = 2000.0
n = 20
threshold = 3000.0
delta = threshold - mean
markov = mean / threshold
chebyshev = mean ** 2 / (n * delta ** 2)
ratio = threshold / mean
chernoff = exp(-n * (ratio - 1 - log(ratio)))
assert 0 < chernoff < chebyshev < markov < 1
print(f'Markov upper-tail bound:    {markov:.6f}')
print(f'Chebyshev two-tail bound:   {chebyshev:.6f}')
print(f'Chernoff upper-tail bound:  {chernoff:.6f}')
for sample_size in [20, 100, 1000]:
    bound = min(1.0, mean ** 2 / (sample_size * delta ** 2))
    print(f'n={sample_size:4d}: Chebyshev bound {bound:.6f}')
