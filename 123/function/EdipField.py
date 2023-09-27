## Dipole Field under the Secondary Spherical Coordinate (cgs unit)
# Input  : nr    --- relative refractive index
#          k     --- modulus of wavevector in vacuum
#          rdip  --- position vector of the dipole
#          vdip  --- direction vector of the dipole
# Output : Edips --- electric field in the spherical coordinate
import numpy as np
import C2S
import S2S
import Settings


def EdipField(nr, k, rdip, vdip):
    # Preallocation
    NX    = np.zeros((3, 1), dtype=np.complex128)
    NY    = np.zeros((3, 1), dtype=np.complex128)
    NZ    = np.zeros((3, 1), dtype=np.complex128)
    r     = rdip[0]
    theta = rdip[1]
    phi   = rdip[2]

    # Radial Function (1j * k^3 is canceled)
    Rad1 = np.exp(1j * k * r) / r * (1 / r**2 - 1j * k / r)
    Rad2 = np.exp(1j * k * r) / r * (k**2 + 1j * k / r - 1 / r**2)
    #print(Rad1)
    #print(Rad2)
    # Z-Component (1j * k^3 is canceled)
    NZ[0] =  Rad1 * np.cos(theta) * 2
    NZ[1] = -Rad2 * np.sin(theta)

    # X-Component (1j * k^3 is canceled)
    NX[0] =  Rad1 * np.sin(theta) * np.cos(phi) * 2
    NX[1] =  Rad2 * np.cos(theta) * np.cos(phi)
    NX[2] = -Rad2 * np.sin(phi)

    # Y-Component (1j * k^3 is canceled)
    NY[0] =  Rad1 * np.sin(theta) * np.sin(phi) * 2
    NY[1] =  Rad2 * np.cos(theta) * np.sin(phi)
    NY[2] =  Rad2 * np.cos(phi)

    # Electric Dipole Field (Gaussian Unit)
    EdipS = (NX * vdip[0] + NY * vdip[1] + NZ * vdip[2]) * nr

    return EdipS

'''
A = np.array([[1.0],
              [1.0],
              [1.0]
              ])

#rdip = C2S.C2S(A)
#print(rdip)
nr   = 1
k    = 1+1j
rdip = np.array([[1],
                 [0],
                 [0]
                 ])
vdip = np.array([[1],
                 [1],
                 [1]
                 ])
#print(EdipField(1, 1, rdip, vdip))
#print(result)

#Edips = S2S.S2S(result, np.pi, 0)
#print(Edips)

#print(EdipField(Settings.Settings["nr"][0], Settings.Settings["k0"], Settings.Settings["APos"]["Sph2"],Settings.Settings["DOri"]["Cart"]))

'''