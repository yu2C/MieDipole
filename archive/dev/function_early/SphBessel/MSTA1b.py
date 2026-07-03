## Sub-Functions of Spherical Bessel/Riccati-Bessel Functions
# Ref: Computation of Special Functions (1996)
#        Authors: Shanjie Zhang, Jianming Jin
#----------------------------------------------
# Called by sbesselc and rcbesselc

# Determine the starting point M to calculate Bessel function by backward recurrence
# Input  : z     --- Argument of Jn(z)
#          mp    --- Value of magnitude
# Output : MSTA1 --- Starting point
import numpy as np 
import matplotlib.pyplot as plt

def envj(n, z):
    n = max(1, abs(n))
    result = 0.5 * np.log10(6.28 * n) - n * np.log10(1.36 * z / n)
    return result

def MSTA1(z, mp):
    a0 = abs(z)
    n0 = int(1.1 * a0) + 1
    f0 = envj(n0, a0) - mp
    n1 = n0 + 5
    f1 = envj(n1, a0) - mp
    
    for _ in range(20):
        nn = n1 - (n1 - n0) / (1.0 - f0 / f1)
        nn = int(nn)  # Convert nn to an integer (nn should not be int.)
        f  = envj(nn, a0) - mp
        
        if abs(nn - n1) < 1:
            break
        
        n0 = n1
        f0 = f1
        n1 = nn
        f1 = f
    
    return nn

print(MSTA1(1, 200))
# Define z values ranging from 1 to 10
z_values = np.linspace(-2-2j, 0, 5, endpoint=False)

# Fixed mp value
mp = 200

# Calculate MSTA1(z, mp) values for each z
MSTA1_values = [MSTA1(z, mp) for z in z_values]

# Create the plot
plt.plot(z_values, MSTA1_values)
plt.xlabel('z')
plt.ylabel('MSTA1(z, mp)')
plt.title('MSTA1(z, mp) for mp=200')

#plt.xlim(1,10)
#plt.ylim(100,180)

plt.grid(True)
plt.show()