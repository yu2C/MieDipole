import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
import matplotlib.axes as x
import sys
import json
#from Settings1 import Settings
from ReadSettings_v1 import ReadSettings
from SingleGR0_v1    import SingleGR0
from SingleGR1       import SingleGR1
from datetime        import datetime
from C2S             import C2S
from VecTrans        import VecTrans
from NormTauPiP      import NormTauPiP
from SphBessel       import SphBessel
from MieSingle       import MieSingle
from SourCoeff       import SourCoeff
from TwoGR0          import TwoGR0
from TwoGR1          import TwoGR1

###########################################################################
## Start the Program

# set the temperary path
sys.path.append('./Functions/')

# File to be calculated
FilePath = './' #'./123/function/'#'./InputFiles/'  # Folder Path of Input Files
FileName = 'Demo_WavelengthMode_CF_sphere'  # File Name

# Output Figure Size (value = 0~1)
Resize = 0.5
############################################################################
############################################################################
## Loading the Input File

# Load JSON input file
Inputfile = ReadSettings(f'{FilePath}{FileName}.json')

Settings = Inputfile['Settings']
#print(Settings)
#print("Settings['nr']")
#print(Settings['nr'])
#fplot = Inputfile['fplot']

if Settings['ModeName'] == 'wavelength':
    k0  = Settings['k0']
    k0  = np.array(k0)
    k0s = Settings['k0s']
    k0s = np.array(k0s)
    lambda_val = Settings['lambda']
    nr  = Settings['nr']
    nr  = np.array(nr)
    #print(Settings['k0s'])
    #print(k0s)
elif Settings['ModeName'] == 'angle':
    Ar = Settings['APos']['Sph'][0][0]
    Atheta = Settings['APos']['Sph'][1]
    Aphi = Settings['APos']['Sph'][2][0]
    Ax = Settings['APos']['Cart'][0]
    Ay = Settings['APos']['Cart'][1]
    Az = Settings['APos']['Cart'][2]

# information of inputfile
start_time = datetime.now()
print('Beginning the program...')
# information of mode
print("Using Mode:", Settings["ModeName"])
# information of structure
print("Using Structure:", Settings["BC"])
############################################################################
############################################################################
## Check the input is correct

if Settings['BC'] == 'simplecavity':
    if np.linalg.norm(Settings['DPos']['Cart']) >= Settings['rbc']:
        raise ValueError('Error: The donor dipole should be inside the cavity.')
        
elif Settings['BC'] == 'sphere':
    if np.linalg.norm(Settings['DPos']['Cart']) <= Settings['rbc']:
        raise ValueError('Error: The donor dipole should be outside the sphere.')
        
elif Settings['BC'] == 'coreshell':
    if np.linalg.norm(Settings['DPos']['Cart']) <= Settings['rbc'][0]:
        raise ValueError('Error: The donor dipole should be outside the shell.')

############################################################################
############################################################################
## Pre-Processing

# Transforming Coordinate
Settings['DPos']['Sph'] = C2S(Settings['DPos']['Cart'])
Settings['DOri']['Sph'] = VecTrans(Settings['DOri']['Cart'], Settings['DPos']['Sph'][1:3], 'C2S')

# for wavelength mode
if Settings['ModeName'] == 'wavelength':
    # Times of the 'for loop'
    #print(Settings['nr'].shape)
    Settings['nn'] = Settings['nr'].shape[0]
    #print(Settings['nn'])

    #print("Main Settings['nn']")
    #print(Settings['nn'])
    #print("Main Settings['nr']")
    #print(Settings['nr'].shape)

    # Coordinate Transformation
    Settings['APos']['Sph']  = C2S(Settings['APos']['Cart'])
    Settings['AOri']['Sph']  = VecTrans(Settings['AOri']['Cart'], Settings['APos']['Sph'][1:3], 'C2S')
    Settings['APos']['Sph2'] = C2S(Settings['APos']['Cart'] - Settings['DPos']['Cart'])

    # Angular Functions
    Settings['DNAng'] = NormTauPiP(Settings['nmax'], Settings['DPos']['Sph'][1], 'reversed')
    Settings['ANAng'] = NormTauPiP(Settings['nmax'], Settings['APos']['Sph'][1], 'normal')


    #sio.savemat('./main_DNAng.mat', mdict=Settings['DNAng'])
    #sio.savemat('./main_ANAng.mat', mdict=Settings['ANAng'])
