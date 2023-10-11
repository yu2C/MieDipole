import numpy as np
from Settings1 import Settings  # Assuming Settings1 is the module containing the Settings dictionary
from NormTauPiP import NormTauPiP
from SourCoeff import SourCoeff
from MieSingle import MieSingle
from VectSphFunc import VectSphFunc
from SphBessel import SphBessel
from C2S import C2S
from S2S import S2S
from EdipField import EdipField

def TwoGR1(settings):
    nmax = settings['nmax']

    if settings['BC'] == 'simplecavity':
        rhoD = settings['nr'][1] * settings['k0'] * settings['DPos']['Sph'][0]
    else:
        rhoD = settings['nr'][0] * settings['k0'] * settings['DPos']['Sph'][0]

    rhoA = settings['nr'][1] * settings['k0'] * settings['APos']['Sph'][0]

    # Radial Functions
    if 'DRad' not in settings:
        if settings['BC'] == 'simplecavity':
            settings['DRad'] = SphBessel(rhoD, nmax, 1, 'bessel')
        else:
            settings['DRad'] = SphBessel(rhoD, nmax, 1, 'hankel1')

    if 'ARad' not in settings:
        settings['ARad'] = SphBessel(rhoA, nmax, 1, 'bessel')
    elif 'j1' not in settings['ARad']:
        settings['ARad'] = SphBessel(rhoA, nmax, 1, 'bessel')

    # Angular Functions
    if 'DNAng' not in settings:
        settings['DNAng'] = NormTauPiP(nmax, settings['DPos']['Sph'][1], 'reversed')

    if 'ANAng' not in settings:
        settings['ANAng'] = NormTauPiP(nmax, settings['APos']['Sph'][1], 'normal')

    # Azimuthal Functions
    if 'emphi' not in settings:
        if settings['APos']['Sph'][2] == 0:
            # For Speed-Up
            emphi = np.sqrt(1 / (2 * np.pi))
        else:
            # Setting exp(-inf) = 0 for Useless Array Elements
            m = -np.inf * np.ones((nmax, 2 * nmax + 1))
            for ii in range(1, nmax + 1):
                m[ii - 1, :2 * ii + 1] = -ii + np.arange(2 * ii + 1)

            emphi = np.sqrt(1 / (2 * np.pi)) * np.exp(1j * m * settings['APos']['Sph'][2])
            # Change exp(-inf) = NaN to Zero
            emphi[np.isnan(emphi)] = 0

    # Mie Coefficients
    if 'Source' not in settings:
        settings['Source'] = SourCoeff(settings, "Green's function only")

    if 'layer1' not in settings:
        if settings['BC'] == 'sphere':
            settings['Layer1'] = MieSingle(settings['nr'], settings['k0s'], nmax)
            settings['Layer1']['d'] = settings['Source']['p'] * np.transpose(settings['Layer1']['delta'])
            settings['Layer1']['c'] = settings['Source']['q'] * np.transpose(settings['Layer1']['gamma'])
        elif settings['BC'] == 'simplecavity':
            settings['Layer1'] = 'error' #MieSimCav(settings['nr'], settings['k0s'], nmax)
            settings['Layer1']['d'] = settings['Source']['r'] * np.transpose(settings['Layer1']['delta'])
            settings['Layer1']['c'] = settings['Source']['s'] * np.transpose(settings['Layer1']['gamma'])
        elif settings['BC'] == 'coreshell':
            # Alert of the Unsupported Function
            #Output['error1'] = "EFieldR1 for coreshell structures is not supported yet."
            settings['Layer1']['gamma'] = 0
            settings['Layer1']['delta'] = 0
            settings['Layer1']['d'] = settings['Source']['p'] * np.transpose(settings['Layer1']['delta'])
            settings['Layer1']['c'] = settings['Source']['q'] * np.transpose(settings['Layer1']['gamma'])

    # Generating M and N Fields
    temp_avsf = VectSphFunc(rhoA, nmax, settings['ARad'], settings['ANAng'], emphi)

    # Donor Dipole Field
    if settings['BC'] == 'simplecavity':
        if 'EdipS2' not in settings:
            if 'APos' not in settings or 'Sph2' not in settings['APos']:
                settings['APos']['Sph2'] = C2S(settings['APos']['Cart'] - settings['DPos']['Cart'])

            # Field in the Secondary Coordinate
            settings['EdipS2'] = EdipField(settings['nr'][1], settings['k0'], settings['APos']['Sph2'], settings['DOri']['Cart'])

            # Transforming to the Primary Coordinate
            settings['EdipS1'] = S2S(settings['EdipS2'], (settings['APos']['Sph2'][1] - settings['APos']['Sph'][1]), 0)
    else:
        settings['EdipS1'] = np.array([[0], [0], [0]])

    # Summing All Order of the Field in Layer 1
    temp_layer1m = np.reshape(np.sum(temp_avsf['M'] * settings['Layer1']['c'], axis=(1, 2)), (3, 1))
    temp_layer1n = np.reshape(np.sum(temp_avsf['N'] * settings['Layer1']['d'], axis=(1, 2)), (3, 1))

    # Two-Points Green's Function (G.Dori, 1/m)
    output_g = temp_layer1m + temp_layer1n + settings['EdipS1'] / (4 * np.pi * (settings['nr'][1] * settings['k0']) ** 2)

    # Total Electric Field at the Acceptor Position (dipole moment = 1)
    output_etot = 4 * np.pi * (settings['nr'][1] * settings['k0']) ** 2 * output_g

    # Total Electric Field at the Acceptor Position (SI)
    epsilon0 = 8.854187817e-12
    output_etotsi = settings['Dpstrength'] * (settings['nr'][1] * settings['k0']) ** 2 / epsilon0 * output_g

    # Total intensity at the Acceptor position
    output_int = np.linalg.norm(output_etot) ** 2

    # Dipole field
    output_edip = settings['EdipS1']

    # Etot / Edip
    output_ne_tot = output_etot / settings['EdipS1']

    return {
        'G': output_g,
        'Etot': output_etot,
        'EtotSI': output_etotsi,
        'Int': output_int,
        'Edip': output_edip,
        'NEtot': output_ne_tot
    }

#print(TwoGR1(Settings))

