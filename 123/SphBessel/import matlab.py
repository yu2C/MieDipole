import matlab.engine

# Start the MATLAB Engine for Python
eng = matlab.engine.start_matlab()

# Add the directory containing demo_function.m to MATLAB's path
eng.eval("addpath('C:\Users\a0909\OneDrive\文件\GitHub\MATLAB_to_py\SphBessel')")

# Call the MATLAB function
result = eng.demo_function()

# Stop the MATLAB Engine for Python
eng.quit()

# Display the result
print(result)
