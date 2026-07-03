import numpy as np
import scipy.io as sio
from SphBessel   import SphBessel
from NormTauPiP  import NormTauPiP
from Settings1 import Settings



def VectSphFunc_for_benchmark(kr, nmax):

    #Rad   = SphBessel.Rad(kr, nmax, array, type)
    #NAng  = NormTauPiP.NAng(nmax, theta, order)
    # Preallocation
    VSF_M = np.zeros((nmax, 2 * nmax + 1, 3), dtype=np.complex128)
    VSF_N = np.zeros((nmax, 2 * nmax + 1, 3), dtype=np.complex128)
    
    # NAng
    theta = np.pi/4 # parameter
    order = 'normal' #p arameter
    NAng  = NormTauPiP(nmax, theta, order)
 
    # Rad
    array = 1 # parameter
    type  = 'bessel' # parameter
    Rad   = SphBessel(kr, nmax, array, type)
    
    #emphi
    # Preallocation
    m = -np.inf * np.ones((nmax, 2 * nmax + 1), dtype=int)
    
    # Generate Azimuthal Function
    for ii in range(1, nmax + 1):
        m[ii - 1, 0:2 * ii + 1] = np.arange(ii, -ii - 1, -1)
    
    if Settings['DPos']['Sph'][2] == 0:
        # For Speed-Up
        emphi = np.sqrt(1 / (2 * np.pi))
    else:
        m_exp = np.exp(1j * m * Settings['DPos']['Sph'][2])
        
        emphi = np.sqrt(1 / (2 * np.pi)) * m_exp
        emphi[np.isnan(emphi)] = 0
    
    #print(emphi)
    
    # Extract Radial Functions
    if   'h1' in Rad:
        z1 = Rad['h1']
    elif 'j1' in Rad:
        z1 = Rad['j1']
    
    z1 = z1.reshape(1, 70)
    #print(z1.shape)
    #print((z1.reshape(1, 70)).shape)
    
    if   'raddxi'  in Rad:
        raddz = Rad['raddxi']
    elif 'raddpsi' in Rad:
        raddz = Rad['raddpsi']
        
    raddz = raddz.reshape(1, 70)
    #print(raddz.shape)
    
    # Construct the Array of Each Order
    n = np.arange(1, nmax + 1).T
    n = n.reshape(70, 1)
    #print(n.shape)
    
    # Construct Radz (j_n(kr)/kr)
    if kr == 0:
        Radz = np.zeros(nmax, 1)
        Radz[0] = 1/3
    else:
        Radz = z1.T / kr
    
    #print(Radz.shape)
    #print((Radz.T).shape)
    #A = NAng['NP']
    #print(A.shape)
    # M Field
    VSF_M[:, :, 1] = 1j * z1.T * NAng['NPi'] * emphi
    VSF_M[:, :, 2] = -z1.T * NAng['NTau'] * emphi
    
    # N Field
    VSF_N[:, :, 0] = Radz * (n * (n + 1)) * (NAng['NP'] * emphi)
    VSF_N[:, :, 1] = raddz.T * NAng['NTau'] * emphi
    VSF_N[:, :, 2] = 1j * np.transpose(raddz) * NAng['NPi'] * emphi
    
    VSF = {'M': VSF_M, 'N': VSF_N}
    #print(VSF_M.shape)
    #print(VSF_N.shape)
    filename = f'./benchmark_of_VectSphFunc.mat'
    sio.savemat(filename, mdict={'VSFpy': VSF, 'NAngpy': NAng, 'Radpy': Rad})
    print(f'VSFpy saved to {filename}')
    return #VSF

print(VectSphFunc_for_benchmark(1.6755, 70))
