"""Original two-class conditional aggregate model."""
from math import exp, isclose

classes = [(0.2, 4.0, 200.0), (0.8, 1.0, 100.0)]
deductible = 50.0
rows = []
for weight, rate, theta in classes:
    q = exp(-deductible / theta)
    mean = rate * q * theta
    variance = rate * 2 * q * theta**2
    rows.append((weight, rate, q, mean, variance))
mean = sum(w * m for w, rate, q, m, v in rows)
within = sum(w * v for w, rate, q, m, v in rows)
between = sum(w * (m - mean)**2 for w, rate, q, m, v in rows)
raw_second = sum(w * (v + m**2) for w, rate, q, m, v in rows)
assert isclose(within + between, raw_second - mean**2)
no_loss = [w * exp(-rate) for w, rate, theta in classes]
posterior = no_loss[0] / sum(no_loss)
no_payment = [w * exp(-rate * q) for w, rate, q, m, v in rows]
posterior_zero = no_payment[0] / sum(no_payment)
payment_weights = [w * rate * q for w, rate, q, m, v in rows]
high_paid_share = payment_weights[0] / sum(payment_weights)
assert posterior < 0.2
assert high_paid_share > 0.5
print(f"P(H | no gross loss): {posterior:.8f}")
print(f"P(H | no payment): {posterior_zero:.8f}")
print(f"High-class share of positive payments: {high_paid_share:.8f}")
print(f"Aggregate mean: {mean:.8f}")
print(f"Within-class variance component: {within:.8f}")
print(f"Between-class variance component: {between:.8f}")
print(f"Total aggregate variance: {within + between:.8f}")
