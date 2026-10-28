"""Original finite-binomial benchmark for continuity correction."""
from math import comb, erfc, sqrt


def normal_tail(z):
    return erfc(z / sqrt(2)) / 2


n, p, k = 100, 0.1, 15
mean = n * p
sd = sqrt(n * p * (1 - p))
exact = sum(comb(n, j) * p**j * (1 - p)**(n - j)
            for j in range(k, n + 1))
corrected = normal_tail((k - 0.5 - mean) / sd)
uncorrected = normal_tail((k - mean) / sd)
assert 0 < exact < 1
assert abs(corrected - exact) < abs(uncorrected - exact)
assert (k - 1) + 0.5 == k - 0.5
print(f"P(B >= {k}), B ~ Binomial({n}, {p})")
print(f"Exact finite sum: {exact:.8f}")
print(f"Normal, corrected: {corrected:.8f}")
print(f"Normal, uncorrected: {uncorrected:.8f}")
print(f"Corrected absolute error: {abs(corrected - exact):.8f}")
