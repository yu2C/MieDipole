## Mie Coefficients for A Single Sphere
# Inputs  :  
#    nr            |1-by-2 complex array| --- relative refractive index
#    ks            |1-by-1 array|         --- dimensionless boundary, k_0 * rbc (radius of boundary) #store in array because other BC will have two k0s values
#    nmax          |int.|                 --- maximum expansion order
# Outputs : 
#    Coeffs        |dict.|                --- Mie coefficients 
#        ['alpha'] |1-by-n complex array| --- Mie coefficient alpha 
#        ['beta']  |1-by-n complex array| --- Mie coefficient beta 
#        ['gamma'] |1-by-n complex array| --- Mie coefficient gamma 
#        ['delta'] |1-by-n complex array| --- Mie coefficient delta 
# Calling functions : SphBessel

import numpy    as np
import scipy.io as sio
from SphBessel import SphBessel
#import Settings1


def MieSingle(nr, ks, nmax):
    '''
    # check the inputs
    #print('Mie Single ks :')
    #print(ks)
    #print('Mie Single nr :')
    #print(nr)
    '''
    # Assuming nr and ks are numpy arrays
    if np.max(len(nr)) != 2 or np.max(len(ks)) != 1:
        errmes = 'Error input size of "nr" or "ks" from "MieSingle"'
        print(f"{errmes}")

    # Defining variables
    n0, n1 = nr
    n0kr1, n1kr1 = n0 * ks[0], n1 * ks[0]
    
    # Radial functions
    n0Rad_b = SphBessel(n0kr1, nmax, 1, 'bessel')
    n0psi, n0dpsi = n0Rad_b['psi'], n0Rad_b['dpsi']
    
    n0Rad_h = SphBessel(n0kr1, nmax, 1, 'hankel1')
    n0xi,  n0dxi  = n0Rad_h['xi'], n0Rad_h['dxi']
    
    n1Rad = SphBessel(n1kr1, nmax, 1, 'bessel')
    n1psi, n1dpsi = n1Rad['psi'], n1Rad['dpsi']
    '''
    #sio.savemat('./MieSingle_n0Rad.mat', mdict=n0Rad_b)
    #print(n0psi.shape)
    #print(n0Rad_b['psi'].shape)
    #print(n0xi.shape)
    #print(n1psi.shape)
    '''
    
    # Coefficients
    alpha = - (n1 * n0dpsi * n1psi - n0 * n0psi * n1dpsi) / (n1 * n0dxi * n1psi - n0 * n0xi * n1dpsi)
    beta  = - (n0 * n0dpsi * n1psi - n1 * n0psi * n1dpsi) / (n0 * n0dxi * n1psi - n1 * n0xi * n1dpsi)
    gamma = n1 * (n0dpsi * n0xi - n0psi * n0dxi) / (n1 * n1dpsi * n0xi - n0 * n1psi * n0dxi)
    delta = n1 * (n0dpsi * n0xi - n0psi * n0dxi) / (n0 * n1dpsi * n0xi - n1 * n1psi * n0dxi)
    
    #print(alpha.shape)
    
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
'''
nr = np.array([1.00, 1.0000])
ks = np.array([1.2566])
nmax = 70
print(MieSingle(nr, ks, nmax))
'''
'''
from Settings1 import Settings
print(MieSingle(Settings['nr'], Settings['k0s'], Settings['nmax']))
'''