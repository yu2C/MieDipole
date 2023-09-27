## Array of Normalized Vector Spherical Functions (M and N)
# Input  : kr    --- Dimensionless Radial variable
#          nmax  --- maximum expansion order of function
#          Rad   --- result of Spherical Bessel function
#          NAng  --- result of NormTauPiP
#          emphi --- array of e^(i*m*phi)
# Output : VSF   --- value of M and N

import numpy as np
import scipy.io as sio
#from SphBessel import Rad
#from NormTauPiP import NAng
#from SourCoeff import emphi
#import SphBessel
#import NormTauPiP
#import SourCoeff
'''
kr    = 1
nmax  = 1
array = 1
type  = 'bessel'
theta = 1
order = 'normal'
Rad   = SphBessel.SphBessel(kr, nmax, array, type)
NAng  = NormTauPiP.NormTauPiP(nmax, theta, order)
#print(Rad)
#print(NAng)
'''

def VectSphFunc(kr, nmax, Rad, NAng, emphi):
    #Rad   = SphBessel.Rad(kr, nmax, array, type)
    #NAng  = NormTauPiP.NAng(nmax, theta, order)
    # Preallocation
    VSF_M = np.zeros((nmax, 2 * nmax + 1, 3), dtype=complex)
    VSF_N = np.zeros((nmax, 2 * nmax + 1, 3), dtype=complex)
    
    # Extract Radial Functions
    if   'h1' in Rad:
        z1 = Rad['h1']
    elif 'j1' in Rad:
        z1 = Rad['j1']
    
    if   'raddxi'  in Rad:
        raddz = Rad['raddxi']
    elif 'raddpsi' in Rad:
        raddz = Rad['raddpsi']
    
    # Construct the Array of Each Order
    n = np.arange(1, nmax + 1)
    
    # Construct Radz (j_n(kr)/kr)
    if kr == 0:
        Radz = np.zeros(nmax, 1)
        Radz[0] = 1/3
    else:
        Radz = np.transpose(z1) / kr
    
    # M Field
    VSF_M[:, :, 1] = 1j * np.transpose(z1) @ NAng['NPi'] * emphi
    VSF_M[:, :, 2] = -np.transpose(z1) @ NAng['NTau'] * emphi
    
    # N Field
    VSF_N[:, :, 0] =  n * (n + 1) * Radz @ NAng['NP'] * emphi
    VSF_N[:, :, 1] = np.transpose(raddz) @ NAng['NTau'] * emphi
    VSF_N[:, :, 2] = 1j * np.transpose(raddz) @ NAng['NPi'] * emphi
    
    VSF = {'M': VSF_M, 'N': VSF_N}
    #sio.savemat('./VectSphFunc.mat', mdict=VSF)
    return VSF

#kr    = 1
#nmax  = 1
#Rad   = {'j1': ([0.30116868]), 'psi': ([0.30116868+0.j]), 'dpsi': ([0.54030231+0.j]), 'raddpsi': ([0.54030231+0.j])}
#NAng  = {'NPi': ([[-0.61237244,  0.        , -0.61237244]]), 'NTau': ([[ 0.33086624, -0.72873525, -0.33086624]]), 'NP': ([[ 0.51529364,  0.46791552, -0.51529364]])}
#emphi = np.sqrt(1/ (2 * np.pi))
#print(VectSphFunc(kr, nmax, Rad, NAng, emphi))