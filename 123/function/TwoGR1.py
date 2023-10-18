import numpy as np
#from Settings1 import Settings  # Assuming Settings1 is the module containing the Settings dictionary
from NormTauPiP  import NormTauPiP
from SourCoeff   import SourCoeff
from MieSingle   import MieSingle
from VectSphFunc import VectSphFunc
from SphBessel   import SphBessel
from C2S         import C2S
from S2S         import S2S
from EdipField   import EdipField

def TwoGR1(Settings):
    # Preallocation
    Temp = {}
    Output = {}
    nmax = Settings['nmax']

    if Settings['BC'] == 'simplecavity':
        rhoD = Settings['nr'][1] * Settings['k0'] * Settings['DPos']['Sph'][0]
    else:
        rhoD = Settings['nr'][0] * Settings['k0'] * Settings['DPos']['Sph'][0]

    rhoA = Settings['nr'][1] * Settings['k0'] * Settings['APos']['Sph'][0]

    # Radial Functions
    #if 'DRad' not in Settings:
    if Settings['BC'] == 'simplecavity':
        Settings['DRad'] = SphBessel(rhoD, nmax, 1, 'bessel')
    else:
        Settings['DRad'] = SphBessel(rhoD, nmax, 1, 'hankel1')

    #if 'ARad' not in Settings:
    Settings['ARad'] = SphBessel(rhoA, nmax, 1, 'bessel')
    #elif 'j1' not in Settings['ARad']:
    #Settings['ARad'] = SphBessel(rhoA, nmax, 1, 'bessel')

    # Angular Functions
    if 'DNAng' not in Settings:
        Settings['DNAng'] = NormTauPiP(nmax, Settings['DPos']['Sph'][1], 'reversed')

    if 'ANAng' not in Settings:
        Settings['ANAng'] = NormTauPiP(nmax, Settings['APos']['Sph'][1], 'normal')

    # Azimuthal Functions
    #if 'emphi' not in Settings:
    if Settings['APos']['Sph'][2] == 0:
        # For Speed-Up
        emphi = np.sqrt(1 / (2 * np.pi))
    else:
        # Setting exp(-inf) = 0 for Useless Array Elements
        m = -np.inf * np.ones((nmax, 2 * nmax + 1))
        for ii in range(1, nmax + 1):
            m[ii - 1, :2 * ii + 1] = -ii + np.arange(2 * ii + 1)

        emphi = np.sqrt(1 / (2 * np.pi)) * np.exp(1j * m * Settings['APos']['Sph'][2])
        # Change exp(-inf) = NaN to Zero
        emphi[np.isnan(emphi)] = 0

    # Mie Coefficients
    #if 'Source' not in Settings:
    Settings['Source'] = SourCoeff(Settings, "Green's function only")

    #if 'layer1' not in Settings:
    if Settings['BC'] == 'sphere':
        Settings['Layer1'] = MieSingle(Settings['nr'], Settings['k0s'], nmax)
        Settings['Layer1']['d'] = Settings['Source']['p'] * ((Settings['Layer1']['delta']).reshape(-1, 1))
        Settings['Layer1']['c'] = Settings['Source']['q'] * ((Settings['Layer1']['gamma']).reshape(-1, 1))
        # elif Settings['BC'] == 'simplecavity':
        #     Settings['Layer1'] = 'error' #MieSimCav(Settings['nr'], Settings['k0s'], nmax)
        #     Settings['Layer1']['d'] = Settings['Source']['r'] * np.transpose(Settings['Layer1']['delta'])
        #     Settings['Layer1']['c'] = Settings['Source']['s'] * np.transpose(Settings['Layer1']['gamma'])
        # elif Settings['BC'] == 'coreshell':
        #     # Alert of the Unsupported Function
        #     #Output['error1'] = "EFieldR1 for coreshell structures is not supported yet."
        #     Settings['Layer1']['gamma'] = 0
        #     Settings['Layer1']['delta'] = 0
        #     Settings['Layer1']['d'] = Settings['Source']['p'] * np.transpose(Settings['Layer1']['delta'])
        #     Settings['Layer1']['c'] = Settings['Source']['q'] * np.transpose(Settings['Layer1']['gamma'])

    # Generating M and N Fields
    Temp['AVSF'] = VectSphFunc(rhoA, nmax, Settings['ARad'], Settings['ANAng'], emphi)

    # Donor Dipole Field
    if Settings['BC'] == 'simplecavity':
        #if 'EdipS2' not in Settings:
        if 'Sph2' not in Settings['APos']:
            Settings['APos']['Sph2'] = C2S(Settings['APos']['Cart'] - Settings['DPos']['Cart'])

        # Field in the Secondary Coordinate
        Settings['EdipS2'] = EdipField(Settings['nr'][1], Settings['k0'], Settings['APos']['Sph2'], Settings['DOri']['Cart'])

        # Transforming to the Primary Coordinate
        Settings['EdipS1'] = S2S(Settings['EdipS2'], (Settings['APos']['Sph2'][1] - Settings['APos']['Sph'][1]), 0)
    else:
        Settings['EdipS1'] = np.array([[0], [0], [0]])

    # Summing All Order of the Field in Layer 1
    Temp['layer1M'] = (np.einsum('ijk,ij->k', Temp['AVSF']['M'], Settings['Layer1']['c'])).reshape((3, 1), order='F')
    Temp['layer1N'] = (np.einsum('ijk,ij->k', Temp['AVSF']['N'], Settings['Layer1']['d'])).reshape((3, 1), order='F')
    
    # Two-Points Green's Function (G.Dori, 1/m)
    Output['G'] = Temp['layer1M'] + Temp['layer1N'] + Settings['EdipS1'] / (4 * np.pi * (Settings['nr'][1] * Settings['k0']) ** 2)

    # Total Electric Field at the Acceptor Position (dipole moment = 1)
    Output['Etot'] = 4 * np.pi * (Settings['nr'][1] * Settings['k0']) ** 2 * Output['G']

    # Total Electric Field at the Acceptor Position (SI)
    epsilon0 = 8.854187817e-12
    Output['EtotSI'] = Settings['Dpstrength'] * (Settings['nr'][1] * Settings['k0']) ** 2 / epsilon0 * Output['G']

    # Total intensity at the Acceptor position
    Output['Int'] = np.linalg.norm(Output['Etot']) ** 2

    # Dipole field
    Output['Edip'] = Settings['EdipS1']

    # Etot / Edip
    #Output['NEtot'] = Output['Etot'] / Settings['EdipS1']
    Output['NEtot'] = np.divide(Output['Etot'], Settings['EdipS1'], where=Settings['EdipS1']!=0)

    return Output

#print(TwoGR1(Settings))

