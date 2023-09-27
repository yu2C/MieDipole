import numpy as np
from scipy.interpolate import interp1d

def interpolation(wavelength, wavelengthi, epsii):
    if wavelengthi.shape[0] == 1:
        epsi = np.full(wavelength.shape, epsii)
    else:
        interp_func = interp1d(wavelengthi, epsii, kind='linear')
        epsi = interp_func(wavelength)
    return epsi
