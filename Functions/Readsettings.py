# Read the inputfile 
# Input : 
#    filename --- file.json

import numpy as np
import json
from ReadDielectrcFunction import ReadDielectricFunction


def read_settings(filename):
    with open(filename, 'r') as file:
        data = json.load(file)

    # Extract data from the JSON
    Settings = data['Settings']
    tmp_set  = data['tmp_set']
    fplot    = data['fplot']
    
    if tmp_set["epsi0"] == 1:
        [lambda0, epsi0] = ReadDielectricFunction()
    # Perform any post-processing or computations as needed
    # Simulated dielectric function readings
    lambda0 = ReadDielectricFunction(tmp_set['epsi0'])
    lambda1 = ReadDielectricFunction(tmp_set['epsi1'])
    lambda2 = ReadDielectricFunction(tmp_set['epsi2'])

    # Perform further processing as needed for your specific application

    # Construct the result dictionary
    result = {
        'Settings': settings,
        'tmp_set': tmp_set,
        'fplot': fplot,
        # Add other computed data if needed
    }

    return result





# Usage
file_path = "./Demo_AngleMode_CF.json"
# Now 'data' contains the contents of the JSON file
