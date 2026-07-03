import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.special import spherical_yn
from matplotlib import cm

# Define the range of complex values for z
real_values = np.linspace(-2, 2, 100)
imag_values = np.linspace(-2, 2, 100)
z_real, z_imag = np.meshgrid(real_values, imag_values)
z_values = z_real + 1j * z_imag

# Calculate Y2 for each complex z (excluding z = 0)
n = 2
Y2_values = np.zeros_like(z_values, dtype=complex)
for i in range(z_values.shape[0]):
    for j in range(z_values.shape[1]):
        if z_values[i, j] != 0:  # Exclude z = 0
            Y2_values[i, j] = spherical_yn(n, z_values[i, j])

# Plot the 3D surface
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(111, projection='3d')
surface = ax.plot_surface(z_real, z_imag, np.abs(Y2_values), cmap=cm.viridis, edgecolor='none')
ax.set_xlabel('Real part of z')
ax.set_ylabel('Imaginary part of z')
ax.set_zlabel('|Y2(z)|')
ax.set_title('Spherical Bessel Function of the Second Kind (Y2) for n=2')
ax.view_init(elev=20, azim=-45)  # Adjust view angle for better visualization
ax.set_zlim(0, np.abs(Y2_values).max())  # Limit z-axis for better visualization
ax.invert_yaxis()  # Invert y-axis to match the MATLAB plot

# Add a colorbar
colorbar = plt.colorbar(surface, ax=ax, shrink=0.5, aspect=10)
colorbar.set_label('Magnitude')

plt.show()
