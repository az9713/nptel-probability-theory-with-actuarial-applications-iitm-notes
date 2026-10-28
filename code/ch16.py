"""Original exact gamma tails compared with fixed-count normal tails."""
from math import erfc, exp, isclose, sqrt


def gamma_integer_tail(shape, x):
    term = exp(-x)
    total = term
    for k in range(1, shape):
        term *= x / k
        total += term
    return total


for count in (2, 10, 50):
    threshold = count + sqrt(count)
    exact = gamma_integer_tail(count, threshold)
    normal = erfc(1 / sqrt(2)) / 2
    assert 0 < exact < 1
    print(f"n={count:2d}, threshold={threshold:.6f}, "
          f"exact={exact:.8f}, normal={normal:.8f}")
assert isclose(gamma_integer_tail(2, 3), 4 * exp(-3))
fixed_variance = 100 * 9
compound_variance = 100 * (9 + 5**2)
assert compound_variance - fixed_variance == 2500
print(f"Fixed-count variance: {fixed_variance}")
print(f"Poisson-count variance: {compound_variance}")
