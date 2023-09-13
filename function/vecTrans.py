# Coordinate Transformation for Vectors

import numpy as np


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

def S2S(S2, S1t, S1p):
    cost = np.cos(S1t)
    sint = np.sin(S1t)
    cosp = np.cos(S1p)
    
    # Rotation matrix
    T = np.array([
        [cost, -sint, 0],
        [sint, cost, 0],
        [0, 0, cosp]
    ])
    
    # Perform the coordinate transformation
    S1 = np.dot(T, S2)
    
    return S1

def VecTrans(vini, solidangle, type):
    # Solid Angle to Polar Angle and Azimuthal Angle
    (theta, phi) = (solidangle[0], solidangle[1])
    
    # Calculating cos(theta) and sin(theta)
    if theta == 0:
        sint = 0
        cost = 1
    elif theta == np.pi:
        sint = 0
        cost = -1
    elif theta == np.pi/2 or theta == 3*np.pi/2:
        cost = 0
        sint = 1
    else:
        cost = np.cos(theta)
        sint = np.sin(theta)
    
    # Calculating cos(phi) and sin(phi)
    if phi == 0:
        sinp = 0
        cosp = 1
    elif phi == np.pi/2:
        cosp = 0
        sinp = 1
    else:
        cosp = np.cos(phi)
        sinp = np.sin(phi)
    
    # Transform Matrix
    T = np.array([[sint * cosp, cost * cosp, -sinp],
                  [sint * sinp, cost * sinp, cosp],
                  [cost, -sint, 0]
                  ])
    print(np.array([[sint * cosp, cost * cosp, -sinp],
                  [sint * sinp, cost * sinp, cosp],
                  [cost, -sint, 0]
                  ]))
    # Assigning the Type of Transformation
    if type == 'C2S':
        T = np.transpose(T)
    elif type != 'S2C':
        print('Error from function "VecTrans"')
    
    #vfin = np.dot(T, vini)
    vfin = T @ vini
    return vfin

vinicart = np.array([[1],
                     [0],
                     [0]
                     ])
print('This is C2S')
print(C2S(np.array([[1],
                    [0],
                    [0]])))
print('=================')

DPosSph = np.array([1., np.pi / 2, 0.])

print(VecTrans(vinicart, DPosSph[1:3], 'C2S'))
# print(DPosSph[1:3])
# print(DPosSph[1:3][0], DPosSph[1:3][1], DPosSph[2])
# print(np.array([[sint * cosp, cost * cosp, -sinp],
                  #[sint * sinp, cost * sinp, cosp],
                  #[cost, -sint, 0]
                  #]))

