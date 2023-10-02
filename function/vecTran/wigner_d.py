import numpy as np
from scipy.special import factorial as f

# Define the wigner_d function analytically 
def wigner_d(j, m, mp, beta):
    smin = max(0, m - mp)
    smax = min(j + m, j - mp)
    
    for s in range(smin, smax + 1):
        phase = (-1)**(mp - m + s)
        sigma = ((-1)**(mp - m + s) * np.cos(beta / 2)**(2j + m - mp -2 * s) * np.sin(beta / 2)**(mp -m + 2 * s)) / (f(j + m -s) * f(s) * f(mp - m + s) * f(j - mp - s))
    return np.sqrt(f((j + mp)) * f(j - mp) * f(j + m) * f(j - m)) * sigma

print(wigner_d(0.5, 1, -1, 0))  
