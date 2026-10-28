"""Check the median order-statistic density against its count event."""
from math import comb, isclose


def integrate(function, count=20000):
    return sum(function((i+.5)/count) for i in range(count))/count


def density(x):
    return 30*x*x*(1-x)**2


threshold = .4
cdf = sum(comb(5, j)*threshold**j*(1-threshold)**(5-j)
          for j in range(3, 6))
count = 20000
width = threshold/count
cdf_integral = width*sum(density((i+.5)*width) for i in range(count))
mean = integrate(lambda x: x*density(x))
variance = integrate(lambda x: (x-.5)**2*density(x))
assert isclose(integrate(density), 1, abs_tol=1e-8)
assert isclose(cdf, cdf_integral, abs_tol=1e-8)
assert isclose(mean, .5, abs_tol=1e-8)
assert isclose(variance, 1/28, abs_tol=1e-8)
print(f"five-observation median CDF at 0.4 = {cdf:.8f}")
print(f"median mean = {mean:.8f}; variance = {variance:.8f}")
print(f"100-claim maximum threshold probability = {1-.99**100:.8f}")