elif Settings["ModeName"] == 'mapping':
    # Times of the 'for loop'
    Settings["nn"] = len(Settings["APos"]["Cart"][1])
    # Coordinate Transformation
    Settings["APos"]["Sph"] = C2S(Settings["APos"]["Cart"])
    # Radial Functions
    rhoD = Settings["nr"][0] * Settings["k0"] * Settings["DPos"]["Sph"][0]
    if Settings["BC"] == 'simplecavity':
        Settings["DRad"] = SphBessel(rhoD, Settings["nmax"], 1, 'bessel')
    else:
        Settings["DRad"] = SphBessel(rhoD, Settings["nmax"], 1, 'hankel1')
    # Angular Functions
    Settings["DNAng"] = NormTauPiP(Settings["nmax"], Settings["DPos"]["Sph"][1], 'reversed')
    # Source Coefficients
    Settings["Source"] = SourCoeff(Settings, "Green's function only")
    # Layer0 Coefficients
    if Settings["BC"] == 'sphere':
        Settings["Layer0"] = MieSingle(Settings["nr"], Settings["k0s"], Settings["nmax"])
    # elif Settings["BC"] == 'coreshell':
    #     Settings["Layer0"] = MieCoreShell(Settings["nr"], Settings["k0s"], Settings["nmax"])
    # elif Settings["BC"] == 'simplecavity':
    #     Settings["Layer0"] = MieSimCav(Settings["nr"], Settings["k0s"], Settings["nmax"])
    # Layer1 Coefficients
    if Settings["BC"] == 'sphere':
        Settings["Layer1"] = MieSingle(Settings["nr"], Settings["k0s"], Settings["nmax"])
    # elif Settings["BC"] == 'coreshell':
    #     print("The feature of core/shell mapping is not supported yet.")
    #     print("Overwrite the electric field of the inner region by zero.")
    #     Settings["Layer1"]["gamma"] = 0
    #     Settings["Layer1"]["delta"] = 0
    # elif Settings["BC"] == 'simplecavity':
    #     Settings["Layer1"] = MieSimCav(Settings["nr"], Settings["k0s"], Settings["nmax"])
    
    if Settings["BC"] == 'simplecavity':
        Settings["Layer0"]["a"] = Settings["Source"]["r"] * (Settings["Layer0"]["alpha"]).reshape(-1, 1)
        Settings["Layer0"]["b"] = Settings["Source"]["s"] * (Settings["Layer0"]["beta"]).reshape(-1, 1)
        Settings["Layer1"]["d"] = Settings["Source"]["r"] * (Settings["Layer1"]["delta"]).reshape(-1, 1)
        Settings["Layer1"]["c"] = Settings["Source"]["s"] * (Settings["Layer1"]["gamma"]).reshape(-1, 1)
    else:
        Settings["Layer0"]["a"] = Settings["Source"]["p"] * (Settings["Layer0"]["alpha"]).reshape(-1, 1)
        Settings["Layer0"]["b"] = Settings["Source"]["q"] * (Settings["Layer0"]["beta"]).reshape(-1, 1)
        Settings["Layer1"]["d"] = Settings["Source"]["p"] * (Settings["Layer1"]["delta"]).reshape(-1, 1)
        Settings["Layer1"]["c"] = Settings["Source"]["q"] * (Settings["Layer1"]["gamma"]).reshape(-1, 1)



    #sio.savemat('./main_DNAng.mat', mdict=Settings['DNAng'])
    #sio.savemat('./main_ANAng.mat', mdict=Settings['ANAng'])


# Radial Functions
#rhoD = Settings['nr'][0] * Settings['k0'] * Settings['DPos']['Sph'][0]
#Settings['DRad'] = SphBessel(rhoD, Settings['nmax'], 1, 'hankel1') 

############################################################################
############################################################################
## Preallocation
Etot     = np.zeros((Settings['nn'], 3), dtype=np.complex128)
NormEtot = np.zeros((Settings['nn'], 3), dtype=np.complex128)
Edip     = np.zeros((Settings['nn'], 3), dtype=np.complex128)
if Settings['ModeName'] == 'wavelength':
    EScat    = np.zeros((Settings['nn'], 3), dtype=np.complex128)
    ImG      = np.zeros((Settings['nn'], 1))
    Purcell  = np.zeros((Settings['nn'], 1))
    if not np.array_equal(Settings['APos']['Cart'], Settings['DPos']['Cart']):
        ImG_vec = np.zeros((Settings['nn'], 3))



