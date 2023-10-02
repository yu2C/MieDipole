## Sub-Functions of Spherical Bessel/Riccati-Bessel Functions
# Ref: Computation of Special Functions (1996)
#        Authors: Shanjie Zhang, Jianming Jin
#----------------------------------------------
# Called by sbesselc and rcbesselc

# Determine the starting point M to calculate Bessel function by backward recurrence
# Input  : z     --- Argument of Jn(z)
#          mp    --- Value of magnitude
# Output : MSTA1 --- Starting point
import numpy as np 
import matplotlib.pyplot as plt

def envj(n, z):
    n = max(1, abs(n))
    result = 0.5 * np.log10(6.28 * n) - n * np.log10(1.36 * z / n)
    return result

def MSTA1(z, mp):
    a0 = abs(z)
    n0 = int(1.1 * a0) + 1
    f0 = envj(n0, a0) - mp
    n1 = n0 + 5
    f1 = envj(n1, a0) - mp
    
    for _ in range(20):
        nn = n1 - (n1 - n0) / (1.0 - f0 / f1)
        nn = int(nn)  # Convert nn to an integer (nn should not be int.)
        f  = envj(nn, a0) - mp
        
        if abs(nn - n1) < 1:
            break
        
        n0 = n1
        f0 = f1
        n1 = nn
        f1 = f
    
    return nn


# Define the range of complex values for z
real_values = np.linspace(-2, 2, 100)
imag_values = np.linspace(-2, 2, 100)
z_values = real_values[:, np.newaxis] + 1j * imag_values

# Compute MSTA1 for each complex z
msta_values = np.empty_like(z_values, dtype=int)
for i in range(z_values.shape[0]):
    for j in range(z_values.shape[1]):
        msta_values[i, j] = MSTA1(z_values[i, j], 200)

# Plot the results
plt.figure(figsize=(10, 6))
plt.contourf(real_values, imag_values, msta_values, cmap='viridis')
plt.colorbar(label='MSTA1(z, 200)')
plt.xlabel('Real part of z')
plt.ylabel('Imaginary part of z')
plt.title('MSTA1(z, 200) for z = -2-2i to +2+2i')
plt.show()
