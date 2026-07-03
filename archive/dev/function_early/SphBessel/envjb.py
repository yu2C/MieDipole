import numpy as np
from scipy.special import spherical_jn as jn 
import matplotlib.pyplot as plt

def a(n, z):  
    result = - np.log10(jn(n, z))
    return result
#print(jv(v, z), a)

# Define the range of z values
z_values = np.arange(1, 15, 0.0001)

# Define the values of n for which to plot lines
n_values_to_plot = [1, 2, 3]  # Add nmax if needed

# Create a plot for each n value
for n in n_values_to_plot:
    a_values = [a(n, z) for z in z_values]
    plt.plot(z_values, a_values, label=f'n={n}')

# Customize the plot
plt.xlabel('z')
plt.ylabel('a(n, z)')
plt.title('Plot of a(n, z) for different n values')
plt.grid(True)
plt.legend()
plt.show()