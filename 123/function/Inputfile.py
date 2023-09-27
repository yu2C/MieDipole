import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Load the CSV file into a DataFrame
df = pd.read_csv('Ag_JPCL.csv')  # Update with your file path

# Perform the operation (second column + third column * 1i)
ni = df.iloc[:, 1] + 1j * df.iloc[:, 2]
# wavelength
l = df.iloc[:, 0] * 1e-3 # microns
# wavenumber
k0 = 2 * np.pi / l 

#if type == 'sphere':
nr = np.zeros((np.size(ni), 2))
# relative refraction index (region 0)
nr[:, 0] = 1
# relative refraction index (region 1)
nr[:, 1] = np.sqrt(ni)
# radius of the sphere (unit: micron)
rbc      = 0.085
# dimensionless radial variable
k0s      = k0 * rbc   
    

# Store the result in an array named 'ni'
ni_array = np.array(ni)

l_array = np.array(l)

k0_array = np.array(k0)


# Create an array for relative refraction index
nr = np.zeros((len(ni), 2), dtype=np.complex128)
nr[:, 0] = 1  # relative refraction index (region 0)
nr[:, 1] = np.sqrt(ni)  # relative refraction index (region 1)

nr_region_1 = nr[:, 1]

nr_region_0 = nr[:, 0]


rbc_array = np.array(rbc)

k0s_array = np.array(k0s)


# Print the 'ni' array
#print('ni:', ni_array)

#print('l:', l_array)

#print('k0:', k0_array)

#print('nr:', nr_region_1)

#print('rbc:', rbc_array)

#print('k0s:', k0s_array)






# Extract the values for the first row
x_value = df.iloc[:, 1]
y_value = df.iloc[:, 2]

# Create a scatter plot
#plt.scatter(x_value, y_value, color='blue')

# Add labels and title
#plt.xlabel('n')
#plt.ylabel('kappa')
#plt.title('Plot of complex relative permittivity')
#plt.xlim(-25, 5)
#plt.ylim(0, 3)
#plt.legend()
#plt.grid(True)

# Show the plot
#plt.show()
