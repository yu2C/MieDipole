# Cartesian Coordinates to Spherical Coordinates
# input (x,y,z) = (0,0,0) will cause theta diverges

import numpy as np

def C2S(rcart):
    # Assigning the Cartesian Components
    x = rcart[0, :]
    y = rcart[1, :]
    z = rcart[2, :]
    
    # Radial Distance
    r = np.sqrt(x**2 + y**2 + z**2)
    
    # Polar Angle
    #theta = np.arccos(z / r)
    # np.arctan2()
    theta = np.arctan2(np.sqrt(r**2 + z**2), z)
    
    # Assigning Polar Angle when r = 0
    #theta[np.logical_not(np.any(r, axis=0))] = 0
    
    # Azimuthal Angle
    phi = np.arctan2(y, x)
    
    # Assigning Azimuthal Angle when x = 0 and y = 0
    phi[np.logical_and(np.logical_not(np.any(y, axis=0)), np.logical_not(np.any(x, axis=0)))] = 0
    
    # Assigning Azimuthal Angle when x < 0
    phi[np.logical_and(x < 0, np.any(y, axis=0))] = np.pi
    
    # Column Form
    rsph = np.vstack((r, theta, phi))
    
    return rsph
#print(np.array([[1, 0, 0],
 #               [1, 1, 0],
  #              [1, 0, 0]]))
print(C2S(np.array([[1, 0, 0],
                    [1, 1, 0],
                    [1, 0, 0]])))