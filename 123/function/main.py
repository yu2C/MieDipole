import numpy as np
import scipy.io as sio
import sys
import json
#from Settings1 import Settings
from ReadSettings_v1 import ReadSettings
from SingleGR0_v1    import SingleGR0
from datetime        import datetime
from C2S             import C2S
from VecTrans        import VecTrans
from NormTauPiP      import NormTauPiP
from SphBessel       import SphBessel
from TwoGR0          import TwoGR0
from TwoGR1          import TwoGR1

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
#print("Settings['nr']")
#print(Settings['nr'])
#fplot = Inputfile['fplot']

if Settings['ModeName'] == 'wavelength':
    k0  = Settings['k0']
    k0  = np.array(k0)
    k0s = Settings['k0s']
    k0s = np.array(k0s)
    lambda_val = Settings['lambda']
    nr  = Settings['nr']
    nr  = np.array(nr)
    #print(Settings['k0s'])
    #print(k0s)
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

if Settings['BC'] == 'simplecavity':
    if np.linalg.norm(Settings['DPos']['Cart']) >= Settings['rbc']:
        raise ValueError('Error: The donor dipole should be inside the cavity.')
        
elif Settings['BC'] == 'sphere':
    if np.linalg.norm(Settings['DPos']['Cart']) <= Settings['rbc']:
        raise ValueError('Error: The donor dipole should be outside the sphere.')
        
elif Settings['BC'] == 'coreshell':
    if np.linalg.norm(Settings['DPos']['Cart']) <= Settings['rbc'][0]:
        raise ValueError('Error: The donor dipole should be outside the shell.')

############################################################################
############################################################################
## Pre-Processing

# Transforming Coordinate
Settings['DPos']['Sph'] = C2S(Settings['DPos']['Cart'])
Settings['DOri']['Sph'] = VecTrans(Settings['DOri']['Cart'], Settings['DPos']['Sph'][1:3], 'C2S')

# for wavelength mode
# Times of the 'for loop'
#print(Settings['nr'].shape)
Settings['nn'] = Settings['nr'].shape[0]
#print(Settings['nn'])

#print("Main Settings['nn']")
#print(Settings['nn'])
#print("Main Settings['nr']")
#print(Settings['nr'].shape)

# Coordinate Transformation
Settings['APos']['Sph']  = C2S(Settings['APos']['Cart'])
Settings['AOri']['Sph']  = VecTrans(Settings['AOri']['Cart'], Settings['APos']['Sph'][1:3], 'C2S')
Settings['APos']['Sph2'] = C2S(Settings['APos']['Cart'] - Settings['DPos']['Cart'])

# Angular Functions
Settings['DNAng'] = NormTauPiP(Settings['nmax'], Settings['DPos']['Sph'][1], 'reversed')
Settings['ANAng'] = NormTauPiP(Settings['nmax'], Settings['APos']['Sph'][1], 'normal')


#sio.savemat('./main_DNAng.mat', mdict=Settings['DNAng'])
#sio.savemat('./main_ANAng.mat', mdict=Settings['ANAng'])

# Radial Functions
#rhoD = Settings['nr'][0] * Settings['k0'] * Settings['DPos']['Sph'][0]
#Settings['DRad'] = SphBessel(rhoD, Settings['nmax'], 1, 'hankel1') 

############################################################################
############################################################################
## Preallocation
if Settings['ModeName'] == 'wavelength':
    Etot     = np.zeros((Settings['nn'], 3), dtype=np.complex128)
    NormEtot = np.zeros((Settings['nn'], 3), dtype=np.complex128)
    Edip     = np.zeros((Settings['nn'], 3), dtype=np.complex128)
    EScat    = np.zeros((Settings['nn'], 3))
    ImG      = np.zeros((Settings['nn'], 1))
    if not np.array_equal(Settings['APos']['Cart'], Settings['DPos']['Cart']):
        ImG_vec = np.zeros((Settings['nn'], 3))
    Purcell  = np.zeros((Settings['nn'], 1))
else:
    Etot     = np.zeros((Settings['nn'], 3), dtype=np.complex128)
    NormEtot = np.zeros((Settings['nn'], 3), dtype=np.complex128)
    Edip     = np.zeros((Settings['nn'], 3), dtype=np.complex128)

