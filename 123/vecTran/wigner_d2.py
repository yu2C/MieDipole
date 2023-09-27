import numpy as np
from scipy.special import wigner_d

# Define quantum numbers
j = 1.5  # Total angular momentum quantum number
m1 = 1   # Magnetic quantum number for the initial state
m2 = -1  # Magnetic quantum number for the final state
beta = np.pi / 3  # Rotation angle in radians

# Calculate the Wigner-D matrix element
D = wigner_d(j, m1, m2, beta)

print("Wigner-D matrix element D(j={}, m1={}, m2={}, beta={}):".format(j, m1, m2, beta))
print(D)
