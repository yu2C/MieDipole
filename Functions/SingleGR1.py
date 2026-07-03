## Single-Point Green's Function in Region 1
# Input  : 
#    Settings           |dict.|                      --- dictionary
# !      ['nmax']       |int.|                       --- maximum expansion order
# !      ['nr']         |1-by-p complex array|*      --- relative refractive index
# !      ['k0']         |float|                      --- angular wavenumber in vacuum
# !      ['k0s']        |float|                      --- k_0 * rbc (radius of boundary)
# !      ['BC']         |string|                     --- boundary condition
# !      ['DPos']       |dict.|                      --- donor position
# !          ['Sph']    |3-by-1 array|               --- in spherical coord.
# !          ['Cart']   |3-by-1 array|               --- in Cartesian coord.
# !      ['APos']       |dict.|                      --- acceptor position
# !          ['Sph']    |3-by-1 array|               --- in spherical coord.
# !          ['Sph2']   |3-by-1 array|               --- in S2 coord.
# !          ['Cart']   |3-by-1 array|               --- in Cartesian coord.
# !      ['DOri']       |dict.|                      --- orientation of the donor dipole
# !          ['Cart']   |3-by-1 array|               --- in Cartesian coord.
#        ['DRad']       |dict.|                      --- donor radial func.
#            ['h1']     |1-by-n complex array|       --- spherical Bessel func.
#            ['raddxi'] |1-by-n complex array|       --- dxi/kr
#        ['DNAng']      |dict.|                      --- donor normalized Tau, Pi, and P
#            ['NTau']   |n-by-(2n+1) complex array|  --- normalized Tau 
#            ['NPi']    |n-by-(2n+1) complex array|  --- normalized Pi 
#            ['NP']     |n-by-(2n+1) complex array|  --- normalized P 
#        ['emphi']      |n-by-(2n+1) complex array|  --- normalized azimuthal func.
#        ['Source']     |dict.|                      --- source expansion coefficients
#            ['r']      |n-by-(2n+1) complex array|  --- coefficient r
#            ['s']      |n-by-(2n+1) array|          --- coefficient s
#        ['Layer0']     |dict.|                      --- Mie coefficients
#            ['delta']  |1-by-n complex array|       --- Mie coefficient delta
#            ['gamma']  |1-by-n complex array|       --- Mie coefficient gamma
# Output : 
#    Output             |dict.|                      --- storage of output data
#        ['Escat']      |3-by-1 complex array|       --- scattering part at DPos
#        ['ImG']        |float|                      --- donor imaginary green's function 
#        ['Purcell']    |float|                      --- Purcell factor at DPos
# Temporary data :
#    Temp               |dict.|                      --- storage of temporary data
#        ['DVSF']       |dict.|                      --- donor vector spherical func.
#            ['M']      |n-by-(2n+1) complex array|  --- donor vector spherical func. M
#            ['N']      |n-by-(2n+1) complex array|  --- donor vector spherical func. N
#        ['Layer0M']    |3-by-1 array|               --- M scattering contribution
#        ['Layer0N']    |3-by-1 complex array|       --- N scattering contribution
# Calling functions : 
#    NormTauPiP
#    SourCoeff
#    MieSingle
#    VectSphFunc
#    SphBessel
# ---------------------------------------------------------------------------------------------
# ! : necessary parameters
# * : p = 2 (single sphere), p = 3 (core/shell sphere)
import numpy as np
from NormTauPiP  import NormTauPiP
from SourCoeff   import SourCoeff
from MieSingle   import MieSingle
from VectSphFunc import VectSphFunc
from SphBessel   import SphBessel
#from Settings1   import Settings

def SingleGR1(Settings):
    Temp = {}
    Output = {}
    nmax = Settings['nmax']
    rhoD = Settings['nr'][1] * Settings['k0'] * Settings['DPos']['Sph'][0]

    # Radial Functions for Donor (need to be computed at each freq.)
    #if 'DRad' not in Settings:
    Settings['DRad'] = SphBessel(rhoD, nmax, 1, 'bessel')

    # Angular Functions (not need to be computed at each freq.)
    if 'DNAng' not in Settings:
        Settings['DNAng'] = NormTauPiP(nmax, Settings['DPos']['Sph'][1], 'reversed')

    if 'DNAngN' not in Settings:
        Settings['DNAngN'] = NormTauPiP(nmax, Settings['DPos']['Sph'][1], 'normal')

    # Azimuthal Functions (not need to be computed at each freq.)
    if 'emphi' not in Settings:
        emphi = np.sqrt(1/(2*np.pi))

    # Source Coefficients (need to be computed at each freq.)
    #if 'Source' not in Settings:
    Settings['Source'] = SourCoeff(Settings, "Green's function only")
    
    # Mie Coefficients (need to be computed at each freq.)
    #if 'Layer1' not in Settings:
    if Settings['BC'] == 'sphere':
        Settings['Layer1'] = MieSingle(Settings['nr'], Settings['k0s'], nmax)
    elif Settings['BC'] == 'coreshell':
        Settings['Layer1'] = "error" #MieCoreShell(Settings['nr'], Settings['k0s'], nmax)
    elif Settings['BC'] == 'simplecavity':
        Settings['Layer1'] = "error" #MieSimCav(Settings['nr'], Settings['k0s'], nmax)
        
    #print(Settings['Source']['r'].shape)
    #print(Settings['Source']['s'].shape)
    #print(Settings['Layer1']['delta'].shape)
    #print(Settings['Layer1']['gamma'].shape)

    Settings['Layer1']['d'] = Settings['Source']['r'] * (Settings['Layer1']['delta'].reshape(-1, 1))
    Settings['Layer1']['c'] = Settings['Source']['s'] * (Settings['Layer1']['gamma'].reshape(-1, 1))

    # Generating M and N Fields
    Temp['DVSF'] = VectSphFunc(rhoD, nmax, Settings['DRad'], Settings['DNAngN'], emphi)

    # Summing All order of the Scattering Field
    Temp['Layer0M'] = (np.einsum('ijk,ij->k', Temp['DVSF']['M'], Settings['Layer1']['c'])).reshape((3, 1), order='F')
    Temp['Layer0N'] = (np.einsum('ijk,ij->k', Temp['DVSF']['N'], Settings['Layer1']['d'])).reshape((3, 1), order='F')

    # Scattering Part at the Donor Position
    Output['EScat'] = Temp['Layer0M'] + Temp['Layer0N']

    # DOri.ImG.Dori
    Output['ImG'] = Settings['k0'] / 6 / np.pi + np.imag((Output['EScat']).T * Settings['DOri']['Sph'])

    # Purcell Factor
    Output['Purcell'] = 6 * np.pi / Settings['k0'] * Output['ImG']

   
    return Output

#print(SingleGR1(Settings))