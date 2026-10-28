"""Bayes updating and pairwise independence, using exact arithmetic."""
from fractions import Fraction as F
from itertools import product

prior = F(1, 100)
sensitivity = F(9, 10)
false_positive = F(1, 20)
positive = prior*sensitivity + (1 - prior)*false_positive
posterior = prior*sensitivity/positive
assert posterior == F(2, 13)
space = list(product((0, 1), repeat=2))
events = [lambda a, b: a == 1, lambda a, b: b == 1,
          lambda a, b: a != b]
for i in range(3):
    for j in range(i):
        joint = sum(events[i](*s) and events[j](*s) for s in space)
        assert F(joint, 4) == F(1, 4)
triple = sum(all(e(*s) for e in events) for s in space)
assert triple == 0
print(f"P(positive) = {positive}")
print(f"P(target | positive) = {posterior} = {float(posterior):.6f}")
print("Three events: each marginal 1/2; each pair 1/4; triple 0")
