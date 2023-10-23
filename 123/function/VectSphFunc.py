## Array of Normalized Vector Spherical Functions (M and N)
# Input  : 
#    kr        |float|                         --- dimensionless Radial variable, k_i * r = (n_i * k_0) * r
#    nmax      |int.|                          --- maximum expansion order of function
#    Rad       |dict.|                         --- result of Spherical Bessel function, radial functions
#    NAng      |dict.|                         --- result of NormTauPiP, angular functions
#    emphi     |array|                         --- array of e^(i*m*phi)
# Output : 
#    VSF       |dict.|                         --- value of M and N
#        ['M'] |n-by-2n+1-by-3 complex array|  --- basis function of Mie theory
#        ['N'] |n-by-2n+1-by-3 complex array|  --- basis function of Mie theory

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
    '''
    Array of Normalized Vector Spherical Functions (M and N)
    Input  : 
        kr        |float|                         --- dimensionless Radial variable, k_i * r = (n_i * k_0) * r
        nmax      |int.|                          --- maximum expansion order of function
        Rad       |dict.|                         --- result of Spherical Bessel function, radial functions
        NAng      |dict.|                         --- result of NormTauPiP, angular functions
        emphi     |array|                         --- array of e^(i*m*phi)
    Output : 
        VSF       |dict.|                         --- value of M and N
            ['M'] |n-by-2n+1-by-3 complex array|  --- basis function of Mie theory
            ['N'] |n-by-2n+1-by-3 complex array|  --- basis function of Mie theory
    '''
    #Rad   = SphBessel.Rad(kr, nmax, array, type)
    #NAng  = NormTauPiP.NAng(nmax, theta, order)
    #sio.savemat('./VectSphFunc_Rad.mat', mdict=Rad)
    #print("VSF emphi : ")
    #print(emphi)
    
    # Preallocation
    VSF = {
        'M' : np.zeros((nmax, 2*nmax + 1, 3), dtype=np.complex128),
        'N' : np.zeros((nmax, 2*nmax + 1, 3), dtype=np.complex128)
    }
    
    # Extract Radial Functions
    if   'h1' in Rad:
        z1 = Rad['h1']
    elif 'j1' in Rad:
        z1 = Rad['j1']
    
    #z1 = z1.reshape(-1, 1)
    
    if   'raddxi'  in Rad:
        raddz = Rad['raddxi']
    elif 'raddpsi' in Rad:
        raddz = Rad['raddpsi']
        
    #raddz = raddz.reshape(-1, 1)
    
    # Construct the Array of Each Order
    n = np.arange(1, nmax + 1)
    #n = n.reshape(-1, 1)

    #print("VSF n.shape : ")
    #print(n)
    #print(n.shape)
    
    # Construct Radz (j_n(kr)/kr)
    if kr == 0:
        Radz    = np.zeros((nmax, ), dtype=np.complex128)
        Radz[0] = 1/3
    else:
        Radz    = z1 / kr
    
    #print("VSF z1 : ")
    #print(z1.shape)
    #print("VSF Radz : ")
    #print(Radz.shape)
    #print("VSF raddz : ")
    #print(raddz.shape)
    #print("VSF NAng['NPi'] : ")
    #print(NAng['NPi'].shape)
    #print("VSF n : ")
    #print(n.shape)
    
    # M Field
    VSF['M'][:, :, 1] = 1j * np.einsum('i,ij->ij', z1, NAng['NPi']) * emphi
    VSF['M'][:, :, 2] = -np.einsum('i,ij->ij', z1, NAng['NTau']) * emphi
    
    #VSF['M'][:, :, 1] = 1j * z1 * NAng['NPi'] * emphi
    #VSF['M'][:, :, 2] = -z1 * NAng['NTau'] * emphi
    
    
    # N Field
    VSF['N'][:, :, 0] = np.einsum('i,ij->ij', Radz*n*(n+1), NAng['NP']) * emphi
    VSF['N'][:, :, 1] = np.einsum('i,ij->ij', raddz, NAng['NTau']) * emphi
    VSF['N'][:, :, 2] = 1j * np.einsum('i,ij->ij', raddz, NAng['NPi']) * emphi
    
    #VSF['N'][:, :, 0] = Radz*n*(n+1) * NAng['NP'] * emphi
    #VSF['N'][:, :, 1] = raddz * NAng['NTau'] * emphi
    #VSF['N'][:, :, 2] = 1j * raddz * NAng['NPi'] * emphi
    
    #sio.savemat('./VectSphFunc.mat', mdict=VSF)
    return VSF

#kr    = 1
#nmax  = 1
#Rad   = {'j1': ([0.30116868]), 'psi': ([0.30116868+0.j]), 'dpsi': ([0.54030231+0.j]), 'raddpsi': ([0.54030231+0.j])}
#NAng  = {'NPi': ([[-0.61237244,  0.        , -0.61237244]]), 'NTau': ([[ 0.33086624, -0.72873525, -0.33086624]]), 'NP': ([[ 0.51529364,  0.46791552, -0.51529364]])}
#emphi = np.sqrt(1/ (2 * np.pi))
#print(VectSphFunc(kr, nmax, Rad, NAng, emphi))