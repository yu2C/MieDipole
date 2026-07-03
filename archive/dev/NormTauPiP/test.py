import numpy as np
from scipy.special import factorial as f
from scipy.special import lpmv, lpmn

def NormTauPiP(nmax, theta):
    # Preallocation
    NTau = np.zeros((nmax, 2 * nmax + 1))
    NPi = np.zeros((nmax, 2 * nmax + 1))
    NP = np.zeros((nmax, 2 * nmax + 1))
    
    for indn in range(1, nmax + 1):
        for m in range(0, indn + 1): 
            for T in range(theta, theta + 1, 1): 
                #print(type(m))      
                print(indn, m)
            #P_mn, dP_mn = lpmn(m, indn, np.cos(0))
            #print(P_mn, dP_mn)
        
            # Normalization Constants
            NormPTauPi = np.sqrt( ((2 * indn + 1) * f(indn - abs(m))) / (2 * indn * (indn + 1) * f(indn + abs(m))))
        
            # Output Functions
            P_mn, dP_mn = lpmn(m, indn, np.cos(theta))
            
            NPi = NormPTauPi * m * P_mn / np.sin(theta)
            NTau = NormPTauPi * dP_mn
            NP = NormPTauPi * P_mn
            # Output a Dictionary
            NAng = {'NPi': NPi, 'NTau': NTau, 'NP': NP}
            print(NAng)
    
    return NAng

print(NormTauPiP(1, 1))