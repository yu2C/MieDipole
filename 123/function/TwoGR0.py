import numpy as np
from Settings1   import Settings  # Assuming Settings1 is the module containing the Settings dictionary
from NormTauPiP  import NormTauPiP
from SourCoeff   import SourCoeff
from MieSingle   import MieSingle
from VectSphFunc import VectSphFunc
from SphBessel   import SphBessel
from C2S         import C2S
from S2S         import S2S
from EdipField   import EdipField
import scipy.io as sio


def TwoGR0(settings):
    # Preallocation
    Temp = {}
    Output = {}
    nmax = settings['nmax']
    rhoD = settings['nr'][0] * settings['k0'] * settings['DPos']['Sph'][0]
    rhoA = settings['nr'][0] * settings['k0'] * settings['APos']['Sph'][0]
    rhoD = rhoD[0]
    rhoA = rhoA[0]
    #print("TwoGR0 rhoD : ")
    #print(rhoD)
    #print("TwoGR0 rhoA : ")
    #print(rhoA)
    
    # Radial Functions
    if 'DRad' not in settings:
        settings['DRad'] = SphBessel(rhoD, nmax, 1, 'hankel1')

    if 'ARad' not in settings:
        settings['ARad'] = SphBessel(rhoA, nmax, 1, 'hankel1')
    
    sio.savemat('./TwoGR0_DRad.mat', mdict=settings['DRad'])
    sio.savemat('./TwoGR0_ARad.mat', mdict=settings['ARad'])


    # Angular Functions
    if 'DNAng' not in settings:
        settings['DNAng'] = NormTauPiP(nmax, settings['DPos']['Sph'][1], 'reversed')

    if 'ANAng' not in settings:
        settings['ANAng'] = NormTauPiP(nmax, settings['APos']['Sph'][1], 'normal')

    # Azimuthal Functions
    if 'emphi' not in settings:
        if settings['APos']['Sph'][2] == 0:
            # Speed-Up
            emphi = np.sqrt(1/(2*np.pi))
        else:
            # Setting exp(-inf) = 0 for Useless Array Elements
            m = -np.inf * np.ones((nmax, 2*nmax+1))
            for ii in range(1, nmax + 1):
                m[ii-1, :2*ii+1] = np.arange(-ii, ii+1)

            emphi = np.sqrt(1/(2*np.pi)) * np.exp(1j * m * settings['APos']['Sph'][2])
            # Change exp(-inf) = NaN to Zero
            emphi[np.isnan(emphi)] = 0
            
    #print("TwoGR0 emphi : ")
    #print(emphi)

    # Source Coefficients
    if 'Source' not in settings:
        settings['Source'] = SourCoeff(settings, "Green's function only")
    
    #sio.savemat('./TwoGR0_Source.mat', mdict=settings['Source'])


    # Mie Coefficients
    if 'Layer0' not in settings:
        if settings['BC'] == 'sphere':
            settings['Source']['p'] = settings['Source']['p'].reshape(nmax, 2 * nmax + 1)
            settings['Source']['q'] = settings['Source']['q'].reshape(nmax, 2 * nmax + 1)
            
            settings['Layer0'] = MieSingle(settings['nr'], settings['k0s'], nmax)
            #print(settings['Source']['p'].shape)
            #print(settings['Layer0']['alpha'])
            settings['Layer0']['alpha'] = settings['Layer0']['alpha'].reshape(1, nmax)
            settings['Layer0']['beta']  = settings['Layer0']['beta'].reshape(1, nmax)
            settings['Layer0']['a']     = settings['Source']['p'] * np.transpose(settings['Layer0']['alpha'])
            settings['Layer0']['b']     = settings['Source']['q'] * np.transpose(settings['Layer0']['beta'])
        #elif settings['BC'] == 'simplecavity':
        #    settings['Layer0'] = 'error' #MieSimCav(settings['nr'], settings['k0s'], nmax)
        #    settings['Layer0']['a'] = settings['Source']['r'] * np.transpose(settings['Layer0']['alpha'])
        #    settings['Layer0']['b'] = settings['Source']['s'] * np.transpose(settings['Layer0']['beta'])
        #elif settings['BC'] == 'coreshell':
        #    settings['Layer0'] = 'error' #MieCoreShell(settings['nr'], settings['k0s'], nmax)
        #    settings['Layer0']['a'] = settings['Source']['p'] * np.transpose(settings['Layer0']['alpha'])
        #    settings['Layer0']['b'] = settings['Source']['q'] * np.transpose(settings['Layer0']['beta'])

    # Generating M and N Fields
    #print("TwoGR0 rhoA : ")
    #print(rhoA)
    #print("TwoGR0 settings['ARad'] : ")
    #print(settings['ARad'])
    #print("TwoGR0 settings['ANAng'] : ")
    #print(settings['ANAng'])
    #print("TwoGR0 emphi : ")
    #print(emphi)
    #sio.savemat('./TwoGR0_ARad.mat', mdict=settings['ARad'])    
    Temp['AVSF'] = VectSphFunc(rhoA, nmax, settings['ARad'], settings['ANAng'], emphi)
    #sio.savemat('./TwoGR0_Temp_AVSF.mat', mdict=Temp['AVSF'])

    # Donor Dipole Field
    if settings['BC'] == 'simplecavity':
        settings['EdipS1'] = np.array([[0], [0], [0]])
    else:
        if 'EdipS1' not in settings:
            if 'EdipS2' not in settings:
                if 'APos' not in settings or 'Sph2' not in settings['APos']:
                    settings['APos']['Sph2'] = C2S(settings['APos']['Cart'] - settings['DPos']['Cart'])

                # Field in the Secondary Coordinate
                #print(settings['nr'][0])
                #print(settings['k0'])
                #print(settings['APos']['Sph2'])
                #print(settings['DOri']['Cart'])
                settings['EdipS2'] = EdipField(settings['nr'][0], settings['k0'], settings['APos']['Sph2'], settings['DOri']['Cart'])

            # Transforming to the Primary Coordinate
            B = settings['APos']['Sph2'][1] - settings['APos']['Sph'][1]
            #print("TwiGR0 B :")
            #print(B.dtype)
            #print("TwoGR0 settings['EdipS2'] : ")
            #print(settings['EdipS2'])
            settings['EdipS1'] = S2S(settings['EdipS2'], B, 0)

    # Summing All order of the Scattering Field
    #print("TwoGR0 Temp['AVSF']['M'] : ")
    #print(Temp['AVSF']['M'].shape)
    #print("TwoGR0 settings['Layer0']['b'] : ")
    #print(settings['Layer0']['b'].shape)
    #sio.savemat('./TwoGR0_Temp.mat', mdict=Temp['AVSF'])
    #sio.savemat('./TwoGR0_Layer0.mat', mdict=settings['Layer0'])

    Temp['Layer0M'] = (np.einsum('ijk,ij->k', Temp['AVSF']['M'], settings['Layer0']['b'])).reshape((3, 1))
    Temp['Layer0N'] = (np.einsum('ijk,ij->k', Temp['AVSF']['N'], settings['Layer0']['a'])).reshape((3, 1))
    #print("TwoGR0 Temp['Layer0N'] : ")
    #print(Temp['Layer0N'])
    #print("TwoGR0 Temp['Layer0M'] : ")
    #print(Temp['Layer0M'])
    # Two-Points Green's Function (G.Dori, 1/m)
    Output['G'] = Temp['Layer0M'] + Temp['Layer0N'] + settings['EdipS1'] / (4*np.pi*(settings['nr'][0]*settings['k0'])**2)
    
    #print("TwoGR0 Output['G'] : ")
    #print(Output['G'])
    # Total Electric Field at the Acceptor Position (dipole moment = 1)
    Output['Etot'] = 4*np.pi*(settings['nr'][0]*settings['k0'])**2 * Output['G']
    
    #print("TwoGR0 Output['Etot'] : ")
    #print(Output['Etot'])
    # Total Electric Field at the Acceptor Position (SI)
    epsilon0 = 8.854187817e-12
    Output['EtotSI'] = settings['Dpstrength'] * (settings['nr'][0]*settings['k0'])**2 / epsilon0 * Output['G']
    
    #print("TwoGR0 Output['EtotSI'] : ")
    #print(Output['EtotSI'])
    # Total Intensity at the Acceptor Position
    Output['Int'] = np.linalg.norm(Output['Etot'])**2

    # Dipole Field (dipole moment = 1, Gaussian unit)
    Output['Edip'] = settings['EdipS1']

    # Etot / Edip
    #print("TwoGR0 settings['EdipS1'] : ")
    #print(settings['EdipS1'])
    
    Output['NEtot'] = Output['Etot'] / settings['EdipS1']
    Output['NEtot'][np.isinf(Output['NEtot'])] = 0
    #print("TwoGR0 Output['NEtot'] : ")
    #print(Output['NEtot'])
    
    return Output

#print(TwoGR0(Settings))