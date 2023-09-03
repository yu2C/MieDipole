import numpy as np
import math 

T = np.array([
    [cos(t), -sin(t), 0],
    [sin(t),  cos(t), 0],
    [0     , 0      , cos(p)]
])
print(T)
S1 = T * S2


#define a function input S2,S1t,S1p output S1
def S2S(S2, S1t, S1p):
    return S1
