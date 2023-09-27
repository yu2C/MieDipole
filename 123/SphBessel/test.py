import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.special import spherical_jn

# Define the range of complex values for z
real_values = np.linspace(-2, 2, 100)
imag_values = np.linspace(-2, 2, 100)
z_real, z_imag = np.meshgrid(real_values, imag_values)
z_values = z_real + 1j * z_imag

# Compute jn(2, z) for each complex z
n = 2
jn_values = spherical_jn(n, np.abs(z_values))

# Plot the 3D surface
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(z_real, z_imag, np.real(jn_values), cmap='viridis')

ax.set_xlabel('Real part of z')
ax.set_ylabel('Imaginary part of z')
ax.set_zlabel(f'jn({n}, z)')
ax.set_title(f'jn({n}, z) for z = -2-2i to +2+2i')
#ax.set_zlim(-0.4, 0.4)  # Limit z-axis for better visualization
ax.view_init(elev=20, azim=-45)  # Adjust view angle for better visualization
plt.show()
