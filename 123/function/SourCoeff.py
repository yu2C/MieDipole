## Mie Coefficient for A Dipole Source (cgs unit)
# Inputs  : Settings --- calculation parameter
#            .nmax   --- maximun expansion order
#            .nr     --- relative refractive index
#            .k0     --- modulus of wavevector in vacuum
#            .DPos   --- donor position
#            .Sph    --- presented in a spherical coordinate
#           Rad      --- set of radial functions
#            .h1     --- spherical bessel functions
#            .raddxi --- dxi/kr
#           NAng     --- normalized Tau, Pi, and P functions
#            .NTau   --- normalized Tau array
#            .NPi    --- normalized Pi array
#            .NP     --- normalized P array
# Outputs : Source   --- source expansion coefficients
#            .p      --- coefficient p
#            .q      --- coefficient q

#import Settings1
import numpy as np
#import pandas as pd
#import Inputfile as i
from SphBessel import SphBessel
#import NormTauPiP
from VectSphFunc import VectSphFunc
from TenCont import TenCont

#Settings = {
 #   "nmax"	     : 30,
  #  "nr"         : 1,
   # "k0"         : 1.551403779550515e+07,
   # "k0s"        : 1.551403779550515e+07 * 70e-8 ,
#    "DPos"	     : {
#        "Cart"   : np.array([[0],
#                             [0],
#                             [80e-9]
#                             ]),
#        "Sph"    : np.array([[8.e-08],
#                             [0.e+00],
#                             [0.e+00]])
#    },
#}


#kr    = 1
#nmax  = 1
#array = 1
#type  = 'bessel'
#theta = 0
#order = 'reversed'
#Rad   = SphBessel.SphBessel(Settings1.Settings1['k0s'], Settings1.Settings1['nmax'], array = 1, type = 'hankel')
#NAng  = NormTauPiP.NormTauPiP(Settings1.Settings1['nmax'], theta, order)
#print(Rad)
#print(NAng)

def SourCoeff(Settings, type):
    # Variables
    nmax = Settings['nmax']
    
    # Define the refractive index where the source is located to "ni"
    if Settings['BC'] == 'simplecavity':
        ni = Settings['nr'][1]
    else:
        ni = Settings['nr'][0]
    
    kr = ni * Settings['k0'] * Settings['DPos']['Sph'][0]
    
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
        m_exp[np.isnan(m_exp)] = 0
        emphi = np.sqrt(1 / (2 * np.pi)) * m_exp
    
    # Generate N and M Functions
    kr  = ni * Settings['k0'] * Settings['DPos']['Sph'][0]
    
    VSF = VectSphFunc(kr, nmax, Settings['DRad'], Settings['DNAng'], emphi)
    
    # Calculate Prefactor
    if type == "Green's function only":
        prefactor = 1j * (ni * Settings['k0']) * (-1) ** m
    elif type == 'dipole':
        # Prefactor from the Green's Function and a Dipole (Gaussian Unit)
        prefactor = 4 * np.pi * 1j * (ni * Settings['k0']) ** 3 * (-1) ** m
    
    # Output
    Source = {}
    if Settings['BC'] == 'simplecavity':
        Source['r'] = prefactor * TenCont(VSF['N'], Settings['DOri']['Sph'], [2, 0])
        Source['s'] = prefactor * TenCont(VSF['M'], Settings['DOri']['Sph'], [2, 0])
    else:
        Source['p'] = prefactor * TenCont(VSF['N'], Settings['DOri']['Sph'], [2, 0])
        Source['q'] = prefactor * TenCont(VSF['M'], Settings['DOri']['Sph'], [2, 0])
    
    return Source


#from Settings1 import Settings
#print(Settings)
#print(SourCoeff(Settings, type="Green's function only"))
