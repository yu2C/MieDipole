import numpy as np
import time

# Function to compare MATLAB and Python implementations
def benchmark_C2S(matlab_func, python_func, input_data):
    # Run MATLAB implementation and measure execution time
    start_time = time.time()
    matlab_output = matlab_func(input_data)
    matlab_execution_time = time.time() - start_time

    # Run Python implementation and measure execution time
    start_time = time.time()
    python_output = python_func(input_data)
    python_execution_time = time.time() - start_time

    # Compare the results
    match = np.allclose(matlab_output, python_output, atol=1e-6)
    
    return match, matlab_execution_time, python_execution_time

# Generate random input data
np.random.seed(42)
input_data = np.random.rand(3, 1000)  # Generate 1000 random points

# Benchmark the implementations
match, matlab_time, python_time = benchmark_C2S(matlab_C2S, C2S, input_data)

# Print the results
if match:
    print("Results match: MATLAB and Python implementations are equivalent.")
else:
    print("Results do not match: Check the implementations.")
print(f"MATLAB Execution Time: {matlab_time} seconds")
print(f"Python Execution Time: {python_time} seconds")
