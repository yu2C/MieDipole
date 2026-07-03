import numpy as np
from scipy.special import factorial as f
from scipy.special import lpmv, lpmn
from scipy.misc import derivative as d

# Input 
nmax = 1
m = np.arange(0, nmax + 1)
print(m)
#m = 1
theta = np.pi / 4
x = np.cos(theta)

# Normalization constant
NormPTauPi = np.sqrt( ((2 * nmax + 1) * f(nmax - abs(m))) / (2 * nmax * (nmax + 1) * f(nmax + abs(m))))
print(NormPTauPi)

# Associated Legendre Polynomials
def P_mn(x):
    return lpmv(m, nmax, x)
print(P_mn(x))

# ALP divided by theta (still wrong but others are correct !)
dP_mn = d(P_mn, theta, dx = 0.01)
print(dP_mn)

# Preallocation
NTau = np.zeros((nmax, 2 * nmax + 1))
NPi = np.zeros((nmax, 2 * nmax + 1))
NP = np.zeros((nmax, 2 * nmax + 1))

# Output Functions
NPi = NormPTauPi * m * P_mn(x) / np.sin(theta)
NTau = NormPTauPi * dP_mn
NP = NormPTauPi * P_mn(x)

# Output a Dictionary
print('NPi')
print(NPi)
print('NTau')
print(NTau)
print('NP')
print(NP)
    








