## For simplecavity
# Input : 
#    Settings
#
import numpy as np
import numpy as np
from NormTauPiP import NormTauPiP
from SourCoeff import SourCoeff
from MieSingle import MieSingle
from VectSphFunc import VectSphFunc
from SphBessel import SphBessel
from Settings1 import Settings

def SingleGR1(settings):
    nmax = settings['nmax']
    rhoD = settings['nr'][1] * settings['k0'] * settings['DPos']['Sph'][0]

    # Radial Functions for Donor
    if 'DRad' not in settings:
        settings['DRad'] = SphBessel(rhoD, nmax, 1, 'bessel')

    # Angular Functions
    if 'DNAng' not in settings:
        settings['DNAng'] = NormTauPiP(nmax, settings['DPos']['Sph'][1], 'reversed')

    if 'DNAngN' not in settings:
        settings['DNAngN'] = NormTauPiP(nmax, settings['DPos']['Sph'][1], 'normal')

    # Mie Coefficients
    if 'Source' not in settings:
        settings['Source'] = SourCoeff(settings, "Green's function only")

    if 'Layer1' not in settings:
        if settings['BC'] == 'sphere':
            settings['Layer1'] = MieSingle(settings['nr'], settings['k0s'], nmax)
        elif settings['BC'] == 'coreshell':
            settings['Layer1'] = "error" #MieCoreShell(settings['nr'], settings['k0s'], nmax)
        elif settings['BC'] == 'simplecavity':
            settings['Layer1'] = "error" #MieSimCav(settings['nr'], settings['k0s'], nmax)
        
        #print(Settings['Source']['r'].shape)
        #print(Settings['Source']['s'].shape)

        #print(Settings['Layer1']['delta'].shape)
        #print(Settings['Layer1']['gamma'].shape)

        settings['Layer1']['d'] = settings['Source']['r'] * settings['Layer1']['delta'].reshape(70, 1)
        settings['Layer1']['c'] = settings['Source']['s'] * settings['Layer1']['gamma'].reshape(70, 1)
        #settings['Layer1']['d'] = np.einsum('i,j->ij', settings['Source']['r'].T, settings['Layer1']['delta'])
        #settings['Layer1']['c'] = np.einsum('i,j->i', settings['Source']['s'].T, settings['Layer1']['gamma'])


    # Azimuthal Functions
    if 'emphi' not in settings:
        emphi = np.sqrt(1/(2*np.pi))

    # Generating M and N Fields
    temp_dvsf = VectSphFunc(rhoD, nmax, settings['DRad'], settings['DNAngN'], emphi)

    # Summing All order of the Scattering Field
    temp_layer0m = np.sum(temp_dvsf['M'] * settings['Layer1']['c'].reshape((70, 141, 1)), axis=(1, 2)).reshape((70, 1))
    temp_layer0n = np.sum(temp_dvsf['N'] * settings['Layer1']['d'].reshape((70, 141, 1)), axis=(1, 2)).reshape((70, 1))

    # Scattering Part at the Donor Position
    output_escat = temp_layer0m + temp_layer0n

    # DOri.ImG.Dori
    print(output_escat.shape)
    print(settings['DOri']['Sph'].shape)
    output_img = settings['k0']/(6*np.pi) + np.imag(output_escat @ settings['DOri']['Sph'].T)

    # Purcell Factor
    output_purcell = (6*np.pi/settings['k0']) * output_img
    print(output_escat.shape)
    print(output_img.shape)
    print(output_purcell.shape)
   
    return {'EScat': output_escat, 'ImG': output_img, 'Purcell': output_purcell}

print(SingleGR1(Settings))