
import numpy as np
from scipy.linalg import eig

j = 1.5
theta = 0

#def Wigner_d(j, theta):
    # Calculation of J+
m = np.arange(-j, j)
J = np.diag(np.sqrt((j - m) * (j + m + 1)), k=-1)
    
print('This is m')
print(m)
print('===============')
print('This is J')
print(J)
print('===============')


    # Create the Spectral Decomposition Matrix J_y at z Representation
Jy = (J - J.T) / (2j)
    
print('This is Jy')
print(Jy)
print('===============')

    # Diagonalization
D, V = eig(Jy)

print('D is the eigenvalue')
print(D)
print('===============')
print('V is the eigenvector') 
print(V)
print('===============')
#check the eignevalue problem
#need to add a tolerance thresshold
tolerance = 1e-15
E = V @ np.diag(D) @ V.conj().T
E[np.isclose(E, 0, atol = tolerance)] = 0
print('This is E')
print(E)
print('===============')



    # Unitary Transformation
G = np.exp(-1j * theta * D)

d = V @ np.diag(G) @ V.conj().T


print('This is G')
print(G)
print('===============')
print('This is d')
print(d)
print('===============')

    
    # Check the Quality of the Transformation
    #np.max() will just output a number instead of column or row vector
if np.max(np.abs(np.imag(d))) > 1e-12:
        warn_mes = 'Wigner_d may not give reliable results.'
        print(warn_mes)
    
    # Change Data Type (double complex -> double real)
dd = np.diag(np.real(d))
print('This is dd')
print(dd)
print('===============')

    
    #return d


