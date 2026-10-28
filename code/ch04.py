"""Expectations before and after an ordinary deductible."""
from fractions import Fraction as F

law = {0: F(7, 10), 100: F(2, 10), 500: F(1, 10)}
assert sum(law.values()) == 1
mean = sum(x*p for x, p in law.items())
second = sum(x*x*p for x, p in law.items())
variance = second - mean*mean
payment = sum(max(x - 100, 0)*p for x, p in law.items())
positive = sum(p for x, p in law.items() if x > 100)
assert (mean, variance, payment) == (70, 22100, 40)
assert payment/positive == 400
print(f"E[X] = {mean}; Var(X) = {variance}")
print(f"E[(X - 100)+] per loss = {payment}")
print(f"Positive-payment probability = {positive}")
print(f"Mean per positive payment = {payment/positive}")
