"""Original exponential-layer design, with independent quadrature checks."""
from math import exp, isclose, log


def simpson(function, upper, steps=2000):
    assert steps > 0 and steps % 2 == 0
    h = upper / steps
    total = function(0) + function(upper)
    for i in range(1, steps):
        total += (4 if i % 2 else 2) * function(i * h)
    return total * h / 3


theta, d, u, c, rate = 1000.0, 500.0, 1500.0, 0.8, 20.0
q, b = exp(-d / theta), u / theta
mean = c * q * theta * (1 - exp(-b))
second = 2 * c**2 * q * theta**2 * (1 - (1 + b) * exp(-b))
check_mean = c * simpson(lambda t: exp(-(d + t) / theta), u)
check_second = 2 * c**2 * simpson(
    lambda t: t * exp(-(d + t) / theta), u)
assert isclose(mean, check_mean, rel_tol=1e-11)
assert isclose(second, check_second, rel_tol=1e-11)
assert isclose(rate * mean, rate * q * (mean / q))
assert isclose(rate * second, rate * q * (second / q))
print(f"Payment probability: {q:.8f}")
print(f"Per-loss mean: {mean:.8f}")
print(f"Per-loss second moment: {second:.8f}")
print(f"Aggregate mean: {rate * mean:.8f}")
print(f"Aggregate variance: {rate * second:.8f}")
coinsurance_second = 0.5**2 * 2 * theta**2
deductible_q = exp(-theta * log(2) / theta)
deductible_second = 2 * deductible_q * theta**2
assert isclose(deductible_second / coinsurance_second, 2)
print("Equal-mean deductible/coinsurance aggregate variance ratio: 2")
