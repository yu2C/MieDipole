import scipy.io as sio
import numpy as np

#save
array_x = np.array([1,2,3,4])
array_y = np.array([5,6,7,8])
sio.savemat('./save.mat', {'arrayX': array_x, 'arrayY': array_y})