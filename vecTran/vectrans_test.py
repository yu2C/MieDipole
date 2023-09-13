# Coordinate Transformation for Vectors

import numpy as np
import C2S as C2S

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
    
    print('This is theta, phi')
    print(theta, phi)
    
    # Transform Matrix
    T = np.array([[sint * cosp, cost * cosp, -sinp],
                  [sint * sinp, cost * sinp, cosp],
                  [cost, -sint, 0]
                  ])
    
    print('This is T')
    print(np.array([[sint * cosp, cost * cosp, -sinp],
                  [sint * sinp, cost * sinp, cosp],
                  [cost, -sint, 0]
                  ]))
    
    # Assigning the Type of Transformation
    if type == 'C2S':
        T = np.transpose(T)
    elif type != 'S2C':
        print('Error from function "VecTrans"')
    
    vfin = np.dot(T, vini)
    return vfin

vinicart = np.array([[1],
                     [0],
                     [0]
                     ])
#DPosSph = np.array([1., 1.57079633, 0.])
DPosSph = C2S.C2S(vinicart)

print(C2S.C2S(vinicart))

print(VecTrans(vinicart, DPosSph[1:3], 'C2S'))
