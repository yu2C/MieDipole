import numpy as np

def VectSphFunc(kr, nmax, Rad, NAng, emphi):
    # Preallocation
    VSF_M = np.zeros((nmax, 2 * nmax + 1, 3), dtype=complex)
    VSF_N = np.zeros((nmax, 2 * nmax + 1, 3), dtype=complex)
    
    # Extract Radial Functions
    if 'h1' in Rad:
        z1 = Rad['h1']
    elif 'j1' in Rad:
        z1 = Rad['j1']
    
    if 'raddxi' in Rad:
        raddz = Rad['raddxi']
    elif 'raddpsi' in Rad:
        raddz = Rad['raddpsi']
    
    # Construct the Array of Each Order
    n = np.arange(1, nmax + 1)
    
    # Construct Radz (j_n(kr)/kr)
    if kr == 0:
        Radz = np.zeros(nmax)
        Radz[0] = 1/3
    else:
        Radz = np.transpose(z1) / kr
    
    # M Field
    VSF_M[:, :, 1] = 1j * np.transpose(z1) * NAng['NPi'] * emphi
    VSF_M[:, :, 2] = -np.transpose(z1) * NAng['NTau'] * emphi
    
    # N Field
    VSF_N[:, :, 0] = Radz * n * (n + 1) * NAng['NP'] * emphi
    VSF_N[:, :, 1] = np.transpose(raddz) * NAng['NTau'] * emphi
    VSF_N[:, :, 2] = 1j * np.transpose(raddz) * NAng['NPi'] * emphi
    
    VSF = {'M': VSF_M, 'N': VSF_N}
    
    return VSF
