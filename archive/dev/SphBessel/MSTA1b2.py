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
from mpl_toolkits.mplot3d import Axes3D

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
z_real, z_imag = np.meshgrid(real_values, imag_values)
z_values = z_real + 1j * z_imag

# Compute MSTA1 for each complex z
msta_values = np.empty_like(z_values, dtype=float)
for i in range(z_values.shape[0]):
    for j in range(z_values.shape[1]):
        msta_values[i, j] = MSTA1(z_values[i, j], 200)

# Plot the 3D surface with modifications
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(z_imag, z_real, msta_values, cmap='viridis')
ax.set_xlabel('Imaginary part of z')
ax.set_ylabel('Real part of z')
ax.set_zlabel('MSTA1(z, 200)')
ax.set_title('MSTA1(z, 200) for z = -2-2i to +2+2i')

# Set y-axis range to 60-140
ax.set_zlim(60, 140)
ax.set_xlim(2, -2)
ax.set_ylim(-2, 2)

# Customize colorbar
colorbar = plt.colorbar(surf, ax=ax, shrink=0.5, aspect=10)
colorbar.set_label('MSTA1(z, 200)')

plt.show()
