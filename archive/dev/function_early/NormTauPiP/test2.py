import numpy as np
from scipy.special import factorial as f
from scipy.special import lpmv, lpmn
from scipy.misc import derivative as d

def P_mn(theta):
    return lpmv(1, 1, theta)


def NormTauPiP(nmax, theta):
    # Preallocation
    NTau = np.zeros((nmax, 2 * nmax + 1))
    NPi = np.zeros((nmax, 2 * nmax + 1))
    NP = np.zeros((nmax, 2 * nmax + 1))
    
    indn = nmax
    
    for m in range(0, indn + 1): 
        for T in range(theta, theta + 1, 1): 
            #print(type(m))      
            print(indn, m)
            #P_mn, dP_mn = lpmn(m, indn, np.cos(0))
            #print(P_mn, dP_mn)
    
            # Normalization Constants
            NormPTauPi = np.sqrt( ((2 * indn + 1) * f(indn - abs(m))) / (2 * indn * (indn + 1) * f(indn + abs(m))))
        
            # Output Functions
            #P_mn, dP_mn = lpmn(m, indn, theta)
            #Pm_mn = lpmv(m, indn, theta)
            dP_mn = d(P_mn, theta, dx = 0.1)
            
            #print(P_mn, dP_mn, Pm_mn)
            
            NPi = NormPTauPi * m * P_mn(theta) / np.sin(theta)
            NTau = NormPTauPi * dP_mn
            NP = NormPTauPi * P_mn(theta)
            # Output a Dictionary
            print('NPi')
            print(NPi)
            print('NTau')
            print(NTau)
            print('NP')
            print(NP)
    
    return 0

print(NormTauPiP(1, 1))





