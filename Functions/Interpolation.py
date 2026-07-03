import numpy as np
from scipy.interpolate import PchipInterpolator


def Interpolation(wavelength, wavelengthi, epsii):
    wavelength = np.asarray(wavelength)
    wavelengthi = np.asarray(wavelengthi)
    epsii = np.asarray(epsii, dtype=np.complex128)

    if wavelengthi.shape[0] == 1:
        epsi = np.full(wavelength.shape, epsii, dtype=np.complex128)
    else:
        # MATLAB interp1(..., 'pchip') supports complex y; PchipInterpolator does not.
        real_interp = PchipInterpolator(wavelengthi, epsii.real)
        imag_interp = PchipInterpolator(wavelengthi, epsii.imag)
        epsi = real_interp(wavelength) + 1j * imag_interp(wavelength)
    return epsi
