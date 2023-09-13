import numpy as np

def SingleGR0(Settings):
    # Variables
    nmax = Settings['nmax']
    rhoD = Settings['nr'][0] * Settings['k0'] * Settings['DPos']['Sph'][0]
    
    # Radial Functions for Donor
    if 'DRad' not in Settings:
        Settings['DRad'] = SphBessel(rhoD, nmax, 1, 'hankel1')
    
    # Angular Functions
    if 'DNAng' not in Settings:
        Settings['DNAng'] = NormTauPiP(nmax, Settings['DPos']['Sph'][1], 'reversed')
    
    if 'DNAngN' not in Settings:
        Settings['DNAngN'] = NormTauPiP(nmax, Settings['DPos']['Sph'][1], 'normal')
    
    # Mie Coefficients
    if 'Source' not in Settings:
        Settings['Source'] = SourCoeff(Settings, "Green's function only")
    
    if 'Layer0' not in Settings:
        if Settings['BC'] == 'sphere':
            Settings['Layer0'] = MieSingle(Settings['nr'], Settings['k0s'], nmax)
        elif Settings['BC'] == 'coreshell':
            Settings['Layer0'] = MieCoreShell(Settings['nr'], Settings['k0s'], nmax)
        
        Settings['Layer0']['a'] = Settings['Source']['p'] * np.transpose(Settings['Layer0']['alpha'])
        Settings['Layer0']['b'] = Settings['Source']['q'] * np.transpose(Settings['Layer0']['beta'])
    
    # Azimuthal Functions
    if 'emphi' not in Settings:
        emphi = np.sqrt(1 / (2 * np.pi))
    
    # Generating M and N Fields
    Temp = {}
    Temp['DVSF'] = VectSphFunc(rhoD, nmax, Settings['DRad'], Settings['DNAngN'], emphi)
    
    # Summing All orders of the Scattering Field
    Temp['Layer0M'] = np.reshape(np.sum(Temp['DVSF']['M'] * Settings['Layer0']['b'], axis=(0, 1)), (3, 1))
    Temp['Layer0N'] = np.reshape(np.sum(Temp['DVSF']['N'] * Settings['Layer0']['a'], axis=(0, 1)), (3, 1))
    
    # Scattering Part at the Donor Position
    Output = {}
    Output['EScat'] = Temp['Layer0M'] + Temp['Layer0N']
    
    # DOri.ImG.Dori
    Output['ImG'] = Settings['k0'] / 6 / np.pi + np.imag(np.transpose(Output['EScat']) * Settings['DOri']['Sph'])
    
    # Purcell Factor
    Output['Purcell'] = 6 * np.pi / Settings['k0'] * Output['ImG']
    
    return Output
