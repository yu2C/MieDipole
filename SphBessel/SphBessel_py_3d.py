import numpy as np
import matplotlib.pyplot as plt


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

def sbesselc(z, n):
    a0 = abs(z)
    nm = n
    
    # If circle checked. Treat z = 0 as a special case
    if a0 < 1e-60:
        csj    = np.zeros(n + 1, dtype=complex)
        csy    = np.full(n + 1, -1e300, dtype=complex)
        csy[0] = 1.0 + 0.0j
        return csj, csy
    
    # checked. 
    csj    = np.zeros(n + 1, dtype=complex)
    csj[0] = np.sin(z) / z
    csj[1] = (csj[0] - np.cos(z)) / z
    
    if n >= 2: # Backward recurrence
        csa = csj[0]
        csb = csj[1]
        m   = MSTA1(a0, 200) 

        if m < n:
            nm = m
        else: 
            m = MSTA2(a0, n, 15)
        
        cf0 = 0.0 
        cf1 = 1.0 - 100
        
        for k in range(m, -1, -1):
            cf = (2.0 * k + 3.0) * cf1 / z - cf0
            
            if k <= nm:
                csj[k] = cf
            
            cf0 = cf1
            cf1 = cf
        
        if abs(csa) > abs(csb):
            cs = csa / cf
        else:
            cs = csb / cf0
        
        for k in range(min(nm, n) + 1):
            csj[k] = cs * csj[k]
    
    csy = np.full(n + 1, 1e200, dtype=complex)
    csy[0] = -np.cos(z) / z #y0(z) by (8.1.11)
    csy[1] = (csy[0] - np.sin(z)) / z #y1(z) by (8.1.12)
    
    for k in range(2, min(nm, n) + 1): # calculate yn(z) by W as n >= 2
        
        if abs(csj[k - 1]) > abs(csj[k - 2]): # GT. or GE.?
            csy[k] = (csj[k] * csy[k - 1] - 1.0 / z ** 2) / csj[k - 1]
        else:
            csy[k] = (csj[k] * csy[k - 2] - (2.0 * k - 1.0) / z ** 3) / csj[k - 2]
    
    return csj, csy

def rcbesselc(z, n):
    rcj  = np.zeros(n + 1, dtype=complex)
    rcy  = np.zeros(n + 1, dtype=complex)
    drcj = np.zeros(n + 1, dtype=complex)
    drcy = np.zeros(n + 1, dtype=complex)
    NM   = n
    
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
            drcj[1] = -rcj[1] / z + rcj0
            
            for K in range(3, NM + 2):
                drcj[K - 1] = -(K - 1) * rcj[K - 1] / z + rcj[K - 2]
    
    return rcj, rcy, drcj, drcy


def SphBessel(kr, nmax, array, type):
    Rad = {}

    if type == 'bessel':
        if kr == 0:
            z1 = np.zeros(nmax, dtype=complex)
            Z = np.zeros(nmax, dtype=complex)
            dZ = np.zeros(nmax, dtype=complex)
            raddZ = np.zeros(nmax, dtype=complex)
            raddZ[0] = 2/3
            if array == 0:
                z1 = z1[nmax]
                Z = Z[nmax]
                dZ = dZ[nmax]
                raddZ = raddZ[nmax]
        else:
            csj, _ = sbesselc(kr, nmax)
            if array == 1:
                z1 = csj[1:nmax+1]
            else:
                z1 = csj[nmax]
                
            rcj, _, drcj, _ = rcbesselc(kr, nmax)
            
            if array == 0:
                Z = rcj[nmax]
                dZ = drcj[nmax]
                raddZ = dZ / kr
            else:
                rcj = rcj[1:]
                drcj = drcj[1:]
                Z = rcj
                dZ = drcj
                raddZ = dZ / kr
        
        Rad['j1'] = z1
        Rad['psi'] = Z
        Rad['dpsi'] = dZ
        Rad['raddpsi'] = raddZ
    
    elif type == 'hankel1':
        if kr == 0:
            if nmax == 0:
                z1 = 1 - 1j * 1e300
                Z = -1j
                dZ = 1
            else:
                z1 = complex(0, -1e300)
                Z = complex(0, -1e300)
                dZ = 1j * 1e300
                raddZ = 0
        else:
            csj, csy = sbesselc(kr, nmax)
            
            if len(csj) < (nmax + 1) or len(csy) < (nmax + 1):
                raise ValueError('Please decrease the expansion order "n".')
            
            if array == 1:
                z1 = csj[1:nmax+1] + 1j * csy[1:nmax+1]
            else:
                z1 = csj[nmax] + 1j * csy[nmax]
            
            rcj, rcy, drcj, drcy = rcbesselc(kr, nmax)
            
            if array == 0:
                Z = rcj[nmax] + 1j * rcy[nmax]
                dZ = drcj[nmax] + 1j * drcy[nmax]
                raddZ = dZ / kr
            else:
                rcj = rcj[1:]
                rcy = rcy[1:]
                drcj = drcj[1:]
                drcy = drcy[1:]
                Z = rcj + 1j * rcy
                dZ = drcj + 1j * drcy
                raddZ = dZ / kr
                
        
        Rad['h1'] = z1
        Rad['xi'] = Z
        Rad['dxi'] = dZ
        Rad['raddxi'] = raddZ
        

    return Rad

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.colors import Normalize

# Assume the existing functions sbesselc, rcbesselc, and SphBessel are defined here

# Define the range for kr (real and imaginary parts)
kr_real_parts = np.linspace(-2, 2, 100)
kr_imaginary_parts = np.linspace(-2, 2, 100)
kr_real_mesh, kr_imag_mesh = np.meshgrid(kr_real_parts, kr_imaginary_parts)
kr_values = kr_real_mesh + 1j * kr_imag_mesh

# Initialize an array to store the real part of psi
psi_real_values = np.zeros_like(kr_values.real)

# Calculate psi for kr = -2-2i to +2+2i and nmax = 2, array = 1, type = 'bessel'
nmax = 2
array = 1
type = 'bessel'

for i in range(kr_values.size):
    kr = kr_values.flat[i]
    result = SphBessel(kr, nmax, array, type)
    psi_real_values.flat[i] = np.real(result['psi'][nmax-1])

# Reshape the results to match the grid
psi_real_values = psi_real_values.reshape(kr_real_mesh.shape)

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(kr_real_mesh, kr_imag_mesh, psi_real_values, cmap='viridis')

# Add a colorbar
norm = Normalize(vmin=psi_real_values.min(), vmax=psi_real_values.max())
sm = plt.cm.ScalarMappable(cmap='viridis', norm=norm)
sm.set_array([])
fig.colorbar(sm, ax=ax, shrink=0.5, aspect=10)

ax.set_xlabel('Real part of kr')
ax.set_ylabel('Imaginary part of kr')
ax.set_zlabel('Real part of psi')
ax.set_title('3D Plot of real part of psi for kr = -2-2i to +2+2i (nmax = 2, array = 1, type = ''bessel'')')
plt.xlim(2, -2)
plt.ylim(2, -2)
plt.show()
