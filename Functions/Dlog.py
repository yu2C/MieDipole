## Logarithmic Derivatives of Riccati-Bessel Functions
# Ref: J. Mod. Opt., 63, 2348-2355 (2016)
# Input  : z  --- complex argument of function
#          n  --- expansion order of function
# Output : D1 --- Logarithmic derivatives ( Ricatti - Bessel )
#          D3 --- Logarithmic derivatives ( Ricatti - Hankel )
import numpy as np

def Dlog(z, n):
    nex = n + int(np.floor(np.abs(1.0478 * z + 18.692)))
    D1  = np.zeros(nex, dtype = np.complex128)
    D3  = np.zeros(n, dtype = np.complex128)

    for nn in range(nex, 1, -1):
        D1[nn - 2] = nn / z - 1 / (nn / z + D1[nn - 1])

    D1[0] = (z ** 2 * np.tan(z) + z - np.tan(z)) / (-z ** 2 + z * np.tan(z))
    D3[0] = (1j * z ** 2 - z - 1j) / (z ** 2 + 1j * z)

    for nn in range(2, n + 1):
        D3[nn - 1] = -nn / z + 1 / (nn / z - D3[nn - 2])

    return D1[:n], D3

'''
# Example usage
z = 2.0
n = 5
D1_result, D3_result = Dlog(z, n)
print("D1:", D1_result)
print("D3:", D3_result)
'''