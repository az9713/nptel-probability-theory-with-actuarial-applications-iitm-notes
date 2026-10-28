"""Check transformed supports, inverse branches, and payment atoms."""
from math import exp, isclose


def midpoint(function, left, right, count=10000):
    width = (right-left)/count
    return width*sum(function(left+(i+.5)*width) for i in range(count))


# Substitute y=u^2, dy=2u du in the square-density pieces.
branch_mass = midpoint(lambda u: 2/3, 0, 1)
branch_mass += midpoint(lambda u: 1/3, 1, 2)
mean_square = midpoint(lambda u: 2*u*u/3, 0, 1)
mean_square += midpoint(lambda u: u*u/3, 1, 2)
assert isclose(branch_mass, 1, abs_tol=1e-10)
assert isclose(mean_square, 1, abs_tol=1e-8)
zero_mass = 1-exp(-1)
cap_mass = exp(-3)
continuous_mass = exp(-1)-exp(-3)
assert isclose(zero_mass+cap_mass+continuous_mass, 1)
print(f"asymmetric square density mass = {branch_mass:.8f}")
print(f"asymmetric square mean = {mean_square:.8f}")
print(f"payment atoms: zero = {zero_mass:.8f}, cap = {cap_mass:.8f}")
print(f"continuous payment mass = {continuous_mass:.8f}")
