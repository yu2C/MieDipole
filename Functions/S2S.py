# Coordinate Transformation (Spherical to Spherical)
import numpy as np

def S2S(S2, S1t, S1p):
    if isinstance(S1t, (np.ndarray, list)):
        S1t = S1t[0]

    if isinstance(S1p, (np.ndarray, list)):
        S1p = S1p[0]


    cost = np.cos(S1t)
    sint = np.sin(S1t)
    cosp = np.cos(S1p)
    #print("S2S cost : ")
    #print(cost)
    #print("S2S sint : ")
    #print(sint)
    #print("S2S cosp : ")
    #print(cosp)
    # Rotation matrix
    T = np.array([
        [cost, -sint,    0],
        [sint,  cost,    0],
        [   0,     0, cosp]
        ]) 
    
    #print("S2S T : ")
    #print(T)
    # Perform the coordinate transformation
    S1 = np.dot(T, S2)
    
    return S1

#print(np.cos(3.14))
#print(S2S(np.array([[1.73205081, 1., 1.],
 #                   [0.95531662, 1.57079633, 1.57079633],
  #                  [0.78539816, 1.57079633, 0.]
   #                 ]), np.pi, 0))
#print(S2S(np.array([[1.73205081],
 #                   [0.95531662],
  #                  [0.78539816]
   #                 ]), 0, 0))
#print(S2S(np.array([[1.73205081],
 #                   [0.95531662],
  #                  [0.78539816]
   #                 ]), np.pi / 2, 0))
'''
print(S2S(np.array([[-3.56558893e+20-1.25710431e+21j],
                    [ 4.90815938e+12-1.05171161e+12j],
                    [ 0.00000000e+00+0.00000000e+00j]]), 0, 0))
'''