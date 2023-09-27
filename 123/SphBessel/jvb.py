import numpy as np
from scipy.special import spherical_jn as jn
import matplotlib.pyplot as plt

#a = - np.log10(jv(n, z))

#print(jv(v, z), a)

# Define the range of z values
z_values = np.arange(0, 20, 0.01)

# Define the values of n for which to plot lines
n_values_to_plot = [0, 1, 2, 3]  # Add nmax if needed

# Create a plot for each n value
for n in n_values_to_plot:
    jn_values = [jn(n, z) for z in z_values]
    plt.plot(z_values, jn_values, label=f'n={n}')

# Customize the plot
plt.xlabel('z')
plt.ylabel('jn(n, z)')
plt.title('Plot of jn(n, z) for different n values')
plt.grid(True)
plt.legend()

# Set y-axis limits to 1.0 to -0.5
plt.ylim(-0.5, 1.0)

# Set x-axis limits to 0-15
plt.xlim(0, 20, 5)

plt.show()