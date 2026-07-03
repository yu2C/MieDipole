import numpy as np
import matplotlib.pyplot as plt
from scipy.special import spherical_jn as sph_jn

# Define the range of z values
z_values = np.linspace(0, 15, 1)

# Initialize arrays to store jn values for different n
jn_values = []

# Calculate jn for each n and each value of z
for n in range(4):  # n from 0 to 3
    jn_n = sph_jn(n, z_values)[0]  # Extract the jn values from the result tuple
    jn_values.append(jn_n)

# Plot jn for different n values as a function of z
plt.figure(figsize=(10, 6))
for i, n in enumerate(range(4)):
    plt.plot(z_values, jn_values[i], label=f'j{n}(z)')

plt.xlabel('z')
plt.ylabel('jn(z)')
plt.title('Spherical Bessel Functions jn(z) for n=0 to 3')
plt.legend()
plt.grid(True)
plt.show()