#print(Settings)
############################################################################
############################################################################
## Main Loop
if Settings['ModeName'] == 'wavelength':
    for ii in range(Settings['nn']):
        Settings['k0']  = k0[ii] # variable
        Settings['nr']  = np.array(nr[ii, :], dtype=np.complex128)
        #Settings['nr']  = Settings['nr'].reshape((1, 2))
        Settings['k0s'] = np.array([k0s[ii]]) # convert to array for coreshell
        '''
        #print("main Settings['k0']")
        #print(Settings['k0'])
        #print("main k0 : ")
        #print('k0')
        #print("main Settings['nr'] : ")
        #print(Settings['nr'])
        #print("main Settings['k0s'] : ")
        #print(Settings['k0s'])
        '''

        # Determine which function is called by the acceptor position
        if np.array_equal(Settings['APos']['Cart'], Settings['DPos']['Cart']):
            if Settings['BC'] == 'simplecavity':
                Output = SingleGR1(Settings)
            else:
                Output = SingleGR0(Settings)

            EScat[ii, :]    = (Output['EScat']).T
            ImG[ii, :]      = (Output['ImG']).T
            Purcell[ii, :]  = (Output['Purcell']).T
        else:
            if Settings['APos']['Sph'][0] >= Settings['rbc'][0]:
                Output = TwoGR0(Settings)
            else:
                Output = TwoGR1(Settings)

            ImG_vec[ii, :]  = (np.imag(Output['G'])).T
            Etot[ii, :]     = (Output['Etot']).T
            Edip[ii, :]     = (Output['Edip']).T
            NormEtot[ii, :] = (Output['NEtot']).T

        # Information
        #print(f'Progress: {((ii + 1) / Settings["nn"]) * 100:.2f}%')
elif Settings["ModeName"] == 'mapping':
    tmp1 = Settings["APos"]["Cart"]
    tmp2 = Settings["APos"]["Sph"]
    print('tmp1', tmp1.shape)
    print('tmp2', tmp2.shape)
    Etot = []
    EtotSI = []
    Edip = []
    for ii in range(Settings["nn"]):
        Settings["APos"]["Cart"] = tmp1[:, ii]
        Settings["APos"]["Sph"] = tmp2[:, ii]
        
        if Settings["APos"]["Sph"][0] >= Settings["rbc"][0]:
            Output = TwoGR0(Settings)
        else:
            Output = TwoGR1(Settings)
        
        Etot.append(list(map(list, zip(*Output["Etot"]))))
        EtotSI.append(list(map(list, zip(*Output["EtotSI"]))))
        Edip.append(list(map(list, zip(*Output["Edip"]))))
        
        # # Information
        # print(f"Progress: {((ii+1)/Settings['nn'])*100:.2f}%")

############################################################################
############################################################################
## Post-processing
if Settings['ModeName'] == 'wavelength':
    if Settings['Quantity'] == 'CF':
        # Coupling Factor
        CF = abs(Etot @ Settings['AOri']['Sph']) ** 2
        # Coupling Factor along R Direction (Vacuum)
        CFdip = abs(Edip @ Settings['AOri']['Sph']) ** 2
        # Setting 0/0 to 0 for Etot/Edip
        NormEtot[np.isnan(NormEtot)] = 0
        # Enhancement Factor
        EF = abs(NormEtot @ Settings['AOri']['Sph']) ** 2
        Result = {
            'CF_py'       : CF,
            'CFdip_py'    : CFdip,
            'NormEtot_py' : NormEtot,
            'EF_py'       : EF,
        }
        sio.savemat('./main_result.mat', mdict=Result)
    elif Settings['Quantity'] == 'Purcell':
        Result = {
            'EScat_py'   : EScat,
            'ImG_py'     : ImG,
            'Purcell_py' : Purcell
        }
        sio.savemat('./main_result.mat', mdict=Result)
    elif Settings['Quantity'] == 'ImG':
        if 'ImG_vec' in locals(): 
            ImG = ImG_vec @ Settings['AOri']['Sph']
        
        Result = {
            'EScat_py'   : EScat,
            'ImG_py'     : ImG,
            'Purcell_py' : Purcell
        }
        sio.savemat('./main_result.mat', mdict=Result)
    elif Settings['Quantity'] == 'J':
        #ImG = ImG_vec @ Settings['AOri']['Sph']
        
        c        = 2.9979e8
        Debye    = 3.33564e-30
        epsilon0 = 8.854187817e-12
        hbar     = 1.05457182e-34
        const    = ((2 * np.pi * 1239.84193 / (lambda_val * 1e9) * 2.4179893e14) ** 2
                    / c ** 2 * Debye ** 2 / (np.pi * hbar * epsilon0))
        J = const.reshape(-1, 1) * ImG
        Result = {
            'J_py'   : J,
        }
        sio.savemat('./main_result.mat', mdict=Result)
        
