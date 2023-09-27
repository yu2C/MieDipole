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

def sbesselc(z, n):
    a0 = abs(z)
    nm = n
    
    # If circle checked. Treat z = 0 as a special case
    if a0 < 1e-60:
        csj    = np.zeros(n + 1, dtype=complex)
        csy    = np.full(n + 1, -1e300, dtype=complex)
        csy[0] = 1.0 + 0.0j
        return csj, csy
    
    # checked. 
    csj    = np.zeros(n + 1, dtype=complex)
    csj[0] = np.sin(z) / z
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
    
    csy = np.full(n + 1, 1e200, dtype=complex)
    csy[0] = -np.cos(z) / z
    csy[1] = (csy[0] - np.sin(z)) / z
    
    for k in range(2, min(nm, n) + 1): # calculate yn(z) by W as n >= 2
        
        if abs(csj[k - 1]) > abs(csj[k - 2]): # GT. or GE.?
            csy[k] = (csj[k] * csy[k - 1] - 1.0 / z ** 2) / csj[k - 1]
        else:
            csy[k] = (csj[k] * csy[k - 2] - (2.0 * k - 1.0) / z ** 3) / csj[k - 2]
    
    return csj, csy





# Set n values
n = 2

# Create an array of complex numbers for z
z_values = [complex(x, y) for x in range(1, 11) for y in range(1, 11)]

# Calculate sbesselc for each z value
csj_values = [sbesselc(z, n)[0] for z in z_values]

# Separate real and imaginary parts
real_parts = np.real(csj_values)
imag_parts = np.imag(csj_values)

# Create a figure and axis
fig, ax = plt.subplots()

# Plot the real and imaginary parts
ax.scatter(real_parts, imag_parts, label='sbesselc')

# Set axis limits
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)

# Add labels
ax.set_xlabel('Re(sbesselc)')
ax.set_ylabel('Im(sbesselc)')

# Show the plot
plt.grid(True)
plt.legend()
plt.show()



















