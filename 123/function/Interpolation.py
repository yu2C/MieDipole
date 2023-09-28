import numpy as np
from scipy.interpolate import interp1d
from scipy.interpolate import PchipInterpolator


def Interpolation(wavelength, wavelengthi, epsii):
    if wavelengthi.shape[0] == 1:
        epsi = np.full(wavelength.shape, epsii, dtype=np.complex128)
    else:
        interp_func = PchipInterpolator(wavelengthi, epsii)
        epsi = interp_func(wavelength)
    return epsi
