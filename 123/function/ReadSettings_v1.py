import json
import numpy as np
from ReadDielectrcFunction import ReadDielectricFunction
from Interpolation import Interpolation


def read_settings(filename):
    # Initialization
    error_msg = False
    
    with open(filename, 'r') as file:
        input_data = json.load(file)

    # Rename
    Settings = input_data['Settings']
    tmp_set = input_data['tmp_set']
    fplot = input_data['fplot']
    '''
    # Post-processing for range and subrange
    if 'range' in fplot:
        for i in range(4):
            if i == 0 or i == 2:
                if np.isnan(fplot['range'][i]):
                    fplot['range'][i] = float('-inf')
            elif i == 1 or i == 3:
                if np.isnan(fplot['range'][i]):
                    fplot['range'][i] = float('inf')
    fplot['range'] = np.array(fplot['range'])

    if 'subrange' in fplot:
        for i in range(4):
            if i == 0 or i == 2:
                if np.isnan(fplot['subrange'][i]):
                    fplot['subrange'][i] = float('-inf')
            elif i == 1 or i == 3:
                if np.isnan(fplot['subrange'][i]):
                    fplot['subrange'][i] = float('inf')
    fplot['subrange'] = np.array(fplot['subrange'])
    '''




    # Verify the assignments of dielectric function
    if 'epsi0' in tmp_set:
        if isinstance(tmp_set['epsi0'], str):
            lambda0, epsi0 = ReadDielectricFunction(tmp_set['epsi0'])
            print("if")
        else:
            lambda0 = np.array([0])
            epsi0 = tmp_set['epsi0']
            print("else")
        
        print(lambda0)
    else:
        print("epsi0 isn't assigned yet.")
        error_msg = True

    if 'epsi1' in tmp_set:
        if isinstance(tmp_set['epsi1'], str):
            lambda1, epsi1 = ReadDielectricFunction(tmp_set['epsi1'])
        else:
            lambda1 = np.array([0])
            epsi1 = tmp_set['epsi1']
    else:
        print("epsi1 isn't assigned yet.")
        error_msg = True

    if Settings['BC'] == 'coreshell':
        if 'epsi2' in tmp_set:
            if isinstance(tmp_set['epsi2'], str):
                lambda2, epsi2 = ReadDielectricFunction(tmp_set['epsi2'])
            else:
                lambda2 = 0
                epsi2 = tmp_set['epsi2']
        else:
            print("epsi2 isn't assigned yet.")
            error_msg = True


    # Post-Processing for Different Mode
    if Settings['ModeName'] == 'wavelength':
        if Settings['BC'] == 'sphere':
            if len(lambda0) > 0:
                mind_lambda = 0
                lambdaa = lambda0  # unit: m
            elif len(lambda1) > 0:
                mind_lambda = 1
                lambdaa = lambda1  # unit: m

            nr = np.zeros((len(lambdaa), 2))
            nr[:, 0] = np.sqrt(Interpolation(lambdaa, lambda0, epsi0))
            nr[:, 1] = np.sqrt(Interpolation(lambdaa, lambda1, epsi1))
        elif Settings['BC'] == 'coreshell':
            # Choose the appropriate lambda based on availability
            if len(lambda0) > 0:
                mind_lambda = 0
                lambdaa = lambda0  # unit: m
            elif len(lambda1) > 0:
                mind_lambda = 1
                lambdaa = lambda1  # unit: m
            elif len(lambda2) > 0:
                mind_lambda = 2
                lambdaa = lambda2  # unit: m


            nr = np.zeros((len(lambdaa), 3))
            nr[:, 0] = np.sqrt(Interpolation(lambdaa, lambda0, epsi0))
            nr[:, 1] = np.sqrt(Interpolation(lambdaa, lambda1, epsi1))
            nr[:, 2] = np.sqrt(Interpolation(lambdaa, lambda2, epsi2))

    elif Settings['ModeName'] == 'angle':
        Theta_num = np.abs(tmp_set['Theta_f'] - tmp_set['Theta_i']) / tmp_set['ThetaResol'] + 1
        R = tmp_set['Ar'] * np.ones(Theta_num)
        Theta = np.pi * np.linspace(tmp_set['Theta_i'], tmp_set['Theta_f'], Theta_num) / 180
        Phi = tmp_set['Phi'] * np.ones(Theta_num)
        Settings['APos']['Cart'] = np.array([
            tmp_set['Ar'] * np.sin(Theta) * np.cos(tmp_set['Phi']),
            tmp_set['Ar'] * np.sin(Theta) * np.sin(tmp_set['Phi']),
            tmp_set['Ar'] * np.cos(Theta)
        ])
        Settings['APos']['Sph'] = np.array([R, Theta, Phi])

        if tmp_set['lambda_i'] == tmp_set['lambda_f']:
            lambdaa = tmp_set['lambda_i']

        if Settings['BC'] == 'sphere':
            nr = np.zeros(2)
            nr[0] = np.sqrt(Interpolation(lambdaa, lambda0, epsi0))
            nr[1] = np.sqrt(Interpolation(lambdaa, lambda1, epsi1))

        elif Settings['BC'] == 'coreshell':
            nr = np.zeros(3)
            nr[0] = np.sqrt(Interpolation(lambdaa, lambda0, epsi0))
            nr[1] = np.sqrt(Interpolation(lambdaa, lambda1, epsi1))
            nr[2] = np.sqrt(Interpolation(lambdaa, lambda2, epsi2))

    Settings['lambda'] = lambdaa
    Settings['k0'] = 2 * np.pi / lambdaa
    Settings['nr'] = nr
    Settings['rbc'] = np.transpose(Settings['rbc'])
    Settings['k0s'] = Settings['k0'] * Settings['rbc']


    result = {
        "Settings": Settings,
        "fplot": fplot,
        "error_msg": error_msg
    }

    return result




# Usage example
filename = './123/function/Demo_WavelengthMode_CF_PCRET.json'  # Update with your file path
result = read_settings(filename)
print(result)
