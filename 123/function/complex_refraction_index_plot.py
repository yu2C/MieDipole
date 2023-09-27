import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Load the CSV file into a DataFrame
df = pd.read_csv('./function\Ag_JPCL.csv')  # Update with your file path

# Perform the operation (second column + third column * 1i)
ni = df.iloc[:, 1] + 1j * df.iloc[:, 2]

# Store the result in an array named 'ni'
ni_array = np.array(ni)


# Print the 'ni' array
print('ni:', ni_array)




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
