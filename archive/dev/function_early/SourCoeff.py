import numpy as np

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
    kr = ni * Settings['k0'] * Settings['DPos']['Sph'][0]
    
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
        Source['r'] = prefactor * TenCont(VSF['N'], Settings['DOri']['Sph'], [3, 1])
        Source['s'] = prefactor * TenCont(VSF['M'], Settings['DOri']['Sph'], [3, 1])
    else:
        Source['p'] = prefactor * TenCont(VSF['N'], Settings['DOri']['Sph'], [3, 1])
        Source['q'] = prefactor * TenCont(VSF['M'], Settings['DOri']['Sph'], [3, 1])
    
    return Source
