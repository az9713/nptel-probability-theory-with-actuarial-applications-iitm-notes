"""Exact covariance and portfolio-variance examples."""
from fractions import Fraction as F


table = [(0, 0, F(2, 5)), (0, 1, F(1, 10)),
         (1, 0, F(1, 10)), (1, 1, F(2, 5))]
mean_x = sum(x*p for x, y, p in table)
mean_y = sum(y*p for x, y, p in table)
var_x = sum((x-mean_x)**2*p for x, y, p in table)
var_y = sum((y-mean_y)**2*p for x, y, p in table)
cov = sum((x-mean_x)*(y-mean_y)*p for x, y, p in table)
var_sum = sum((x+y-mean_x-mean_y)**2*p for x, y, p in table)
assert sum(p for x, y, p in table) == 1
assert var_sum == var_x + var_y + 2*cov == F(4, 5)
values = [-1, 0, 1]
mean_square = sum(F(x*x, 3) for x in values)
uncorrelated = sum(F(x, 3)*(x*x-mean_square) for x in values)
assert uncorrelated == 0
assert F(1, 3) != F(1, 3)*F(1, 3)  # X=0 and X^2=0 coincide.
print(f"covariance = {cov}; sum variance = {var_sum}")
print(f"dependent square example covariance = {uncorrelated}")
print(f"100-policy average variance = {100*(.05+.95/100):.2f}")
