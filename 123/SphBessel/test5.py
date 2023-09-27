import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.special import riccati_yn

# Define the range for z (real and imaginary parts)
real_parts = np.linspace(-2, 2, 100)
imaginary_parts = np.linspace(-2, 2, 100)
real_mesh, imag_mesh = np.meshgrid(real_parts, imaginary_parts)
z_values = real_mesh + 1j * imag_mesh

# Initialize an array to store rcy values
rcy_values = np.zeros(z_values.shape, dtype=complex)

# Calculate rcy for z = -2-2i to +2+2i and n = 2
n = 2
for i in range(z_values.shape[0]):
    for j in range(z_values.shape[1]):
        z = z_values[i, j]
        real_part, _ = riccati_yn(n, z)
        rcy_values[i, j] = real_part

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(real_mesh, imag_mesh, rcy_values.real, cmap='viridis')
fig.colorbar(surf, ax=ax, label='Real part of rcy')
ax.set_xlabel('Real part of z')
ax.set_ylabel('Imaginary part of z')
ax.set_zlabel('Real part of rcy')
ax.set_title('3D Plot of rcy for z = -2-2i to +2+2i (n = 2)')

plt.show()
