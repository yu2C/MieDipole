import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def ReadDielectricFunction(filename):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(filename)

    # Perform the operation (second column + third column * 1i)
    epsi = df.iloc[:, 1] + 1j * df.iloc[:, 2]

    # wavelength
    lambdaa = df.iloc[:, 0] * 1e-9  # meter

    epsi = epsi.to_numpy(dtype=np.complex128)
    lambdaa = lambdaa.to_numpy()    
    
    return lambdaa, epsi

# Usage example
filename = './123/function/Ag_JPCL.csv'
lambdaa, epsi = ReadDielectricFunction(filename)
#print(ReadDielectricFunction(filename))
# Print the arrays
#print('nr:', nr[:, 1])
#print('l:', lambdaa)
#print('k0:', epsi)

'''
 # wavenumber
    k0 = 2 * np.pi / l

    # relative refraction index (region 1)
    nr = np.zeros((len(ni), 2), dtype=np.complex128)
    nr[:, 0] = 1  # relative refraction index (region 0)
    nr[:, 1] = np.sqrt(ni)  # relative refraction index (region 1)
    
    # radius of the sphere (unit: micron)
    rbc      = 0.085
    # dimensionless radial variable
    k0s      = k0 * rbc
'''
    

# Store the result in an array named 'ni'
#ni_array = np.array(ni)

#l_array = np.array(l)

#k0_array = np.array(k0)




'''
# Extract the values for the first row
x_value = df.iloc[:, 1]
y_value = df.iloc[:, 2]

# Create a scatter plot
plt.scatter(x_value, y_value, color='blue')

# Add labels and title
plt.xlabel('n')
plt.ylabel('kappa')
plt.title('Plot of complex relative permittivity')
plt.xlim(-25, 5)
plt.ylim(0, 3)
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
'''