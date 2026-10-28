"""Marginalization and conditioning on a finite joint law."""
from fractions import Fraction as F

joint = {(0, 0): F(4, 10), (0, 1): F(1, 10),
         (1, 0): F(2, 10), (1, 1): F(3, 10)}
px = {x: sum(p for (a, b), p in joint.items() if a == x)
      for x in (0, 1)}
py = {y: sum(p for (a, b), p in joint.items() if b == y)
      for y in (0, 1)}
assert sum(joint.values()) == 1
conditional = joint[1, 1]/py[1]
assert conditional == F(3, 4)
assert joint[1, 1] != px[1]*py[1]
print(f"P(X=1) = {px[1]}; P(Y=1) = {py[1]}")
print(f"P(X=1 | Y=1) = {conditional}")
print(f"Joint at (1,1) = {joint[1, 1]}; product = {px[1]*py[1]}")
