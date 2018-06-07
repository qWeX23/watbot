import os
import numpy as np

def das_v0(data_dir, width=48, height=27):
    X = np.load(os.path.join(data_dir, 'imgs_%dw_%dh.npy'%(width, height)))
    Y = np.load(os.path.join(data_dir, 'labels_%dw_%dh.npy'%(width, height)))
    return X, Y

def das_v2(data_dir, width=48, height=27):
    X = np.load(os.path.join(data_dir, 'imgs_%dw_%dh_test.npy'%(width, height)))
    Y = np.load(os.path.join(data_dir, 'labels_%dw_%dh_test.npy'%(width, height)))
    return X, Y
