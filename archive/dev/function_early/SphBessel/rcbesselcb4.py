import numpy as np
import matplotlib.pyplot as plt
from nrcbesselc import rcbesselc  # Assuming rcbesselc is defined in rcbesselc.py

# Define the range of real values for z
z_values = np.linspace(0, 14, 100)

# Initialize arrays for rcj values for different n values
n_values = [1, 2, 3]
rcj_values = np.zeros((len(n_values), len(z_values)), dtype=complex)

# Calculate rcj for each n and each real value of z
for i, n in enumerate(n_values):
    for j, z_real in enumerate(z_values):
        z = complex(z_real, 0)  # Imaginary part is 0 for this case
        rcj, _, _, _ = rcbesselc(z, n)
        rcj_values[i, j] = rcj[n]

# Plot rcj for different n values as a function of the real part of z
plt.figure(figsize=(10, 6))
for i, n in enumerate(n_values):
    plt.plot(z_values, rcj_values[i].real, label=f'n={n}')

plt.xlabel('Real part of z')
plt.ylabel('rcj')
plt.title('rcj for z from 0 to 14, n=1 to 3')
plt.xlim(0, 14)
plt.ylim(-1.5, 1.5)
plt.legend()
plt.grid(True)
plt.show()