elif Settings["ModeName"] == 'mapping':
    # c = 2.9979e8
    # const = Dpstrength * c**2 * 1e-5
    
    # Electric Field Intensity (Spheres)
    EFI = np.linalg.norm(EtotSI, axis=1)**2
    # Reshape the Array
    EFImap = EFI.reshape(Settings["shape"])
    
    # Electric Field Intensity (Vacuum)
    EFIdip = np.linalg.norm(Edip, axis=1)**2
    # Reshape the Array
    EFIdipmap = EFIdip.reshape(Settings["shape"])

############################################################################
############################################################################
## Plot Figures
if Settings['ModeName'] == 'wavelength':
    if Settings['Quantity'] == 'CF':
        # Your data for the first plot (I'm assuming lambda_val, CF, and CFdip are already defined)
        x_axis     = 1.0 / lambda_val * 1e-2   # wavenumber in cm^{-1}
        y_axis     = CF * 1e-12                # CF         in cm^{-6}
        y_axis_QED = CFdip * 1e-12             # CFdip      in cm^{-1}
        y_axis_EF  = EF                        # Enhancement Factor 

        # Create the first plot
        fig1, ax1 = plt.subplots()

        # Plot the CF data
        ax1.plot(x_axis, y_axis,color='k', label='CF')

        # Plot the QED data in red
        ax1.plot(x_axis, y_axis_QED, color='red', label='QED')

        # Set x and y labels
        ax1.set_xlabel(r'wavenumber cm$^{-1}$')
        ax1.set_ylabel('CF')

        # Set the y-axis to log scale
        ax1.set_yscale('log')

        # Find minimum and maximum y-values among both datasets
        y_min = min(np.min(y_axis), np.min(y_axis_QED))
        y_max = max(np.max(y_axis), np.max(y_axis_QED)) + 0.2e+33

        # Set y-axis limits based on min and max values
        ax1.set_ylim(y_min, y_max)

        # Set x-axis limits
        ax1.set_xlim(14285, 33333)

        # Add a title
        ax1.set_title('CF and QED')

        # Add a legend
        ax1.legend()

        # Show the first plot
        plt.show()

        # Create the second plot
        fig2, ax2 = plt.subplots()

        # Plot the EF data
        ax2.plot(x_axis, y_axis_EF, label='EF')

        # Set x and y labels
        ax2.set_xlabel(r'wavenumber cm$^{-1}$')
        ax2.set_ylabel('EF')

        ax2.set_yscale('log')  

        # Set new y-axis limits for EF data
        y_min_EF = np.min(y_axis_EF)
        y_max_EF = np.max(y_axis_EF) + 0.3e+2

        ax2.set_ylim(1e-3, 1e+5)

        # Set x-axis limits to be the same as the first plot
        ax2.set_xlim(14285, 33333)

        # Add a title
        ax2.set_title('EF')

        # Add a legend
        ax2.legend()

        # Show the second plot
        plt.show()
        #fig2.savefig('./EF.png', transparent=True)
    elif Settings['Quantity'] == 'Purcell':
        x_axis = 1239.84193 / (lambda_val * 1e9)
        y_axis = Purcell
        
        fig1, ax1 = plt.subplots()

        # Plot the Purcell data
        ax1.plot(x_axis, y_axis,color='k', label='Purcell')

        # Set x and y labels
        ax1.set_xlabel(r'wavenumber (cm$^{-1}$)')
        ax1.set_ylabel('Purcell Factor')

        # Set the y-axis to log scale
        ax1.set_yscale('log')

        # Find minimum and maximum y-values among both datasets
        #y_min = min(np.min(y_axis))
        #y_max = max(np.max(y_axis)) + 0.2e+33

        # Set y-axis limits based on min and max values
        ax1.set_ylim(min(y_axis), max(y_axis*1.01))

        # Set x-axis limits
        ax1.set_xlim(min(x_axis), max(x_axis))

        # Add a title
        ax1.set_title('Purcell Factor')

        # Add a legend
        ax1.legend()

        # Show the first plot
        plt.show()
    elif Settings['Quantity'] == 'ImG':
        x_axis = 1239.84193 / (lambda_val * 1e9)
        y_axis = ImG
        
        fig1, ax1 = plt.subplots()

        # Plot the Purcell data
        ax1.plot(x_axis, y_axis,color='k', label='ImG')

        # Set x and y labels
        ax1.set_xlabel(r'wavenumber (cm$^{-1}$)')
        ax1.set_ylabel('ImG')

        # Set the y-axis to log scale
        ax1.set_yscale('log')

        # Find minimum and maximum y-values among both datasets
        #y_min = min(np.min(y_axis))
        #y_max = max(np.max(y_axis)) + 0.2e+33

        # Set y-axis limits based on min and max values
        ax1.set_ylim(min(y_axis), max(y_axis*1.01))

        # Set x-axis limits
        ax1.set_xlim(min(x_axis), max(x_axis))

        # Add a title
        ax1.set_title('ImG')

        # Add a legend
        ax1.legend()

        # Show the first plot
        plt.show()
    elif Settings['Quantity'] == 'J':
        x_axis = 1239.84193 / (lambda_val * 1e9)
        y_axis = J
        
        fig1, ax1 = plt.subplots()

        # Plot the Purcell data
        ax1.plot(x_axis, y_axis,color='k', label='J')

        # Set x and y labels
        ax1.set_xlabel(r'wavenumber (cm$^{-1}$)')
        ax1.set_ylabel('J')

        # Set the y-axis to log scale
        ax1.set_yscale('log')

        # Find minimum and maximum y-values among both datasets
        #y_min = min(np.min(y_axis))
        #y_max = max(np.max(y_axis)) + 0.2e+33

        # Set y-axis limits based on min and max values
        ax1.set_ylim(min(y_axis), max(y_axis*1.01))

        # Set x-axis limits
        ax1.set_xlim(min(x_axis), max(x_axis))

        # Add a title
        ax1.set_title('J')

        # Add a legend
        ax1.legend()

        # Show the first plot
        plt.show()



