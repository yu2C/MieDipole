import numpy as np
import C2S
from Demo_WavelengthMode_CF_PCRET  import Settings
import csv
import scipy.io as sio



#C:\Users\a0909\OneDrive\桌面\123\function\Ag_JPCL.csv
#function\Ag_JPCL.csv

C = Settings["DPos"]
#print(C)
if Settings['BC'] == 'simplecavity':
        ni = Settings['nr'][1] 
 #       print(ni)

n = 3
#A = np.ones((n, n + 1), dtype=complex)
#C = np.arctan2(1, 1j)
#B = C2S.C2S(A)
#AA = A * np.cos(1)
#AAA = np.transpose(A)

k = 1
r = 1.0

Rad1 = np.exp(1j * k * r) / r * (r**(-2) - 1j * k / r)
A = np.exp(1j * 1 * 1)
#print(A)
#print(Rad1)
#print(A[:,:,1])
#print(A[:,:,2])


theta = np.arctan2(np.sqrt(0**2 + 1**2), 1)

#print(theta)

#print(1.551403779550515e+07 * 70e-8)
'''
A = np.array([[0],
                             [0],
                             [-80e-9]])
B = np.array([[0],
                             [0],
                             [80e-9]
                             ])
C = np.array([[ 0.0e+00],
              [ 0.0e+00], 
              [-1.6e-07]
              ]) # A - B 
print(C)
print(C2S.C2S(C))
'''

A = np.array([[1.60000000e-07],
                             [3.14159265e+00],
                             [0.00000000e+00]])

B = np.array([[8.00000000e-08],
                             [3.14159265e+00],
                             [0.00000000e+00]])