# d-Matrix Evaluation (Wigner d-matrix)

import numpy as np

def Wigner_d(j, theta):
    # Calculation of J+
    m = np.arange(-j, j)
    J = np.diag(np.sqrt((j - m) * (j + m + 1)), k=-1)
    
    # Create the Spectral Decomposition Matrix J_y at z Representation
    Jy = (J - J.T) / (2j)
    
    # Diagonalization
    D, V = np.linalg.eig(Jy)
    
    # Unitary Transformation
    d = V @ np.diag(np.exp(-1j * theta *D)) @ V.conj().T
    
    # Check the Quality of the Transformation
    #np.max() will just output a number instead of column or row vector
    if np.max(np.abs(np.imag(d))) > 1e-12:
        warn_mes = 'Wigner_d may not give reliable results.'
        print(warn_mes)
    
    # Change Data Type (complex -> real)
    dd= np.real(d)
    
    return dd

#some value is approximately difference at non-diagonal term
print(Wigner_d(1.5,0))




