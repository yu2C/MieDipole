## Spherical Bessel Functions (Complex Argument)
# Ref: Computation of Special Functions (1996)
#        Authors: Shanjie Zhang, Jianming Jin
#----------------------------------------------
# Called by SphBessel
# Substitite j = k + 1 with k in array-like

import numpy as np
import matplotlib.pyplot as plt

def MSTA1(z, mp):
    a0 = abs(z)
    n0 = int(1.1 * a0) + 1
    f0 = envj(n0, a0) - mp
    n1 = n0 + 5
    f1 = envj(n1, a0) - mp
    
    for _ in range(20):
        nn = n1 - (n1 - n0) / (1.0 - f0 / f1)
        nn = int(nn)
        f = envj(nn, a0) - mp
        
        if abs(nn - n1) < 1:
            break
        
        n0 = n1
        f0 = f1
        n1 = nn
        f1 = f
    
    return nn

def MSTA2(z, n, mp):
    a0 = abs(z)
    hmp = 0.5 * mp
    ejn = envj(n, a0)
    
    if ejn <= hmp:
        obj = mp
        n0 = int(1.1 * a0)
    else:
        obj = hmp + ejn
        n0 = n
    
    f0 = envj(n0, a0) - obj
    n1 = n0 + 5
    f1 = envj(n1, a0) - obj
    
    for _ in range(20):
        nn = n1 - (n1 - n0) / (1.0 - f0 / f1)
        nn = int(nn)
        f = envj(nn, a0) - obj
        
        if abs(nn - n1) < 1:
            break
        
        n0 = n1
        f0 = f1
        n1 = nn
        f1 = f
    
    return nn + 10

def envj(n, z):
    n = max(1, abs(n))
    result = 0.5 * np.log10(6.28 * n) - n * np.log10(1.36 * z / n)
    return result

import numpy as np
import matplotlib.pyplot as plt
from sbesselc import sbesselc  # Assuming sbesselc is defined in sbesselc.py

# Define the range of real values for z
z_values = np.linspace(0, 14, 140)

# Initialize arrays for csj values for different n values
n_values = [1, 2, 3]
csj_values = {n: np.zeros_like(z_values, dtype=complex) for n in n_values}

# Calculate csj for each n and each real value of z
for n in n_values:
    for i, z_real in enumerate(z_values):
        z = complex(z_real, 0)  # Imaginary part is 0 for this case
        csj, _ = sbesselc(z, n)
        csj_values[n][i] = csj[n]

# Print the csj values
print('csj values for z from 0 to 14:')
for n in n_values:
    print(f'n={n}: {csj_values[n]}')

# Plot csj for different n values as a function of the real part of z
plt.figure(figsize=(10, 6))
for n in n_values:
    plt.plot(z_values, csj_values[n].real, label=f'csj, n={n}')

plt.xlabel('Real part of z')
plt.ylabel('csj')
plt.title('csj for z from 0 to 14 for n=1 to 3')
plt.legend()
plt.grid(True)
plt.xlim(0, 14)  # Fix x-axis from 0 to 14
plt.ylim(-0.5, 1.0)  # Fix x-axis from 0 to 14

plt.show()
