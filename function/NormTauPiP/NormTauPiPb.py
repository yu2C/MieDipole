import numpy as np
from scipy.special import factorial as f
from scipy.special import lpmv, lpmn
#print(lpmn(0, 1, 0))
#print(lpmv(0, 1, 0))

def NormTauPiP(nmax, theta):
    # Preallocation
    NTau = np.zeros((nmax, 2 * nmax + 1))
    NPi = np.zeros((nmax, 2 * nmax + 1))
    NP = np.zeros((nmax, 2 * nmax + 1))
     
    for indn in range(1, nmax + 1):
        m = np.arange(-indn, indn + 1, 1)        
        
        # Normalization Constants
        NormPTauPi = np.sqrt( ((2 * indn + 1) * f(indn - abs(m))) / (2 * indn * (indn + 1) * f(indn + abs(m))))
        
        # Output Functions
        P_mn, dP_mn = lpmn(m, indn, np.cos(theta))
        
        NPi[indn - 1, :2 * indn + 1] = NormTauPi * m * P_mn / np.sin(theta)
        NTau[indn - 1, :2 * indn + 1] = NormTauPi * dP_mn
        NP[indn - 1, :2 * indn + 1] = NormPTauPi * P_mn
    
    # Correction to the Floating Numbers
    NPi[np.abs(NPi) < 1e-15] = 0
    NTau[np.abs(NTau) < 1e-15] = 0
    NP[np.abs(NP) < 1e-15] = 0
    
    # Output a Dictionary
    NAng = {'NPi': NPi, 'NTau': NTau, 'NP': NP}
    
    return NAng

print(NormTauPiP(1, 0))