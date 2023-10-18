## Two Points Green's Function
# Input  : 
#    Settings           |dict.|                          --- dictionary
# !      ['nmax']       |int.|                           --- maximum expansion order
# !      ['nr']         |1-by-p complex array|*          --- relative refractive index
# !      ['k0']         |float|                          --- angular wavenumber in vacuum
# !      ['k0s']        |1-by-1 array|                   --- k_0 * rbc (radius of boundary) #store in array because other BC will have two k0s values
# !      ['BC']         |string|                         --- boundary condition
# !      ['DPos']       |dict.|                          --- donor position
# !          ['Sph']    |3-by-1 array|                   --- in spherical coord.
# !          ['Cart']   |3-by-1 array|                   --- in Cartesian coord.
# !      ['APos']       |dict.|                          --- acceptor position
# !          ['Sph']    |3-by-1 array|                   --- in spherical coord.
#            ['Sph2']   |3-by-1 array|                   --- in S2 coord.
# !          ['Cart']   |3-by-1 array|                   --- in Cartesian coord.
# !      ['DOri']       |dict.|                          --- orientation of the donor dipole
# !          ['Cart']   |3-by-1 array|                   --- in Cartesian coord.
# !      ['Dpstrength'] |float|                          --- dipole strength
#        ['DRad']       |dict.|                          --- donor radial functions
#            ['h1']     |1-by-n complex array|           --- spherical Bessel function
#            ['raddxi'] |1-by-n complex array|           --- dxi / kr
#        ['ARad']       |dict.|                          --- acceptor radial functions
#            ['h1']     |1-by-n complex array|           --- spherical Bessel function
#            ['raddxi'] |1-by-n complex array|           --- dxi / kr
#        ['DNAng']      |dict.|                          --- donor angular functions
#            ['NTau']   |n-by-(2n+1) complex array|      --- normalized Tau 
#            ['NPi']    |n-by-(2n+1) complex array|      --- normalized Pi 
#            ['NP']     |n-by-(2n+1) complex array|      --- normalized P 
#        ['ANAng']      |dict.|                          --- acceptor angular functions
#            ['NTau']   |n-by-(2n+1) complex array|      --- normalized Tau 
#            ['NPi']    |n-by-(2n+1) complex array|      --- normalized Pi 
#            ['NP']     |n-by-(2n+1) complex array|      --- normalized P 
#        ['emphi']      |n-by-(2n+1) complex array|      --- normalized azimuthal functions
#        ['Source']     |dict.|                          --- source expansion coefficients
#            ['p']      |n-by-(2n+1) complex array|      --- coefficient p
#            ['q']      |n-by-(2n+1) complex array|      --- coefficient q
#        ['Layer0']     |dict.|                          --- Mie coefficients
#            ['alpha']  |1-by-n complex array|           --- Mie coefficient alpha
#            ['beta']   |1-by-n complex array|           --- Mie coefficient beta
# Output : 
#    Output             |dict.|                          --- storage of output data
#        ['G']          |3-by-1 complex array|           --- two-Points Green's Function (G.Dori, 1/m)
#        ['Etot']       |3-by-1 complex array|           --- total electric field at the acceptor position (dipole moment = 1)
#        ['EtotSI']     |3-by-1 complex array|           --- total electric field at the acceptor position (SI)
#        ['Int']        |float|                          --- total intensity at the acceptor position 
#        ['Edip']       |3-by-1 complex array|           --- dipole field (dipole moment = 1, Gaussian unit)
#        ['NEtot']      |3-by-1 complex array|           --- Etot / Edip
# Temporary data :
#    Temp               |dict.|                          --- storage of temporary data
#        ['AVSF']       |dict.|                          --- acceptor vector spherical functions
#            ['M']      |n-by-(2n+1)-by-3 complex array| --- acceptor vector spherical function M
#            ['N']      |n-by-(2n+1)-by-3 complex array| --- acceptor vector spherical function N
#        ['Layer0M']    |3-by-1 complex array|           --- M scattering contribution
#        ['Layer0N']    |3-by-1 complex array|           --- N scattering contribution
# Calling functions : 
#    NormTauPiP
#    SourCoeff
#    MieSingle
#    VectSphFunc
#    SphBessel
#    C2S
#    S2S
#    EdipField
# --------------------------------------------------------------------------------------------
# ! : necessary parameters
# * : p = 2 (single sphere), p = 3 (core/shell sphere)

import numpy    as np
import scipy.io as sio
#from Settings1   import Settings  # Assuming Settings1 is the module containing the Settings dictionary
from NormTauPiP  import NormTauPiP
from SourCoeff   import SourCoeff
from MieSingle   import MieSingle
from VectSphFunc import VectSphFunc
from SphBessel   import SphBessel
from C2S         import C2S
from S2S         import S2S
from EdipField   import EdipField



