import numpy as np
import C2S
from Demo_WavelengthMode_CF_PCRET  import Settings
import csv
import scipy.io as sio
import json
import os

'''
json_file = ('./123/function/Demo_WavelengthMode_CF_PCRET.json')

with open(json_file) as json_data:
        data = json.load(json_data)
        
print(type(data))
print(data)
print(data["Settings"]["ModeName"])
print(type(data["tmp_set"]["epsi0"]))

print(os.getcwd())     

A = np.zeros((1, 2))
print(A)
'''

'''
import numpy as np
import matplotlib.pyplot as plt

# Generate x values from 0 to 100
x = np.arange(0, 101)  # Values from 0 to 100

# Calculate y based on the given formula
#y = np.sqrt((2 * x + 1) / 8)
y = np.sqrt((2 * x + 1) / (2 * x * (x + 1)))

# Plot x and y
plt.plot(x, y)
plt.xlabel('indn')
plt.ylabel('sqrt((2 * indn + 1) / 8)')
plt.title('Plot of sqrt((2 * indn + 1) / 8) vs. indn')
plt.xlim(0, 100)
#plt.ylim(0, 5.5)
plt.grid(True)
plt.show()
'''

'''
A = np.array([1, 2])
B = np.array([[1, 2]])
print(A[0])
print(B[0])
'''

A = np.zeros((2, 5, 3))
print(A)
A[:, :, 1] = 1
print(A)