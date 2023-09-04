import numpy as np
import math 

#give the value of coordinate 
S1t = 0
S1p = 0
S2 = np.array([
    [0],
    [0],
    [0]
     ])

#define the trigonometry 
cost = math.cos(S1t)
sint = math.sin(S1t)
cosp = math.cos(S1p)

print(cost, sint, cosp)

#define the transformation matrix
T = np.array([
    [cost, -sint, 0],
    [sint,  cost, 0],
    [0     , 0      , cosp]
])
print(T)

#translate coordinate of S2 to S1
S1 = np.dot(T,S2)

print(S1)


#define a function input S2,S1t,S1p output S1
def S2S(S2, S1t, S1p):
    return S1

print(S2S(S2, S1t, S1p))
