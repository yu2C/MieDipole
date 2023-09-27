## Mie Coefficients for A Single Sphere
# Inputs  :  
#   nr       -> double (1-by-2): Relative refractive index %
#   ks       -> double         : Dimensionless boundary (k* sphere_radius ) %
#   n        -> double         : expansion order %
# Outputs : 
#   Coeffs   -> struct array   : Mie coefficients %
#    . alpha -> double (1-by-n): Mie coefficient alpha %
#    . beta  -> double (1-by-n): Mie coefficient beta %
#    . gamma -> double (1-by-n): Mie coefficient gamma %
#    . delta -> double (1-by-n): Mie coefficient delta %
# Calling functions : SphBessel


import numpy as np
from SphBessel import SphBessel
#import Settings1

def MieSingle(nr, ks, nmax):
    try:
        if len(nr) != 2 or len(ks) != 1:
            raise ValueError("Error input size of 'nr' or 'ks' from 'MieSingle'")
    except TypeError:
        print("Error: 'ks' should be a list or array with one element.")
        return None
    
    n0, n1 = nr
    n0kr1, n1kr1 = n0 * ks[0], n1 * ks[0]
    
    n0Rad = SphBessel(n0kr1, nmax, 1, 'bessel')
    n0psi, n0dpsi = n0Rad['psi'], n0Rad['dpsi']
    
    n0Rad = SphBessel(n0kr1, nmax, 1, 'hankel1')
    n0xi, n0dxi = n0Rad['xi'], n0Rad['dxi']
    
    n1Rad = SphBessel(n1kr1, nmax, 1, 'bessel')
    n1psi, n1dpsi = n1Rad['psi'], n1Rad['dpsi']
    
    alpha = -(n1 * n0dpsi * n1psi - n0 * n0psi * n1dpsi) / (n1 * n0dxi * n1psi - n0 * n0xi * n1dpsi)
    beta = - (n0 * n0dpsi * n1psi - n1 * n0psi * n1dpsi) / (n0 * n0dxi * n1psi - n1 * n0xi * n1dpsi)
    gamma = n1 * (n0dpsi * n0xi - n0psi * n0dxi) / (n1 * n1dpsi * n0xi - n0 * n1psi * n0dxi)
    delta = n1 * (n0dpsi * n0xi - n0psi * n0dxi) / (n0 * n1dpsi * n0xi - n1 * n1psi * n0dxi)
    
    Coeffs = {
        'alpha': alpha,
        'beta' : beta,
        'gamma': gamma,
        'delta': delta
    }
    
    return Coeffs

'''
#nr   = np.array([1,	0.0506194160110720 + 2.17040801055408j], dtype=np.complex128)
nr   = Settings1.Settings1["nr"]
ks   = Settings1.Settings1["k0s"]
nmax = Settings1.Settings1["nmax"]
'''
#print(MieSingle(nr, ks, nmax))
'''
from Settings1 import Settings
print(MieSingle(Settings['nr'], Settings['k0s'], Settings['nmax']))
'''