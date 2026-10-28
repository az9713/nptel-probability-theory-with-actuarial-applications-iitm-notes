"""Exact family formulas, with floating-point consistency checks."""
from math import erfc, exp, isclose, sqrt

rate = 0.5
s, t = 2.0, 3.0
conditional = exp(-rate*(s + t))/exp(-rate*s)
assert isclose(conditional, exp(-rate*t))
alpha, beta = 3.0, 0.5
mean, variance = alpha/beta, alpha/beta**2
assert (mean, variance) == (6.0, 12.0)
normal_negative = 0.5*erfc(3/sqrt(2))
assert 0.0013 < normal_negative < 0.0014
print(f"Exponential residual survival at 3 = {conditional:.6f}")
print(f"Gamma(shape=3, rate=0.5): mean {mean:.1f}; variance {variance:.1f}")
print(f"Normal(mean=6, sd=2): P(X < 0) = {normal_negative:.8f}")
