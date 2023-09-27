import numpy as np
import scipy.io as sio


def Wigner_d(j, theta):
    # Calculation of J+
    m = np.arange(-j, j)
    J = np.diag(np.sqrt((j - m) * (j + m + 1)), k=-1)
    
    # Create the Spectral Decomposition Matrix J_y at z Representation
    Jy = (J - J.T) / (2j)
    
    # Diagonalization
    D, V = np.linalg.eig(Jy)
    
    # Unitary Transformation
    d = V @ np.diag(np.exp(-1j * theta *D)) @ V.conj().T
    
    # Check the Quality of the Transformation
    #np.max() will just output a number instead of column or row vector
    if np.max(np.abs(np.imag(d))) > 1e-12:
        warn_mes = 'Wigner_d may not give reliable results.'
        print(warn_mes)
    
    # Change Data Type (complex -> real)
    dd= np.real(d)
    
    return dd


def NormTauPiP(nmax, theta, order):
    # Preallocation
    NTau = np.zeros((nmax, 2 * nmax + 1))
    NPi = np.zeros((nmax, 2 * nmax + 1))
    NP = np.zeros((nmax, 2 * nmax + 1))
    
    for indn in range(1, nmax + 1):
        # Calling Wigner d Matrix of Order n
        dn = Wigner_d(indn, theta)
        
        # Setting the Order
        if order == 'normal':
            # d_(m,+1)^n
            dnp1 = dn[:, indn + 1]
            # d_(m,0)^n
            dn01 = dn[:, indn ]
            # d_(m,-1)^n
            dnn1 = dn[:, indn - 1]
        elif order == 'reversed':
            # d_(m,+1)^n
            dnp1 = np.flip(dn[:, indn + 1])
            # d_(m,0)^n
            dn01 = np.flip(dn[:, indn ])
            # d_(m,-1)^n
            dnn1 = np.flip(dn[:, indn - 1])
        
        # Normalization Constants
        NormTauPi = np.sqrt((2 * indn + 1) / 8)
        NormP = np.sqrt((2 * indn + 1) / (2 * indn * (indn + 1)))
        
        # Output Functions
        NPi[indn - 1, :2 * indn + 1] = -NormTauPi * (dnp1 + dnn1)
        NTau[indn - 1, :2 * indn + 1] = -NormTauPi * (dnp1 - dnn1)
        NP[indn - 1, :2 * indn + 1] = NormP * dn01
    
    # Correction to the Floating Numbers
    NPi[np.abs(NPi) < 1e-15] = 0
    NTau[np.abs(NTau) < 1e-15] = 0
    NP[np.abs(NP) < 1e-15] = 0
    
    # Output a Dictionary
    NAng = {'NPi': NPi, 'NTau': NTau, 'NP': NP}
    # wrap the result in .mat
    #sio.savemat('./NormTauPiP.mat', mdict=NAng)
    return NAng

print(NormTauPiP(1, 1, 'normal'))

# wrap the result in .mat
