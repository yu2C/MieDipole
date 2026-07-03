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

print(MSTA2(1, 2, 15))



import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the range of complex values for z
real_values = np.linspace(-2, 2, 100)
imag_values = np.linspace(-2, 2, 100)
z_real, z_imag = np.meshgrid(real_values, imag_values)
z_values = z_real + 1j * z_imag

# Calculate MSTA2 with n=2 and mp=15 for each complex z
n = 2
mp = 15
msta2_values = np.empty_like(z_values, dtype=int)
for i in range(z_values.shape[0]):
    for j in range(z_values.shape[1]):
        msta2_values[i, j] = MSTA2(z_values[i, j], n, mp)

# Transpose the matrix for the plot
msta2_values = msta2_values.T

# Plot the 3D surface
fig = plt.figure(figsize=(12, 6))

# Plot for MSTA2
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(z_imag, z_real, msta2_values, cmap='viridis')

# Add a color bar
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)

ax.set_xlabel('Imaginary part of z')
ax.set_ylabel('Real part of z')
ax.set_zlabel(f'MSTA2(z, n={n}, mp={mp})')
ax.set_title(f'MSTA2(z, n={n}, mp={mp}) for z = -2-2i to +2+2i')
ax.set_zlim(15, 30)  # Set z-axis limits
ax.set_xlim(+2, -2)  # Set x-axis limits
ax.set_ylim(-2, 2)  # Set y-axis limits


plt.show()
