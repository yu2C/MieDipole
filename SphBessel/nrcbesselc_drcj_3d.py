## Riccati-Bessel Functions (Complex Argument)
# Ref: Computation of Special Functions (1996)
#        Authors: Shanjie Zhang, Jianming Jin
#----------------------------------------------
# Called by SphBessel
# Compute Riccati-Bessel functions of the first and second kinds and their derivatives
# Input  : z       --- complex argument of Riccati-Bessel Fucntion
#          n       --- order of jn(z) (n = 0, 1, 2,...)
# Output : rcj(n)  --- x * jn(z)
#          drcj(n) --- (x * jn(z))'
#          rcy(n)  --- x * yn(z)
#          drcy(n) --- (x * yn(z))'
#          

import numpy as np

def MSTA1(z, mp):
    a0 = abs(z)
    n0 = int(1.1 * a0) + 1
    f0 = envj(n0, a0) - mp
    n1 = n0 + 5
    f1 = envj(n1, a0) - mp
    
    for _ in range(20):
        nn = n1 - (n1 - n0) / (1.0 - f0 / f1)
        nn = int(nn)
        f = envj(nn, a0) - mp
        
        if abs(nn - n1) < 1:
            break
        
        n0 = n1
        f0 = f1
        n1 = nn
        f1 = f
    
    return nn

def MSTA2(z, n, mp):
    a0 = abs(z)
    hmp = 0.5 * mp
    ejn = envj(n, a0)
    
    if ejn <= hmp:
        obj = mp
        n0 = int(1.1 * a0)
    else:
        obj = hmp + ejn
        n0 = n
    
    f0 = envj(n0, a0) - obj
    n1 = n0 + 5
    f1 = envj(n1, a0) - obj
    
    for _ in range(20):
        nn = n1 - (n1 - n0) / (1.0 - f0 / f1)
        nn = int(nn)
        f = envj(nn, a0) - obj
        
        if abs(nn - n1) < 1:
            break
        
        n0 = n1
        f0 = f1
        n1 = nn
        f1 = f
    
    return nn + 10

def envj(n, z):
    n = max(1, abs(n))
    result = 0.5 * np.log10(6.28 * n) - n * np.log10(1.36 * z / n)
    return result




def rcbesselc(z, n):
    rcj  = np.zeros(n + 1, dtype=complex)
    rcy  = np.zeros(n + 1, dtype=complex)
    drcj = np.zeros(n + 1, dtype=complex)
    drcy = np.zeros(n + 1, dtype=complex)
    NM   = n
    NMy  = 0
    
    if abs(z) < 1e-60: # Treat z = 0 as a special case
        print('ricatti-bessel function precision down')
        drcj[0] = 1.0 # zeroth order
        rcy     = -1.0e300 * np.ones(n + 1)
        drcy    = 1.0e300 * np.ones(n + 1)
        rcy[0]  = -1.0
        drcy[0] = 0.0
    else:
        rcj[0] = np.sin(z)  # zeroth order
        rcy[0] = -np.cos(z)
        rcj[1] = rcj[0] / z - np.cos(z)  # first order
        rcy[1] = rcy[0] / z - np.sin(z)
        rcj0   = rcj[0]
        rcj1   = rcj[1]
        RF0    = rcy[0]
        RF1    = rcy[1]
        
        for Ky in range(3, n + 2):
            RF2 = (2.0 * (Ky - 1) - 1.0) * RF1 / z - RF0
            
            if abs(RF2) > 1.0e300:
                continue
            
            rcy[Ky - 1] = RF2
            RF0 = RF1
            RF1 = RF2
            NMy = Ky - 1
            
        
        
    
    
        drcy[0] = np.sin(z)
        drcy[1] = -rcy[1] / z + rcy[0]
        
        for Ky in range(3, NMy + 2):
            drcy[Ky - 1] = -(Ky - 1) * rcy[Ky - 1] / z + rcy[Ky - 2]
        
        if n >= 2:
            M = MSTA1(z, 200)
            
            if M < n:
                NM = M
            else:
                M = MSTA2(z, n, 15)
            
            F0 = 0.0
            F1 = 1.0e-100
            
            for K in range(M + 1, 0, -1):
                F = (2.0 * (K - 1) + 3.0) * F1 / z - F0
                
                if K <= NM + 1:
                    rcj[K - 1] = F
                
                F0 = F1
                F1 = F
            
            if abs(rcj0) > abs(rcj1):
                CS = rcj0 / F
            else:
                CS = rcj1 / F0
            
            for K in range(1, NM + 2):
                rcj[K - 1] = CS * rcj[K - 1]
        
        drcj[0] = np.cos(z)
        #drcj[1] = -rcj[1] / z + rcj0
        
        for K in range(2, NM + 2): # 3, NM + 2
            drcj[K - 1] = -(K - 1) * rcj[K - 1] / z + rcj[K - 2]
    
    return rcj, rcy, drcj, drcy

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# Define the range for z (real and imaginary parts)
real_parts = np.linspace(-2, 2, 100)
imaginary_parts = np.linspace(-2, 2, 100)
real_mesh, imag_mesh = np.meshgrid(real_parts, imaginary_parts)
z_values = real_mesh + 1j * imag_mesh

# Initialize an array to store drcj values
drcj_values = np.zeros_like(z_values, dtype=complex)

# Calculate drcj for z = -2-2i to +2+2i and n = 2
n = 2
for i in range(z_values.size):
    _, _, drcj, _ = rcbesselc(z_values.flat[i], n)
    drcj_values.flat[i] = drcj[n]

# Reshape the results to match the grid
drcj_values = drcj_values.reshape(real_mesh.shape)

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(real_mesh, imag_mesh, np.real(drcj_values), cmap=cm.viridis)
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)  # Add a colorbar

ax.set_xlabel('Real part of z')
ax.set_ylabel('Imaginary part of z')
ax.set_zlabel('Real part of drcj')
ax.set_title('3D Plot of drcj for z = -2-2i to +2+2i (n = 2)')
plt.xlim(-2, +2)
plt.ylim(-2, +2)

plt.show()
