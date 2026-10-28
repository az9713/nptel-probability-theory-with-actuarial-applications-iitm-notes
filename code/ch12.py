"""Exact total moments and conditional prediction in two risk classes."""
from fractions import Fraction as F


classes = [(F(4, 5), F(1, 10)), (F(1, 5), F(2, 5))]
joint = [(weight*(p if x else 1-p), x, p)
         for weight, p in classes for x in (0, 1)]
mean = sum(prob*x for prob, x, p in joint)
variance = sum(prob*(x-mean)**2 for prob, x, p in joint)
within = sum(weight*p*(1-p) for weight, p in classes)
between = sum(weight*(p-mean)**2 for weight, p in classes)
prediction_error = sum(prob*(x-p)**2 for prob, x, p in joint)
constant_error = sum(prob*(x-F(1, 5))**2 for prob, x, p in joint)
extra = sum(weight*(p-F(1, 5))**2 for weight, p in classes)
assert sum(prob for prob, x, p in joint) == 1
assert variance == within + between
assert prediction_error == within
assert constant_error == within + extra
print(f"mean = {float(mean):.4f}; variance = {float(variance):.4f}")
print(f"within = {float(within):.4f}; between = {float(between):.4f}")
print(f"class prediction error = {float(prediction_error):.4f}")
print(f"constant 0.2 prediction error = {float(constant_error):.4f}")
