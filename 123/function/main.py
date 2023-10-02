import numpy as np
import sys
import json
from Settings1 import Settings
from ReadSettings_v1 import ReadSettings
from SingleGR0_v1 import SingleGR0
from datetime import datetime
from C2S import C2S
from VecTrans import VecTrans
from NormTauPiP import NormTauPiP
from SphBessel import SphBessel

###########################################################################
## Start the Program

# set the temperary path
sys.path.append('./Functions/')

# File to be calculated
FilePath = './123/function/'#'./InputFiles/'  # Folder Path of Input Files
FileName = 'Demo_WavelengthMode_CF_PCRET'  # File Name

# Output Figure Size (value = 0~1)
Resize = 0.5
############################################################################
############################################################################
## Loading the Input File

# Load JSON input file
Inputfile = ReadSettings(f'{FilePath}{FileName}.json')

Settings = Inputfile['Settings']
#print(Settings)
#fplot = Inputfile['fplot']

if Settings['ModeName'] == 'wavelength':
    k0 = Settings['k0']
    k0s = Settings['k0s']
    lambda_val = Settings['lambda']
    nr = Settings['nr']
elif Settings['ModeName'] == 'angle':
    Ar = Settings['APos']['Sph'][0][0]
    Atheta = Settings['APos']['Sph'][1]
    Aphi = Settings['APos']['Sph'][2][0]
    Ax = Settings['APos']['Cart'][0]
    Ay = Settings['APos']['Cart'][1]
    Az = Settings['APos']['Cart'][2]

# information of inputfile
start_time = datetime.now()
print('Beginning the program...')
# information of mode
print("Using Mode:", Settings["ModeName"])
# information of structure
print("Using Structure:", Settings["BC"])
############################################################################
############################################################################
## Check the input is correct

############################################################################
############################################################################
## Pre-Processing

# Transforming Coordinate
Settings['DPos']['Sph'] = C2S(Settings['DPos']['Cart'])
Settings['DOri']['Sph'] = VecTrans(Settings['DOri']['Cart'], Settings['DPos']['Sph'][1:3], 'C2S')

    # Times of the 'for loop'
Settings['nn'] = Settings['nr'].shape[0]

# Coordinate Transformation
Settings['APos']['Sph']  = C2S(Settings['APos']['Cart'])
Settings['AOri']['Sph']  = VecTrans(Settings['AOri']['Cart'], Settings['APos']['Sph'][1:3], 'C2S')
Settings['APos']['Sph2'] = C2S(Settings['APos']['Cart'] - Settings['DPos']['Cart'])

# Angular Functions
Settings['DNAng'] = NormTauPiP(Settings['nmax'], Settings['DPos']['Sph'][1], 'reversed')
Settings['ANAng'] = NormTauPiP(Settings['nmax'], Settings['APos']['Sph'][1], 'normal')

# Radial Functions
#rhoD = Settings['nr'][0] * Settings['k0'] * Settings['DPos']['Sph'][0]
#Settings['DRad'] = SphBessel(rhoD, Settings['nmax'], 1, 'hankel1') 

############################################################################
############################################################################
## Preallocation
if Settings['ModeName'] == 'wavelength':
    EScat = np.zeros((Settings['nn'], 3))
    ImG = np.zeros(Settings['nn'])
    if not np.array_equal(Settings['APos']['Cart'], Settings['DPos']['Cart']):
        ImG_vec = np.zeros((Settings['nn'], 3))
    Purcell = np.zeros(Settings['nn'])
else:
    Etot = np.zeros((Settings['nn'], 3))
    NormEtot = np.zeros((Settings['nn'], 3))
    Edip = np.zeros((Settings['nn'], 3))

#print(Settings)
############################################################################
############################################################################
## Main Loop
if Settings['ModeName'] == 'wavelength':
    for ii in range(Settings['nn']):
        Settings['k0'] = k0[ii]
        Settings['nr'] = nr[ii, :]
        Settings['k0s'] = k0s[ii]
        #print(Settings['nr'])

        # Determine which function is called by the acceptor position
        if np.array_equal(Settings['APos']['Cart'], Settings['DPos']['Cart']):
            if Settings['BC'] == 'simplecavity':
                Output = "error" #SingleGR1(Settings)
            else:
                Output = SingleGR0(Settings)

            EScat[ii, :] = Output['EScat'].T
            ImG[ii] = Output['ImG'].T
            Purcell[ii] = Output['Purcell'].T
        else:
            if Settings['APos']['Sph'][0] >= Settings['rbc'][0]:
                Output = "error" #TwoGR0(Settings)
            else:
                Output = "error" #TwoGR1(Settings)

            ImG_vec[ii, :] = np.imag(Output['G']).T
            Etot[ii, :] = Output['Etot'].T
            Edip[ii, :] = Output['Edip'].T
            NormEtot[ii, :] = Output['NEtot'].T

        # Information
        print(f'Progress: {((ii + 1) / Settings["nn"]) * 100:.2f}%')

# Continue with the rest of the code
