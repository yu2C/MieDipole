import numpy as np
from scipy.special import lpmv

l = 1
m_values = [-1, 0, 1]
x = np.cos(np.pi / 4)  # Example value of x

for m in m_values:
    P = lpmv(m, l, x)
    
    if m < 0:
        # Apply the relationship for negative m
        P *= (-1) ** (-m) * np.math.factorial(l - m) / np.math.factorial(l + m)
    
    print(f'P_{m}^{l}({x}) = {P}')
