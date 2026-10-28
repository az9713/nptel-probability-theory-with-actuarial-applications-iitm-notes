"""Check compound transforms, cumulants, and a Poisson tail bound."""
from math import exp, factorial, isclose, log


rate = 2
t = .1
severity_mgf = (exp(t)+exp(3*t))/2
closed = exp(rate*(severity_mgf-1))
count_sum = sum(exp(-rate)*rate**n/factorial(n)*severity_mgf**n
                for n in range(60))
assert isclose(count_sum, closed, rel_tol=1e-12)
cumulants = [rate*(1+3**r)/2 for r in range(1, 5)]
assert cumulants == [4, 10, 28, 82]
tail = 1-exp(-rate)*sum(rate**k/factorial(k) for k in range(6))
bound = exp(-6*log(6/rate)+6-rate)
assert 0 < tail < bound < 1
assert isclose(exp(rate*((1+1)/2-1)), 1)
print(f"compound MGF at 0.1 = {closed:.10f}")
print(f"count-sum MGF at 0.1 = {count_sum:.10f}")
print("compound cumulants = " + ", ".join(f"{x:g}" for x in cumulants))
print(f"Poisson P(N >= 6) = {tail:.10f}")
print(f"Chernoff bound = {bound:.10f}")
