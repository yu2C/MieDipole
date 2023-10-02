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

# Modify sbesselc to accept a specific z value
def sbesselc(z, n):
    a0 = abs(z)
    nm = n
    
    # If circle checked. Treat z = 0 as a special case
    if a0 < 1e-60:
        csj    = np.zeros(n + 1, dtype=complex)
        csy    = np.full(n + 1, -1e300, dtype=complex)
        csy[0] = 1.0 + 0.0j
        return csj
    
    csj    = np.zeros(n + 1, dtype=complex)
    csj[0] = np.sin(z) / z
    
    if n >= 1:
        csj[1] = (csj[0] - np.cos(z)) / z
    
    if n >= 2: # Backward recurrence
        csa = csj[0]
        csb = csj[1]
        m   = MSTA1(a0, 200) 

        if m < n:
            nm = m
        else: 
            m = MSTA2(a0, n, 15)
        
        cf0 = 0.0 
        cf1 = 1.0 - 100
        
        for k in range(m, -1, -1):
            cf = (2.0 * k + 3.0) * cf1 / z - cf0
            
            if k <= nm:
                csj[k] = cf
            
            cf0 = cf1
            cf1 = cf
        
        if abs(csa) > abs(csb):
            cs = csa / cf
        else:
            cs = csb / cf0
        
        for k in range(min(nm, n) + 1):
            csj[k] = cs * csj[k]
    
    return csj

import numpy as np
import matplotlib.pyplot as plt
from sbesselc import sbesselc  # Assuming sbesselc is defined in sbesselc.py

# Define the range of real values for z
z_values = np.linspace(0, 14, 140)

# Initialize array for csj values
csj_values = np.zeros_like(z_values, dtype=complex)

# Calculate csj for n=2 for each real value of z
n = 2
for i, z_real in enumerate(z_values):
    z = complex(z_real, 0)  # Imaginary part is 0 for this case
    csj, _ = sbesselc(z, n)
    csj_values[i] = csj[n]

# Print the csj values
print('csj values for z from 0 to 14:')
print(csj_values)

# Plot csj against z
plt.figure()
plt.plot(z_values, csj_values.real, 'b-', linewidth=1.5, label='Real part of csj')
plt.plot(z_values, csj_values.imag, 'r--', linewidth=1.5, label='Imaginary part of csj')
plt.xlabel('Real part of z')
plt.ylabel('csj')
plt.title('csj for z from 0 to 14, n=2')
plt.legend(loc='best')
plt.grid(True)
plt.show()
