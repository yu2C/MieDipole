import numpy as np
from scipy.special import spherical_jn, spherical_yn

def MieSingle(nr, ks, nmax):
    # Checking Input
    if len(nr) != 2 or len(ks) != 1:
        raise ValueError("Error input size of 'nr' or 'ks' from 'MieSingle'")

    # Defining Variables
    n0 = nr[0]
    n1 = nr[1]
    n0kr1 = n0 * ks[0]
    n1kr1 = n1 * ks[0]

    # Generating Radial Functions
    n0psi, n0dpsi = spherical_jn(nmax, n0kr1), spherical_jn(nmax, n0kr1, derivative=True)
    n0xi, n0dxi = spherical_yn(nmax, n0kr1), spherical_yn(nmax, n0kr1, derivative=True)
    n1psi, n1dpsi = spherical_jn(nmax, n1kr1), spherical_jn(nmax, n1kr1, derivative=True)

    # Coefficients
    alpha = -(n1 * n0dpsi * n1psi - n0 * n0psi * n1dpsi) / (n1 * n0dxi * n1psi - n0 * n0xi * n1dpsi)
    beta = -(n0 * n0dpsi * n1psi - n1 * n0psi * n1dpsi) / (n0 * n0dxi * n1psi - n1 * n0xi * n1dpsi)
    gamma = n1 * (n0dpsi * n0xi - n0psi * n0dxi) / (n1 * n1dpsi * n0xi - n0 * n1psi * n0dxi)
    delta = n1 * (n0dpsi * n0xi - n0psi * n0dxi) / (n0 * n1dpsi * n0xi - n1 * n1psi * n0dxi)

    Coeffs = {"alpha": alpha, "beta": beta, "gamma": gamma, "delta": delta}

    return Coeffs
