import numpy
from numpy import fromfile, zeros, mean, shape, flip


#DEFINING FUNCTIONS
# the authot of the BBXimportNorm function is Johannes Förster (Max Planck Institute for Intelligent Systems, Stuttgart, Germany)
def BBXimportNorm(M, path): #exporting dynamic magnetic contrast
    with open(path, 'rb') as f:    
        a = fromfile(f, dtype = '>u4')   
    N = a[0]
    Y = a[2]
    X = a[1]
    Bild = zeros([Y, X, N])
    for k in range(0, N): 
        for i in range(0, Y):
            for j in range(0, X):
                Bild[i, j, k * M % N]=a[3 + i + Y * j + Y * X * k]
    
    Normbild = zeros(shape(Bild))
    S = mean(Bild, axis=2)
    for i in range(0, N):
        Normbild[:, :, i] = flip(Bild[:, :, i] / S, axis = 0)
    del(Bild)
    return Normbild, N
    
def BBXimport(M, path): #exporting the chemical contrast
    with open(path, 'rb') as f:    
        a = fromfile(f, dtype = '>u4')   
    N = a[0]
    Y = a[2]
    X = a[1]
    Bild = zeros([Y, X, N])
    for k in range(0, N): 
        for i in range(0, Y):
            for j in range(0, X):
                Bild[i, j, k * M % N] = a[3 + i + Y * j + Y * X * k]
    
    Normbild = zeros(shape(Bild))
    S = mean(Bild, axis=2)
    for i in range(0, N):
        Normbild[:, :, i] = flip(Bild[:, :, i], axis = 0)
    del(Bild)
    return Normbild, N