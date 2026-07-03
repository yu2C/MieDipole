import json
import numpy as np
from ReadDielectrcFunction import ReadDielectricFunction
from Interpolation import Interpolation
import scipy.io as sio


def ReadSettings(filename):
    # Initialization
    error_msg = False
    result    = {}
    
    with open(filename, 'r') as file:
        input_data = json.load(file)

    # Rename
    Settings = input_data['Settings']
    tmp_set  = input_data['tmp_set']
    fplot    = input_data['fplot']
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
            #print("epsi0if")
        else:
            lambda0 = np.array([0])
            epsi0 = tmp_set['epsi0']
            #print("spsi0else")
        
        #print(lambda0)
    else:
        #print("epsi0 isn't assigned yet.")
        error_msg = True

    if 'epsi1' in tmp_set:
        if isinstance(tmp_set['epsi1'], str):
            lambda1, epsi1 = ReadDielectricFunction(tmp_set['epsi1'])
            #print("epsi1if")

        else:
            lambda1 = np.array([0])
            epsi1 = tmp_set['epsi1']
            #print("epsi1else")
            
        #print(lambda1)

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
            if lambda0.size > lambda1.size:
                mind_lambda = 0
                lambdaa = lambda0  # unit: m
            else:
                mind_lambda = 1
                lambdaa = lambda1  # unit: m

            #print(lambdaa)
            nr = np.zeros((len(lambdaa), 2), dtype=np.complex128)
            nr[:, 0] = np.sqrt(Interpolation(lambdaa, lambda0, epsi0))
            nr[:, 1] = np.sqrt(Interpolation(lambdaa, lambda1, epsi1))
            #print('ReadSettings nr :')
            #print(nr.shape)
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
        
        # Convert list to array
        DPos_Cart = Settings["DPos"]["Cart"]
        #print("ReadSettings DPos_Cart : ")
        #print(DPos_Cart)
        #DPos_Cart_column = DPos_Cart.reshape()
        Settings["DPos"]["Cart"] = np.array(DPos_Cart).reshape(-1, 1)
        #print('ReadSettings type(Settings["DPos"]["Cart"]) : ')
        #print(type(Settings["DPos"]["Cart"]))
        #print(Settings["DPos"]["Cart"])
        APos_Cart = Settings["APos"]["Cart"]
        Settings["APos"]["Cart"] = np.array(APos_Cart).reshape(-1, 1)
        #print('ReadSettings Settings["APos"]["Cart"] : ')
        #print(Settings["APos"]["Cart"])
        DOri_Cart = Settings["DOri"]["Cart"]
        Settings["DOri"]["Cart"] = np.array(DOri_Cart).reshape(-1, 1)
        #print('ReadSettings Settings["DOri"]["Cart"] : ')
        #print(Settings["DOri"]["Cart"])
        AOri_Cart = Settings["AOri"]["Cart"]
        Settings["AOri"]["Cart"] = np.array(AOri_Cart).reshape(-1, 1)
        #print('ReadSettings Settings["AOri"]["Cart"] : ')
        #print(Settings["AOri"]["Cart"])

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

    elif Settings["ModeName"] == 'mapping':
        Settings["shape"] = (tmp_set["x_points"], tmp_set["y_points"])
        
        # Acceptor dipole
        xgrid = np.linspace(tmp_set["x_start"], tmp_set["x_end"], tmp_set["x_points"])
        ygrid = np.linspace(tmp_set["y_start"], tmp_set["y_end"], tmp_set["y_points"])
        
        if tmp_set["plane"] == 'xz':
            Ax, Az = np.meshgrid(xgrid, ygrid)
            Settings["plotx"] = Ax
            Settings["ploty"] = Az
            
            AxReshape = Ax.ravel()
            AyReshape = tmp_set["third_coord"] * np.ones(Ax.size)
            AzReshape = Az.ravel()
        elif tmp_set["plane"] == 'xy':
            Ax, Ay = np.meshgrid(xgrid, ygrid)
            Settings["plotx"] = Ax
            Settings["ploty"] = Ay
            
            AxReshape = Ax.ravel()
            AyReshape = Ay.ravel()
            AzReshape = tmp_set["third_coord"] * np.ones(Ax.size)
        elif tmp_set["plane"] == 'yz':
            Ay, Az = np.meshgrid(xgrid, ygrid)
            Settings["plotx"] = Ay
            Settings["ploty"] = Az

            AxReshape = tmp_set["third_coord"] * np.ones(Ay.size)
            AyReshape = Ay.ravel()
            AzReshape = Az.ravel()
        
        APos_Cart = np.array([[AxReshape], [AyReshape], [AzReshape]])
        Settings["APos"]["Cart"] = APos_Cart

        if tmp_set["lambda_i"] == tmp_set["lambda_f"]:
            lambdaa = np.array(tmp_set["lambda_i"])
            
        else:
            print("The initial wavelength isn't equal to the final wavelength.")

        if Settings["BC"] == 'sphere':
            nr = np.zeros(2)
            nr[0] = np.sqrt(Interpolation(lambdaa, lambda0, epsi0))
            nr[1] = np.sqrt(Interpolation(lambdaa, lambda1, epsi1))
        elif Settings["BC"] == 'coreshell':
            nr = np.zeros(3)
            nr[0] = np.sqrt(Interpolation(lambdaa, lambda0, epsi0))
            nr[1] = np.sqrt(Interpolation(lambdaa, lambda1, epsi1))
            nr[2] = np.sqrt(Interpolation(lambdaa, lambda2, epsi2))
            
        # Convert list to array
        DPos_Cart = Settings["DPos"]["Cart"]
        #print("ReadSettings DPos_Cart : ")
        #print(DPos_Cart)
        #DPos_Cart_column = DPos_Cart.reshape()
        Settings["DPos"]["Cart"] = np.array(DPos_Cart).reshape(-1, 1)
        #print('ReadSettings type(Settings["DPos"]["Cart"]) : ')
        #print(type(Settings["DPos"]["Cart"]))
        #print(Settings["DPos"]["Cart"])
        APos_Cart = Settings["APos"]["Cart"]
        Settings["APos"]["Cart"] = np.array(APos_Cart).reshape(-1, 1)
        #print('ReadSettings Settings["APos"]["Cart"] : ')
        #print(Settings["APos"]["Cart"])
        DOri_Cart = Settings["DOri"]["Cart"]
        Settings["DOri"]["Cart"] = np.array(DOri_Cart).reshape(-1, 1)
        #print('ReadSettings Settings["DOri"]["Cart"] : ')
        #print(Settings["DOri"]["Cart"])
        AOri_Cart = Settings["AOri"]["Cart"]
        Settings["AOri"]["Cart"] = np.array(AOri_Cart).reshape(-1, 1)
        #print('ReadSettings Settings["AOri"]["Cart"] : ')
        #print(Settings["AOri"]["Cart"])

    


    Settings['lambda'] = lambdaa
    Settings['k0']     = 2 * np.pi / lambdaa
    Settings['nr']     = nr
    Settings['rbc']    = np.transpose(Settings['rbc'])
    Settings['k0s']    = Settings['k0'] * Settings['rbc']
    #print("Settings['k0s'] :")
    #print(Settings['k0s'].shape)


    result = {
        "Settings": Settings,
        #"fplot": fplot,
        "error_msg": error_msg
    }
    
    
    
    return result




# Usage example
#filename = './123/function/Demo_WavelengthMode_CF_PCRET.json'  # Update with your file path
#result = ReadSettings(filename)
#print(result)

#sio.savemat('./ReadSettings_py.mat', mdict=result)
