import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def C2S(rcart):
    # Assigning the Cartesian Components
    x = rcart[0, :]
    y = rcart[1, :]
    z = rcart[2, :]
    
    # Radial Distance
    r = np.sqrt(x**2 + y**2 + z**2)
    
    # Polar Angle
    theta = np.arccos(z / r)
    
    # Assigning Polar Angle when r = 0
    theta[np.logical_not(np.any(r, axis=0))] = 0
    
    # Azimuthal Angle
    phi = np.arctan2(y, x)
    
    # Assigning Azimuthal Angle when x = 0 and y = 0
    phi[np.logical_and(np.logical_not(np.any(y, axis=0)), np.logical_not(np.any(x, axis=0)))] = 0
    
    # Assigning Azimuthal Angle when x < 0
    phi[np.logical_and(x < 0, np.any(y, axis=0))] = np.pi
    
    # Column Form
    rsph = np.vstack((r, theta, phi))
    
    return rsph

# Sample input Cartesian coordinates
input_points = np.array([[1, 0, 1],
                         [1, 0, 0],
                         [1, 0, 0]
                         ])

# Convert Cartesian to Spherical coordinates
rsph = C2S(input_points)

# Create a 3D scatter plot in Cartesian coordinates
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(input_points[:, 0], input_points[:, 1], input_points[:, 2], c='b', marker='o', label='Cartesian Points')

# Overlay vectors for Spherical coordinates
for i in range(len(rsph[0])):
    r, theta, phi = rsph[:, i]
    x, y, z = r * np.sin(theta) * np.cos(phi), r * np.sin(theta) * np.sin(phi), r * np.cos(theta)
    ax.quiver(0, 0, 0, x, y, z, color='r', label='Spherical Vectors')

# Set a fixed axis range (adjust as needed)
ax.set_xlim([0, 2])
ax.set_ylim([0, 2])
ax.set_zlim([0, 2])

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()

plt.show()
print(C2S(input_points))
