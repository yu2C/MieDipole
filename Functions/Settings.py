import numpy as np
import scipy.io as sio

{
    "Settings" : {
        "ModeName"   : "wavelength",
        "Quantity"   : "CF",
        "BC"         : "sphere",
        "nmax"	     : 1,
        "nr"         : np.array([1,	0.0506194160110720 + 2.17040801055408j], dtype=np.complex128),
        "k0"         : 1.551403779550515e+07,
        "k0s"        : np.array([1.0859826456853604]) ,
        "DPos"	     : {
            "Cart"   : np.array([[0],
                                [0],
                                [80e-9]
                                ]),
            "Sph"    : np.array([[8.e-08],
                                [0.e+00],
                                [0.e+00]])
        },
        "APos"	     : {
            "Cart"   : np.array([[0],
                                [0],
                                [80e-9]]),
            "Sph"    : np.array([[8.00000000e-08],
                                [3.14159265e+00],
                                [0.00000000e+00]]),
            "Sph2"   : np.array([[1.60000000e-07],
                                [3.14159265e+00],
                                [0.00000000e+00]]),
        },
        "DOri"	     : {
            "Cart"   : np.array([[0],
                                [0],
                                [1]]),
            "Sph"    : np.array([[1],
                                [0],
                                [0]])
        },
        "AOri"	     : {
            "Cart"   : np.array([[0],
                                [0],
                                [1]]),
            
        },
        "rbc"		 : 7.0e-8,
        "Dpstrength" : 1,
        "DNAng"      :{
            "NPi"    : np.array([[-0.61237244,  0.       , -0.61237244]]), 
            "NTau"   : np.array([[-0.61237244,  0.       ,  0.61237244]]), 
            "NP"     : np.array([[0.         ,  0.8660254,  0.        ]])
        },
        "DRad"       : {
            "h1"     : np.array([0.32106156-1.20987784j], dtype=np.complex128), 
            "xi"     : np.array([0.34866729-1.31390633j], dtype=np.complex128), 
            "dxi"    : np.array([0.56370023+0.74383432j], dtype=np.complex128), 
            "raddxi" : np.array([0.51906928+0.68494126j], dtype=np.complex128)
        },
        "EdipS2"     : np.array([[-3.56558893e+20-1.25710431e+21j],
                                [ 4.90815938e+12-1.05171161e+12j],
                                [ 0.00000000e+00+0.00000000e+00j]], dtype=np.complex128),
        "EdipS1"     : np.array([[-3.56558893e+20-1.25710431e+21j],
                                [ 4.90815938e+12-1.05171161e+12j],
                                [ 0.00000000e+00+0.00000000e+00j]], dtype=np.complex128),
        }, 


    "tmp_set"  : {
        "mode"	   : "Auto",
        "lambda_s"   : 300e-9,
        "lambda_e"   : 700e-9,
        "epsi0"	   : 1,
        "epsi1"	   : 4,
        "epsi2"	   : ".\\InputFiles\\DielectricFunctions\\Ag_JPCL.csv"
        },
    
    "fplot"	   : {
        "colorstyle" : "-k",
        "range" 	   : [1],
        "yscale"     : "log",
        "xlabel"	   : "$\\mathrm{Wavenumber}~(\\mathrm{cm}^{-1})$",
        "ylabel"	   : "$\\mathrm{Coupling~Factor}~(\\mathrm{cm}^{-6})$",
        "subaxis"    : 1,
        "subrange"   : [1],
        "subxlabel"  : "$\\mathrm{Wavelength}~(\\mathrm{nm})$"
        }	 

}
    
   


#sio.savemat('./Settings.mat', mdict=Settings)

#print(Settings["APos"])
#print(Settings["DRad"])
'''
import numpy as np
# Transforming Coordinate
Settings1.Settings1['DPos']['Sph'] = C2S.C2S(Settings1.Settings1['DPos']['Cart'])
Settings1.Settings1['DOri']['Sph'] = VecTrans.VecTrans(Settings1.Settings1['DOri']['Cart'], Settings1.Settings1['DPos']['Sph'][1:3], 'C2S')

    # Times of the 'for loop'
Settings1.Settings1['nn'] = Settings1.Settings1['nr'].shape[0]

# Coordinate Transformation
Settings1.Settings1['APos']['Sph'] = C2S.C2S(Settings1.Settings1['APos']['Cart'])
Settings1.Settings1['AOri']['Sph'] = VecTrans.VecTrans(Settings1.Settings1['AOri']['Cart'], Settings1.Settings1['APos']['Sph'][1:3], 'C2S')
Settings1.Settings1['APos']['Sph2'] = C2S.C2S(Settings1.Settings1['APos']['Cart'] - Settings1.Settings1['DPos']['Cart'])

# Angular Functions
Settings1.Settings1['DNAng'] = NormTauPiP.NormTauPiP(Settings1.Settings1['nmax'], Settings1.Settings1['DPos']['Sph'][1], 'reversed')
Settings1.Settings1['ANAng'] = NormTauPiP.NormTauPiP(Settings1.Settings1['nmax'], Settings1.Settings1['APos']['Sph'][1], 'normal')
'''


