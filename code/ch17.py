"""Original exact discrete deductible calculation, using fractions."""
from fractions import Fraction as F

losses = [(100, F(1, 2)), (400, F(3, 10)), (1000, F(1, 5))]
deductible = 250
payments = [(max(x - deductible, 0), p) for x, p in losses]
q = sum(p for y, p in payments if y > 0)
mean = sum(y * p for y, p in payments)
second = sum(y**2 * p for y, p in payments)
variance = second - mean**2
positive_mean = sum(y * p / q for y, p in payments if y > 0)
positive_second = sum(y**2 * p / q for y, p in payments if y > 0)
positive_variance = positive_second - positive_mean**2
assert mean == q * positive_mean == 195
assert second == q * positive_second == 119250
assert variance == q * positive_variance + q * (1 - q) * positive_mean**2
assert variance == 81225
print(f"Payment probability: {q}")
print(f"Per-loss mean, second moment, variance: {mean}, {second}, {variance}")
print(f"Per-payment mean, variance: {positive_mean}, {positive_variance}")
