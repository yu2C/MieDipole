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
    rcj = np.zeros(n + 1, dtype=complex)
    rcy = np.zeros(n + 1, dtype=complex)
    drcj = np.zeros(n + 1, dtype=complex)
    drcy = np.zeros(n + 1, dtype=complex)
    NM = n
    Ky = 0  # Initialize Ky to a default value

    if abs(z) < 1e-60:
        print('ricatti-bessel function precision down')
        drcj[0] = 1  # zeroth order
        rcy = -1.0e300 * np.ones(n + 1)
        drcy = 1.0e300 * np.ones(n + 1)
        rcy[0] = -1.0
        drcy[0] = 0.0
    else:
        rcj[0] = np.sin(z)  # zeroth order
        rcy[0] = -np.cos(z)
        rcj[1] = rcj[0] / z - np.cos(z)  # first order
        rcy[1] = rcy[0] / z - np.sin(z)
        rcj0 = rcj[0]
        rcj1 = rcj[1]
        RF0 = rcy[0]
        RF1 = rcy[1]

        for Ky in range(2, n + 1):
            RF2 = (2.0 * (Ky - 1) - 1.0) * RF1 / z - RF0
            if abs(RF2) > 1.0e300:
                continue
            rcy[Ky] = RF2
            RF0 = RF1
            RF1 = RF2

        NMy = Ky - 1
        drcy[0] = np.sin(z)
        drcy[1] = -rcy[1] / z + rcy[0]

        for Ky in range(2, NMy + 1):
            drcy[Ky] = -(Ky - 1) * rcy[Ky] / z + rcy[Ky - 1]

        if n >= 2:
            M = MSTA1(z, 200) if MSTA1(z, 200) < n else MSTA2(z, n, 15)

            F0 = 0.0
            F1 = 1.0e-100

            for K in range(M, -1, -1):
                F = (2.0 * (K - 1) + 3.0) * F1 / z - F0

                if K <= NM + 1:
                    rcj[K - 1] = F

                F0 = F1
                F1 = F

            CS = rcj0 / F if abs(rcj0) > abs(rcj1) else rcj1 / F0

            for K in range(NM + 1):
                rcj[K] = CS * rcj[K]

        drcj[0] = np.cos(z)
        drcj[1] = -rcj[1] / z + rcj0

        for Ky in range(2, NM + 1):
            drcj[Ky] = -(Ky - 1) * rcj[Ky] / z + rcj[Ky - 1]

    return rcj, rcy, drcj, drcy

# Add MSTA1 and MSTA2 functions here if they are defined in your code.
# Also, ensure that the necessary imports are included.


n = 1 
z = 1
print(rcbesselc(z, n))