def TwoGR0(Settings):
    # Preallocation
    Temp = {}
    Output = {}
    nmax = Settings['nmax']
    rhoD = Settings['nr'][0] * Settings['k0'] * Settings['DPos']['Sph'][0] # float number k_i * r = (n_i * k_0) * r
    rhoA = Settings['nr'][0] * Settings['k0'] * Settings['APos']['Sph'][0] # float number k_i * r = (n_i * k_0) * r
    rhoD = rhoD[0] # convert the array to float
    rhoA = rhoA[0] # convert the array to float
    '''
    # print("TwoGR0 rhoD : ")
    # print(rhoD)
    # print("TwoGR0 rhoA : ")
    # print(rhoA)
    '''

    # Radial Functions (need to be computed at each freq.)
    #if 'DRad' not in Settings:
    Settings['DRad'] = SphBessel(rhoD, nmax, 1, 'hankel1') 

    #if 'ARad' not in Settings:
    Settings['ARad'] = SphBessel(rhoA, nmax, 1, 'hankel1') 
    '''
    #sio.savemat('./TwoGR0_DRad.mat', mdict=Settings['DRad'])
    #sio.savemat('./TwoGR0_ARad.mat', mdict=Settings['ARad'])
    '''
    
    # Angular Functions (not need to be computed at each freq.)
    if 'DNAng' not in Settings:
        Settings['DNAng'] = NormTauPiP(nmax, Settings['DPos']['Sph'][1], 'reversed') 

    if 'ANAng' not in Settings:
        Settings['ANAng'] = NormTauPiP(nmax, Settings['APos']['Sph'][1], 'normal') 
    '''
    # print(Settings['DNAng']['NPi'][0,0])
    # print(Settings['ANAng']['NPi'][0,0])    
    #sio.savemat('./TwoGR0_DNAng.mat', mdict=Settings['DNAng'])
    #sio.savemat('./TwoGR0_ANAng.mat', mdict=Settings['ANAng'])
    '''
    
    # Azimuthal Functions (need to be computed at each freq.)
    #if 'emphi' not in Settings:
    if Settings['APos']['Sph'][2] == 0:
        # Speed-Up
        emphi = np.sqrt(1/(2*np.pi))
    else: #need debug
        # Setting exp(-inf) = 0 for Useless Array Elements
        m = -np.inf * np.ones((nmax, 2*nmax+1))
        for ii in range(1, nmax + 1):
            m[ii-1, :2*ii+1] = np.arange(-ii, ii+1)

        emphi = np.sqrt(1/(2*np.pi)) * np.exp(1j * m * Settings['APos']['Sph'][2])
        # Change exp(-inf) = NaN to Zero
        emphi[np.isnan(emphi)] = 0
    '''        
    #print("TwoGR0 emphi : ")
    #print(emphi)
    '''
    
    # Source Coefficients (need to be computed at each freq.)
    #if 'Source' not in Settings:
    Settings['Source'] = SourCoeff(Settings, "Green's function only")
    '''
    #sio.savemat('./TwoGR0_Source.mat', mdict=Settings['Source'])
    '''

    # Mie Coefficients (need to be computed at each freq.)
    #if 'Layer0' not in Settings:
    if Settings['BC'] == 'sphere':
        Settings['Layer0'] = MieSingle(Settings['nr'], Settings['k0s'], nmax)
        Settings['Layer0']['a'] = Settings['Source']['p'] * ((Settings['Layer0']['alpha']).reshape(-1, 1))
        Settings['Layer0']['b'] = Settings['Source']['q'] * ((Settings['Layer0']['beta']).reshape(-1, 1))
        '''
        #Settings['Layer0']['alpha'] = np.reshape(Settings['Layer0']['alpha'], (1, nmax), order='F')
        #Settings['Layer0']['beta']  = np.reshape(Settings['Layer0']['beta'], (1, nmax), order='F')
        #print(Settings['Source']['p'].shape)
        #print(Settings['Layer0']['alpha'].shape)
        '''
        #elif Settings['BC'] == 'simplecavity':
        #    Settings['Layer0'] = 'error' #MieSimCav(Settings['nr'], Settings['k0s'], nmax)
        #    Settings['Layer0']['a'] = Settings['Source']['r'] * np.transpose(Settings['Layer0']['alpha'])
        #    Settings['Layer0']['b'] = Settings['Source']['s'] * np.transpose(Settings['Layer0']['beta'])
        #elif Settings['BC'] == 'coreshell':
        #    Settings['Layer0'] = 'error' #MieCoreShell(Settings['nr'], Settings['k0s'], nmax)
        #    Settings['Layer0']['a'] = Settings['Source']['p'] * np.transpose(Settings['Layer0']['alpha'])
        #    Settings['Layer0']['b'] = Settings['Source']['q'] * np.transpose(Settings['Layer0']['beta'])

    # Generating M and N Fields
    '''
    #print("TwoGR0 rhoA : ")
    #print(rhoA)
    #print("TwoGR0 Settings['ARad'] : ")
    #print(Settings['ARad'])
    #print("TwoGR0 Settings['ANAng'] : ")
    #print(Settings['ANAng'])
    #print("TwoGR0 emphi : ")
    #print(emphi)
    #sio.savemat('./TwoGR0_ARad.mat', mdict=Settings['ARad'])    
    '''
    Temp['AVSF'] = VectSphFunc(rhoA, nmax, Settings['ARad'], Settings['ANAng'], emphi)
    #sio.savemat('./TwoGR0_Temp_AVSF.mat', mdict=Temp['AVSF'])

    # Donor Dipole Field
    if Settings['BC'] == 'simplecavity':
        Settings['EdipS1'] = np.array([[0], [0], [0]])
    else:
        #if 'EdipS1' not in Settings:
            #if 'EdipS2' not in Settings:
        if 'Sph2' not in Settings['APos']:
            Settings['APos']['Sph2'] = C2S(Settings['APos']['Cart'] - Settings['DPos']['Cart'])

        # Field in the Secondary Coordinate (need to be computed at each freq.)
        '''
                #print(Settings['nr'][0])
                #print("TwoGR0 Settings['k0'] : ")
                #print(Settings['k0'])
                #print(Settings['APos']['Sph2'])
                #print(Settings['DOri']['Cart'])
        '''
        Settings['EdipS2'] = EdipField(Settings['nr'][0], Settings['k0'], Settings['APos']['Sph2'], Settings['DOri']['Cart'])

        # Transforming to the Primary Coordinate (need to be computed at each freq.)
        '''
                #B = Settings['APos']['Sph2'][1] - Settings['APos']['Sph'][1]
            #print("TwiGR0 B :")
            #print(B.dtype)
            #print("TwoGR0 Settings['EdipS2'] : ")
            #print(Settings['EdipS2'])
        '''
        Settings['EdipS1'] = S2S(Settings['EdipS2'], Settings['APos']['Sph2'][1] - Settings['APos']['Sph'][1], 0)
        '''
        #print('true')
        #else:
            #print('False')
        '''

    # Summing All order of the Scattering Field
    '''
    #print("TwoGR0 Temp['AVSF']['M'] : ")
    #print(Temp['AVSF']['M'].shape)
    #print("TwoGR0 Settings['Layer0']['b'] : ")
    #print(Settings['Layer0']['b'].shape)
    #sio.savemat('./TwoGR0_Temp.mat', mdict=Temp['AVSF'])
    #sio.savemat('./TwoGR0_Layer0.mat', mdict=Settings['Layer0'])
    '''
    Temp['Layer0M'] = (np.einsum('ijk,ij->k', Temp['AVSF']['M'], Settings['Layer0']['b'])).reshape((3, 1), order='F')
    Temp['Layer0N'] = (np.einsum('ijk,ij->k', Temp['AVSF']['N'], Settings['Layer0']['a'])).reshape((3, 1), order='F')
    '''
    #print("TwoGR0 Temp['Layer0N'] : ")
    #print(Temp['Layer0N'])
    #print("TwoGR0 Temp['Layer0M'] : ")
    #print(Temp['Layer0M'])
    '''
    # Two-Points Green's Function (G.Dori, 1/m)
    Output['G'] = Temp['Layer0M'] + Temp['Layer0N'] + Settings['EdipS1'] / (4*np.pi*(Settings['nr'][0]*Settings['k0'])**2)
    '''
    #print("TwoGR0 Output['G'] : ")
    #print(Output['G'])
    '''
    # Total Electric Field at the Acceptor Position (dipole moment = 1)
    Output['Etot'] = 4*np.pi*(Settings['nr'][0]*Settings['k0'])**2 * Output['G']
    '''
    #print("TwoGR0 Output['Etot'] : ")
    #print(Output['Etot'])
    '''
    # Total Electric Field at the Acceptor Position (SI)
    epsilon0 = 8.854187817e-12
    Output['EtotSI'] = Settings['Dpstrength'] * (Settings['nr'][0]*Settings['k0'])**2 / epsilon0 * Output['G']
    '''
    #print("TwoGR0 Output['EtotSI'] : ")
    #print(Output['EtotSI'])
    '''
    # Total Intensity at the Acceptor Position
    Output['Int'] = np.linalg.norm(Output['Etot'])**2

    # Dipole Field (dipole moment = 1, Gaussian unit)
    Output['Edip'] = Settings['EdipS1']

    # Etot / Edip
    Output['NEtot'] = np.divide(Output['Etot'], Settings['EdipS1'], where=Settings['EdipS1']!=0)
    '''
    #Output['NEtot'] = Output['Etot'] / Settings['EdipS1']
    #Output['NEtot'][np.isinf(Output['NEtot'])] = 0
    #print("TwoGR0 Settings['EdipS1'] : ")
    #print(Settings['EdipS1'])
    #print("TwoGR0 Output['NEtot'] : ")
    #print(Output['NEtot'])
    '''
    
    return Output

#print(TwoGR0(Settings))