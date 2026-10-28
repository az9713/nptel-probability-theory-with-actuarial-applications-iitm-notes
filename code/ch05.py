"""Binomial rare-event approximation and truncated Poisson moments."""
from math import comb, exp, factorial, isclose

n = 1000
rate = 2.0
p = rate/n
exact_zero = (1 - p)**n
poisson_zero = exp(-rate)
mass = [exp(-rate)*rate**k/factorial(k) for k in range(40)]
assert isclose(sum(mass), 1.0, abs_tol=1e-14)
mean = sum(k*q for k, q in enumerate(mass))
variance = sum((k - rate)**2*q for k, q in enumerate(mass))
assert isclose(mean, rate, abs_tol=1e-12)
assert isclose(variance, rate, abs_tol=1e-12)
binomial_two = comb(n, 2)*p**2*(1 - p)**(n - 2)
print(f"P(N=0): binomial {exact_zero:.8f}; Poisson {poisson_zero:.8f}")
print(f"P(N=2): binomial {binomial_two:.8f}; Poisson {mass[2]:.8f}")
print(f"Poisson truncated mean {mean:.6f}; variance {variance:.6f}")
