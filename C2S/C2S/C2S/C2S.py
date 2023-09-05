#To transfer the rcartesian to rspherical coordinate
import numpy as np
import math as m

#Define the value of Cartesian coordinate

(x,y,z) = (4, 3, 6)


rcart = np.array([
    [x],[y],[z]
    ])
print(rcart)

#Radius
r = m.sqrt(x**2 + y**2 + z**2)

#Polar angle
theta = m.acos(z / r)
#Undefined value at r = (0,x,x)
if np.logical_not(np.any(r, axis = 0)):
    theta = 0


#Azimuth angle 
phi = m.atan(y / x)
#Undefined value at x = 0 amd y = 0
if np.logical_and(np.logical_not(np.any(y, axis = 0)), np.logical_not(np.any(x, axis = 0))):
    phi = 0
#Undefined value as x < 0
elif  np.logical_and(x < 0, np.any(y, axis = 0)):
    phi = pi

rsph = np.array([
    [r], [theta], [phi]
    ])


def C2S(rcart):
    return rsph

print(C2S(rcart))

