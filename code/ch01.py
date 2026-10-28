"""Exact enumeration of a uniform audit without replacement."""
from fractions import Fraction
from itertools import combinations
from math import comb

audits = list(combinations(range(20), 4))
exactly_two = sum(sum(label < 8 for label in a) == 2 for a in audits)
none_marked = sum(all(label >= 8 for label in a) for a in audits)
probability = Fraction(exactly_two, len(audits))
assert len(audits) == comb(20, 4)
assert exactly_two == comb(8, 2)*comb(12, 2)
assert none_marked == comb(12, 4)
assert probability == Fraction(616, 1615)
print(f"Audits: {len(audits)}; exactly two marked: {exactly_two}")
print(f"P(exactly two) = {probability} = {float(probability):.6f}")
print(f"P(at least one) = {1 - Fraction(none_marked, len(audits))}")
