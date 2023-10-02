## Sub-Functions of Spherical Bessel/Riccati-Bessel Functions
# Ref: Computation of Special Functions (1996)
#        Authors: Shanjie Zhang, Jianming Jin
#----------------------------------------------
# Called by sbesselc and rcbesselc
# Determine the starting point for backward recurrence such that all Jn(x) has mp significant digits
# Input :  x     --- Argument of Jn(x)
#          n     --- order of Jn(x)
#          mp    --- significant digits
# Output : MSTA2 --- Starting point

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def envj(n, z):
    n = max(1, abs(n))
    result = 0.5 * np.log10(6.28 * n) - n * np.log10(1.36 * z / n)
    return result

def MSTA2(z, n, mp):
    a0  = abs(z)
    hmp = 0.5 * mp
    ejn = envj(n, a0)
    
    if ejn <= hmp:  # If |JM(x)| >= e-(p/2)
        obj = mp
        n0  = int(1.1 * a0)
    else:  # Otherwise
        obj = hmp + ejn
        n0  = n
    
    f0 = envj(n0, a0) - obj
    n1 = n0 + 5
    f1 = envj(n1, a0) - obj
    
    for _ in range(20):
        nn = n1 - (n1 - n0) / (1.0 - f0 / f1)
        nn = int(nn)  # Convert nn to an integer
        f  = envj(nn, a0) - obj
        
        if abs(nn - n1) < 1:
            break
        
        n0 = n1
        f0 = f1
        n1 = nn
        f1 = f
    
    return nn + 10

print(MSTA2(2+2j, 2, 15))



import numpy as np
import matplotlib.pyplot as plt

# Define the range of n values
n_values = np.arange(2, 51)

# Fixed complex value for z
z = 2 + 2j

# Calculate MSTA2 for each n
mp = 15
msta2_values = np.array([MSTA2(z, n, mp) for n in n_values])

# Plot the values
plt.figure(figsize=(10, 6))
plt.plot(n_values, msta2_values, marker='o')
plt.xlabel('n')
plt.ylabel(f'MSTA2(z={z}, n, mp={mp})')
plt.title(f'MSTA2(z={z}, n, mp={mp}) for n=2 to 50')
plt.ylim(25, 65)
plt.xlim(0, 50)


plt.grid(True)
plt.show()
