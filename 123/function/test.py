import numpy as np
import C2S
from Demo_WavelengthMode_CF_PCRET  import Settings
import csv
import scipy.io as sio
import json
import os


json_file = ('./123/function/Demo_WavelengthMode_CF_PCRET.json')

with open(json_file) as json_data:
        data = json.load(json_data)
        
print(type(data))
print(data)
print(data["Settings"]["ModeName"])
print(type(data["tmp_set"]["epsi0"]))

print(os.getcwd())     

A = np.zeros((1, 2))
print(A)
