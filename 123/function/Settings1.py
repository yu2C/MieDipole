import numpy as np
import scipy.io as sio


Settings1 = {
    "ModeName"   : "wavelength",
    "Quantity"   : "CF",

    "nr"         : np.array([1,	1.349872708298668 + 0.990253984899622j], dtype=np.complex128),
    "k0"         : 2.094395102393195e+07,
    "k0s"        : np.array([1.256637061435917]) ,
    "DPos"	     : {
        "Cart"   : np.array([[0],
                             [0],
                             [80e-9]
                             ]),
        "Sph"    : np.array([[8.e-08],
                             [0.e+00],
                             [0.e+00]]),
    },
    "APos"	     : {
        "Cart"   : np.array([[0],
                             [0],
                             [80e-9]]),
    },
    "DOri"	     : {
        "Cart"   : np.array([[0],
                             [0],
                             [1]]),
    },
    "AOri"	     : {
        "Cart"   : np.array([[0],
                             [0],
                             [1]]),
        
    },
    "nmax"	     : 70,
    "BC"         : "sphere",
    "rbc"		 : 60e-9,
    "Dpstrength" : 1,    
}

#sio.savemat('./Settings1.mat', mdict=Settings1)

#print(Settings1["APos"])
#print(Settings1["DRad"])
#print(Settings1["nmax"])
import numpy as np
from C2S import C2S
from VecTrans import VecTrans
from NormTauPiP import NormTauPiP
from SphBessel import SphBessel

# Transforming Coordinate
Settings1['DPos']['Sph'] = C2S(Settings1['DPos']['Cart'])
Settings1['DOri']['Sph'] = VecTrans(Settings1['DOri']['Cart'], Settings1['DPos']['Sph'][1:3], 'C2S')

    # Times of the 'for loop'
Settings1['nn'] = Settings1['nr'].shape[0]

# Coordinate Transformation
Settings1['APos']['Sph']  = C2S(Settings1['APos']['Cart'])
Settings1['AOri']['Sph']  = VecTrans(Settings1['AOri']['Cart'], Settings1['APos']['Sph'][1:3], 'C2S')
Settings1['APos']['Sph2'] = C2S(Settings1['APos']['Cart'] - Settings1['DPos']['Cart'])

# Angular Functions
Settings1['DNAng'] = NormTauPiP(Settings1['nmax'], Settings1['DPos']['Sph'][1], 'reversed')
Settings1['ANAng'] = NormTauPiP(Settings1['nmax'], Settings1['APos']['Sph'][1], 'normal')

# Radial Functions
rhoD = Settings1['nr'][0] * Settings1['k0'] * Settings1['DPos']['Sph'][0]
Settings1['DRad'] = SphBessel(rhoD, Settings1['nmax'], 1, 'hankel1') 


Settings = Settings1 
#print(Settings)
#print(Settings['DRad'])
#print(rhoD)
filename = f'./Settings_VSF.mat'
sio.savemat(filename, mdict={'Settings': Settings})
print(f'Settings_VSF saved to {filename}')