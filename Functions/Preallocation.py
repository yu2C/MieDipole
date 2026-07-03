import numpy as np
import C2S
import vecTrans
import NormTauPiP

# Transforming Coordinate
Settings['DPos']['Sph'] = C2S.C2S(Settings['DPos']['Cart'])
Settings['DOri']['Sph'] = vecTrans.VecTrans(Settings['DOri']['Cart'], Settings['DPos']['Sph'][1:3], 'C2S')

# Pre-Calculation of Fixed Variables for Each Mode
if Settings['ModeName'] == 'wavelength':
    # Times of the 'for loop'
    Settings['nn'] = Settings['nr'].shape[0]

    # Coordinate Transformation
    Settings['APos']['Sph'] = C2S.C2S(Settings['APos']['Cart'])
    Settings['AOri']['Sph'] = vecTrans.VecTrans(Settings['AOri']['Cart'], Settings['APos']['Sph'][1:3], 'C2S')
    Settings['APos']['Sph2'] = C2S.C2S(Settings['APos']['Cart'] - Settings['DPos']['Cart'])

    # Angular Functions
    Settings['DNAng'] = NormTauPiP.NormTauPiP(Settings['nmax'], Settings['DPos']['Sph'][1], 'reversed')
    Settings['ANAng'] = NormTauPiP.NormTauPiP(Settings['nmax'], Settings['APos']['Sph'][1], 'normal')
