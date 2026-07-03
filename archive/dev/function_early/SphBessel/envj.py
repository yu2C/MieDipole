## Sub-Functions of MSTA1/MSTA2
# Ref: Computation of Special Functions (1996)
#        Authors: Shanjie Zhang, Jianming Jin
#----------------------------------------------
# Called by MSTA1 and MSTA2
# Calculate the -log(Jn(z))
# Input  : n          --- order of Jn(z)
#          z          --- absolute value of complex argument of Jn(z)
# Output : envj(n, z) --- value of -log(Jn(z))

import numpy as np
import matplotlib.pyplot as plt

def envj(n, z):
    n = max(1, abs(n))
    result = 0.5 * np.log10(6.28 * n) - n * np.log10(1.36 * z / n)
    return result

print(envj(1, 1))

# Define the range of z values
z_values = np.arange(1, 51, 0.001)

# Define the values of n for which to plot lines
n_values_to_plot = np.arange(1, 10)  # Add nmax if needed

# Create a plot for each n value
for n in n_values_to_plot:
    envj_values = [envj(n, z) for z in z_values]
    plt.plot(z_values, envj_values, label=f'n={n}')

# Customize the plot
plt.xlabel('z')
plt.ylabel('envj(n, z)')
plt.title('Plot of envj(n, z) for different n values')

plt.xlim(0, 50)
plt.ylim(-8, 10)

plt.grid(True)
plt.legend()
plt.show()