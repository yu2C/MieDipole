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

#A = np.zeros((2, 5, 3))
#print(A)
#A[:, :, 1] = 1
#print(A)

'''
import numpy as np
import matplotlib.pyplot as plt

# Define the function e^(e^(iwt))
def complex_function(n, t, w):
    z = np.exp(1j * w * t) + np.exp(-1j * w * t)
    return np.exp(n * z)

# Generate values of t
t = np.linspace(0, 10, 1000)  # Adjust the range and number of points as needed

# Set coupling strength parameter (plays a similar role of Huang-Rhys factor)
n = 1

# Set up the plot
plt.figure(figsize=(12, 6))

# Loop over a range of w values
for w in np.linspace(0, 2*np.pi, 10):  # Adjust the range and number of w values as needed
    # Calculate the function values
    result = complex_function(n, t, w)

    # Plot the real and imaginary parts
    plt.plot(t, result.real, label=f'Real part, w = {w:.2f}')
    plt.plot(t, result.imag, '--', label=f'Imaginary part, w = {w:.2f}')

# Configure plot settings
plt.xlabel('t')
plt.ylabel('Function Value')
plt.title(r'$e^{e^{iwt}}$ vs t for different w')
plt.legend(loc='upper right', fontsize='small')
plt.grid(True)

# Show the plot
plt.show()
'''
'''
A = np.ones((1, 4, 3))
B = np.ones((3, 1))
C = np.einsum('ijk, kl-> ij', A, B)
print(A.shape)
print(B.shape)
print(C.shape)
print(C)
'''
'''
import numpy as np
import matplotlib.pyplot as plt

# Given data
Peak_Position = np.array([21.1632, 42.066, 63.8906, 85.1896, 106.1475, 127.208, 148.0884, 169.3662, 190.3978, 211.8724, 233.4677, 254.3442, 275.6267])
Intensity = np.array([101, 284, 431, 498, 574, 525, 475, 381, 289, 220, 151, 95, 59])

# Fit data using a polynomial of degree 5 (chosen for demonstration; you might want to adjust this)
p = np.polyfit(Peak_Position, Intensity, 12)
print(p)
fitted_curve = np.poly1d(p)


# Plotting
plt.figure(figsize=(10, 6))
plt.plot(Peak_Position, Intensity, 'ro', label='Data Points')
plt.plot(Peak_Position, fitted_curve(Peak_Position), 'b-', label='Fitted Curve')
plt.xlabel('Peak Position (cm^-1)')
plt.ylabel('Intensity (A.U.)')
plt.title('Peak Position vs Intensity with Fitted Curve')
plt.legend()
plt.grid(True)
plt.show()
'''

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Given data
peak_positions = np.array([21.1632, 42.066, 63.8906, 85.1896, 106.1475, 127.208, 148.0884, 169.3662, 190.3978, 211.8724, 233.4677, 254.3442, 275.6267])
J_values = np.arange(len(peak_positions))

# Define the function for curve fitting
def fit_func(J, B):
    return 2 * B * J * (J + 1)

# Fit the data to the function
params, covariance = curve_fit(fit_func, J_values, peak_positions)
print(params)
B = params[0]

# Plot the data and the fit
plt.figure(figsize=(10,6))
plt.plot(J_values, peak_positions, 'ro', label='Data')
plt.plot(J_values, fit_func(J_values, B), 'b-', label=f'Fit: B={B:.4f} cm^-1')
plt.xlabel('J(J+1)')
plt.ylabel('Peak Position (cm^-1)')
plt.legend()
plt.show()

print(f"Rotational constant, B = {B:.4f} cm^-1")

"""
import numpy as np
import matplotlib.pyplot as plt

# Given data
peak_positions = np.array([21.1632, 42.066, 63.8906, 85.1896, 106.1475, 127.208, 148.0884, 169.3662, 190.3978, 211.8724, 233.4677, 254.3442, 275.6267])

# Quantum number J values
J_values = np.arange(len(peak_positions))

# Calculate x = J(J+1) values
x_values = J_values * (J_values + 1)

# Use polyfit for linear regression (degree = 1 for linear)
slope, intercept = np.polyfit(x_values, peak_positions, 1)

# The slope is equal to 2B
B = slope / 2

print(f"Rotational constant, B = {B:.4f} cm^-1")

# Plotting the results
plt.figure(figsize=(10,6))
plt.plot(x_values, peak_positions, 'ro', label='Data')
plt.plot(x_values, slope * x_values + intercept, 'b-', label=f'Linear Fit: B={B:.4f} cm^-1')
plt.xlabel('J(J+1)')
plt.ylabel('Peak Position (cm^-1)')
plt.legend()
plt.grid(True)
plt.show()
"""
'''
import numpy as np

# Given data
peak_positions = np.array([21.1632, 42.066, 63.8906, 85.1896, 106.1475, 127.208, 148.0884, 169.3662, 190.3978, 211.8724, 233.4677, 254.3442, 275.6267])

# Calculate the differences between successive peak positions
differences = np.diff(peak_positions)

# Estimate 2B by averaging the differences
average_difference = np.mean(differences)

# B is half of this average difference
B = average_difference / 2

print(f"Rotational constant, B = {B:.4f} cm^-1")
'''