#print(Settings)
############################################################################
############################################################################
## Main Loop
if Settings['ModeName'] == 'wavelength':
    for ii in range(Settings['nn']):
        Settings['k0']  = k0[ii] # variable
        Settings['nr']  = np.array(nr[ii, :], dtype=np.complex128)
        #Settings['nr']  = Settings['nr'].reshape((1, 2))
        Settings['k0s'] = np.array([k0s[ii]])
        #print(Settings['nr'])
        #print("Settings['k0s']")
        #print(Settings['k0s'])
        #print("=============================")
        #print('k0')
        #print("main Settings['k0']")
        #print(Settings['k0'])
        #print("main Settings['nr']")
        #print(Settings['nr'])
        # Determine which function is called by the acceptor position
        if np.array_equal(Settings['APos']['Cart'], Settings['DPos']['Cart']):
            if Settings['BC'] == 'simplecavity':
                Output = "error" #SingleGR1(Settings)
            else:
                Output = SingleGR0(Settings)

            EScat[ii, :] = Output['EScat'].T
            ImG[ii]      = Output['ImG'].T
            Purcell[ii]  = Output['Purcell'].T
        else:
            if Settings['APos']['Sph'][0] >= Settings['rbc'][0]:
                Output = TwoGR0(Settings)
                #print('TwoGR0')
            else:
                Output = TwoGR1(Settings)
                #print('TwoGR1')

            ImG_vec[ii, :]  = (np.imag(Output['G'])).T
            Etot[ii, :]     = (Output['Etot']).T
            Edip[ii, :]     = (Output['Edip']).T
            NormEtot[ii, :] = (Output['NEtot']).T

        # Information
        #print(f'Progress: {((ii + 1) / Settings["nn"]) * 100:.2f}%')
        

# Continue with the rest of the code
if Settings['ModeName'] == 'wavelength':
    if Settings['Quantity'] == 'CF':
        # Coupling Factor
        CF = abs(Etot @ Settings['AOri']['Sph']) ** 2
        # Coupling Factor along R Direction (Vacuum)
        CFdip = abs(Edip @ Settings['AOri']['Sph']) ** 2
        # Setting 0/0 to 0 for Etot/Edip
        NormEtot[np.isnan(NormEtot)] = 0
        # Enhancement Factor
        EF = abs(NormEtot @ Settings['AOri']['Sph']) ** 2
    elif Settings['Quantity'] == 'Purcell':
        pass
    elif Settings['Quantity'] == 'ImG':
        if 'ImG_vec' in locals(): ####
            ImG = ImG_vec * Settings['AOri']['Sph']
    elif Settings['Quantity'] == 'J':
        if 'ImG_vec' in locals():
            ImG = ImG_vec * Settings['AOri']['Sph']
        c = 2.9979e8
        Debye = 3.33564e-30
        epsilon0 = 8.854187817e-12
        hbar = 1.05457182e-34
        const = ((2 * np.pi * 1239.84193 / (lambda_val * 1e9) * 2.4179893e14) ** 2
                 / c ** 2 * Debye ** 2 / (np.pi * hbar * epsilon0))
        J = const * ImG
        
        
           
import matplotlib.pyplot as plt


if Settings['ModeName'] == 'wavelength':
    if Settings['Quantity'] == 'CF':
        fplot = {}
        fplot['x'] = 1.0 / lambda_val * 1e-2
        fplot['y'] = CF * 1e-12
        MyPlot(fplot, Resize, 0)
        
        fplot['y'] = CFdip * 1e-12
        fplot['colorstyle'] = 'r-'
        MyPlot(fplot, Resize, 1)
        
        if Settings['BC'] == 'sphere':
            plt.legend(['Single Sphere', 'Vacuum (QED)'], loc='best')
        elif Settings['BC'] == 'coreshell':
            plt.legend(['Core/Shell Sphere', 'Vacuum (QED)'], loc='best')
        
        fplot['y'] = EF
        fplot['colorstyle'] = '-'
        fplot['range'] = [float('-inf'), float('inf'), 1e-3, 1e5]
        fplot['ylabel'] = 'Enhancement'
        MyPlot(fplot, Resize, 0)
        
        if Settings['BC'] == 'sphere':
            plt.legend(['Single Sphere'], loc='best')
        elif Settings['BC'] == 'coreshell':
            plt.legend(['Core/Shell Sphere'], loc='best')
    
    elif Settings['Quantity'] == 'Purcell':
        fplot['x'] = 1239.84193 / (lambda_val * 1e9)
        fplot['y'] = Purcell
        MyPlot(fplot, Resize, 0)
    
    elif Settings['Quantity'] == 'ImG':
        fplot['x'] = 1239.84193 / (lambda_val * 1e9)
        fplot['y'] = ImG
        MyPlot(fplot, Resize, 0)
    
    elif Settings['Quantity'] == 'J':
        fplot['x'] = 1239.84193 / (lambda_val * 1e9)
        fplot['y'] = J
        MyPlot(fplot, Resize, 0)


