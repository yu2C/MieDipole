import numpy as np
import matplotlib.pyplot as plt
from scipy.special import riccati_jn

# Define the range of real values for z
z_values = np.linspace(0, 14, 100)

# Initialize arrays for drcj values for different n values
n_values = [1, 2, 3]
drcj_values = np.zeros((len(n_values), len(z_values)), dtype=complex)

# Calculate drcj for each n and each real value of z
for i, n in enumerate(n_values):
    for j, z_real in enumerate(z_values):
        z = complex(z_real, 0)  # Imaginary part is 0 for this case
        rcj, _, drcj, _ = riccati_jn(n, z)
        drcj_values[i, j] = drcj  # Derivative of Riccati-Hankel

# Plot drcj for different n values as a function of the real part of z
plt.figure(figsize=(10, 6))
for i, n in enumerate(n_values):
    plt.plot(z_values, drcj_values[i].real, label=f'drcj, n={n}')

plt.xlabel('Real part of z')
plt.ylabel('drcj')
plt.title('Derivative of Riccati-Bessel function (drcj) for z from 0 to 14')
plt.legend()
plt.grid(True)
plt.show()
