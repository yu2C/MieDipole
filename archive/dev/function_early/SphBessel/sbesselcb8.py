import numpy as np
import matplotlib.pyplot as plt
from sbesselc import sbesselc  # Assuming sbesselc is defined in sbesselc.py

# Define the range of real values for z
z_values = np.linspace(1, 14, 130)

# Initialize arrays for csy values for different n values
n_values = [1, 2, 3]
csy_values = np.zeros((len(n_values), len(z_values)), dtype=complex)

# Calculate csy for each n and each real value of z
for i, n in enumerate(n_values):
    for j, z_real in enumerate(z_values):
        z = complex(z_real, 0)  # Imaginary part is 0 for this case
        _, csy = sbesselc(z, n)
        csy_values[i, j] = csy[n]  # Python uses 0-based indexing for arrays

# Plot csy for different n values as a function of z
plt.figure(figsize=(10, 6))
for i, n in enumerate(n_values):
    plt.plot(z_values, csy_values[i].real, label=f'n={n}')

plt.xlabel('Real part of z')
plt.ylabel('csy')
plt.title('csy for z from 1 to 14 for n=1 to 3')
plt.legend()
plt.grid(True)
plt.xlim(1, 14)  # Fix x-axis from 2 to 14
plt.ylim(-0.4, 0.4)  # Fix x-axis from 2 to 14

plt.show()
