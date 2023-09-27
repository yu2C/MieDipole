import numpy as np



def read_settings(filename):
    with open(filename, 'r') as file:
        data = json.load(file)

    # Extract data from the JSON
    settings = data['Settings']
    tmp_set = data['tmp_set']
    fplot = data['fplot']

    # Perform any post-processing or computations as needed
    # Simulated dielectric function readings
    lambda0 = read_dielectric_function(tmp_set['epsi0'])
    lambda1 = read_dielectric_function(tmp_set['epsi1'])
    lambda2 = read_dielectric_function(tmp_set['epsi2'])

    # Perform further processing as needed for your specific application

    # Construct the result dictionary
    result = {
        'Settings': settings,
        'tmp_set': tmp_set,
        'fplot': fplot,
        # Add other computed data if needed
    }

    return result

if __name__ == "__main__":
    # Specify the JSON file path
    json_file = 'C:\\Users\\a0909\\OneDrive\\桌面\\123\\InputFiles\\Demo_AngleMode_CF.json'

    # Read settings from the JSON file
    result = read_settings(json_file)

    # Perform additional operations as needed based on the extracted data

    # Print the result or save to a file if required
    print(result)


import json

def read_dielectric_function(file_path):
    with open(file_path) as json_file:
        data = json.load(json_file)
    return data

# Usage
file_path = "./Demo_AngleMode_CF.json"
data = read_dielectric_function(file_path)

# Now 'data' contains the contents of the JSON file
print(data)  # You can access and use the data from the JSON file as needed
