import numpy as np

def EdipField(nr, k, rdip, vdip):
    # Preallocation
    NX = np.zeros(3)
    NY = np.zeros(3)
    NZ = np.zeros(3)
    r = rdip[0]
    theta = rdip[1]
    phi = rdip[2]

    # Radial Function (1j * k^3 is canceled)
    Rad1 = np.exp(1j * k * r) / r * (r**(-2) - 1j * k / r)
    Rad2 = np.exp(1j * k * r) / r * (k**2 + 1j * k / r - r**(-2))

    # Z-Component (1j * k^3 is canceled)
    NZ[0] = Rad1 * np.cos(theta) * 2
    NZ[1] = -Rad2 * np.sin(theta)

    # X-Component (1j * k^3 is canceled)
    NX[0] = Rad1 * np.sin(theta) * np.cos(phi) * 2
    NX[1] = Rad2 * np.cos(theta) * np.cos(phi)
    NX[2] = -Rad2 * np.sin(phi)

    # Y-Component (1j * k^3 is canceled)
    NY[0] = Rad1 * np.sin(theta) * np.sin(phi) * 2
    NY[1] = Rad2 * np.cos(theta) * np.sin(phi)
    NY[2] = Rad2 * np.cos(phi)

    # Electric Dipole Field (Gaussian Unit)
    EdipS = (NX * vdip[0] + NY * vdip[1] + NZ * vdip[2]) * nr

    return EdipS
