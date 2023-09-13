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

def sbesselc(z, n):
    a0 = abs(z)
    nm = n
    
    # If circle checked
    if a0 < 1e-60:
        csj = np.zeros(n + 1)
        csy = np.full(n + 1, -1e300)
        csy[0] = 1.0
        return csj, csy
    
    # checked
    csj = np.zeros(n + 1)
    csj[0] = np.sin(z) / z
    csj[1] = (csj[0] - np.cos(z)) / z
    
    if n >= 2:
        csa = csj[0]
        csb = csj[1]
        m = MSTA1(a0, 200)

        if m < n:
            nm = m
        else:
            m = MSTA2(a0, n, 15)
        
        cf0 = 0.0
        cf1 = 1.0 - 100
        
        for k in range(m, -1, -1):
            j = k + 1
            cf = (2.0 * k + 3.0) * cf1 / z - cf0
            
            if k <= nm:
                csj[j - 1] = cf
            
            cf0 = cf1
            cf1 = cf
        
        if abs(csa) > abs(csb):
            cs = csa / cf
        else:
            cs = csb / cf0
        
        for k in range(min(nm, n) + 1):
            j = k + 1
            csj[j - 1] = cs * csj[j - 1]
    
    csy = np.full(n + 1, 1e200)
    csy[0] = -np.cos(z) / z
    csy[1] = (csy[0] - np.sin(z)) / z
    
    # This is test j --> j - 1
    for k in range(2, min(nm, n) + 1):
        j = k + 1
        
        if abs(csj[j - 2]) >= abs(csj[j - 3]):
            csy[j - 1] = (csj[j - 1] * csy[j - 2] - 1.0 / z ** 2) / csj[j - 2]
        else:
            csy[j - 1] = (csj[j - 1] * csy[j - 3] - (2.0 * k - 1.0) / z ** 3) / csj[j - 3]
    
    return csj, csy

print(sbesselc(1, 2))