'''
        if Settings['ModeName'] == 'wavelength':
            if Settings['Quantity'] == 'CF':
                fplot = {}
                fplot['x'] = 1.0 / lambda_val * 1e-2
                fplot['y'] = CF * 1e-12
                MyPlot(fplot, Resize, 0)
                
                fplot['y'] = CFdip * 1e-12
                fplot['colorstyle'] = 'r-'
                MyPlot(fplot, Resize, 1)
                
                if Settings['BC'] == 'sphere':
                    plt.legend(['Single Sphere', 'Vacuum (QED)'], loc='best')
                elif Settings['BC'] == 'coreshell':
                    plt.legend(['Core/Shell Sphere', 'Vacuum (QED)'], loc='best')
                
                fplot['y'] = EF
                fplot['colorstyle'] = '-'
                fplot['range'] = [float('-inf'), float('inf'), 1e-3, 1e5]
                fplot['ylabel'] = 'Enhancement'
                MyPlot(fplot, Resize, 0)
                
                if Settings['BC'] == 'sphere':
                    plt.legend(['Single Sphere'], loc='best')
                elif Settings['BC'] == 'coreshell':
                    plt.legend(['Core/Shell Sphere'], loc='best')
            
            elif Settings['Quantity'] == 'Purcell':
                fplot['x'] = 1239.84193 / (lambda_val * 1e9)
                fplot['y'] = Purcell
                MyPlot(fplot, Resize, 0)
            
            elif Settings['Quantity'] == 'ImG':
                fplot['x'] = 1239.84193 / (lambda_val * 1e9)
                fplot['y'] = ImG
                MyPlot(fplot, Resize, 0)
            
            elif Settings['Quantity'] == 'J':
                fplot['x'] = 1239.84193 / (lambda_val * 1e9)
                fplot['y'] = J
                MyPlot(fplot, Resize, 0)
        '''

