import numpy as np
import rcbesselc as rc

# Define a range of complex input values z
z_values = np.linspace(-2 - 2j, 2 + 2j, 100)  # Adjust the number of points as needed

# Define the orders n for which you want to compute the functions
n_values = [1, 2, 3, 4, 5]  # Adjust as needed

# Initialize arrays to store results from both MATLAB and Python
matlab_results = []
python_results = []

# Loop through each z value and n value
for z in z_values:
    for n in n_values:
        # Compute Riccati-Bessel functions using MATLAB code
        # Call MATLAB code here and store the result in matlab_result

        # Compute Riccati-Bessel functions using Python code
        rcj, _, _, _ = rc.rcbesselc(z, n)  # Use your Python code
        python_results.append(rcj)

# At this point, you have both MATLAB and Python results in matlab_results and python_results

# Now, you can compare the results as needed to verify if they match
# You can use NumPy's allclose function to compare complex arrays
for matlab_result, python_result in zip(matlab_results, python_results):
    if not np.allclose(matlab_result, python_result, rtol=1e-6, atol=1e-6):
        print("Results do not match for some z and n values.")

# If the print statement is not executed, it means the results match within the specified tolerance.
