# -*- coding: utf-8 -*-
import numpy as np
from mypkgs.processor.numericalmethod import central_diff
from mypkgs.processor.array_process import broadcast_to_any
from mypkgs.processor.gridmethod    import circleregion_mean
from mypkgs.processor.iterative_method import poisson_eq_relaxation

# not completed
def vertical_vorticity_budget(x, y, z, u, v, w, lat, vor = None, div = None):
    shape = u.shape
    X = [z, y, x]
    X = [broadcast_to_any(X[i], shape, n = i) for i in range(3)]
    U = [w, v, u]
    
        
    f = 2 * 2 * np.pi / 86400 * np.sin(lat / 180 * np.pi)
    if not type(f) is float:
        if len(f.shape) <= 2:
            f = broadcast_to_any(f, shape, n = 1)
    if vor is None:
        vor = - central_diff(U[2],X[1],n=1) + central_diff(U[1],X[2],n=2)
    if div is None:
        div = central_diff(U[1],X[1],n=1) + central_diff(U[2],X[2],n=2)
    
    ADV = [- U[i] * central_diff(vor,X[i],n=i) for i in range(3)]
    STR = - (f + vor)*div
    TLT = - (central_diff(U[0],X[2],n=2) * central_diff(U[1],X[0],n=0) - central_diff(U[0],X[1],n=1) * central_diff(U[2],X[0],n=0))
    HAD = ADV[1] + ADV[2]
    VAD = ADV[0]
    
    return HAD, VAD, STR, TLT

# xx: (nx) or (ny, nx)
# vor: (..., ny, nx)
def rotational_wind(xx, yy, vor):
    if len(xx.shape) == 1 and len(yy.shape) == 1:
        xx, yy = np.meshgrid(xx, yy)
    ori_shape = vor.shape
    vor = np.reshape(vor, (-1, *xx.shape))
    if isinstance(vor,np.ma.core.MaskedArray):
        temp = vor.mask
        vor = vor.data
        vor[temp] = np.nan
    vor = fillNAN(xx, yy, vor)
    result = np.zeros_like(vor)
    for i in range(vor.shape[0]):
        if np.any(np.isnan(vor[i])):
            result[i,...] = np.nan
            continue
        result[i] = poisson_eq_relaxation(vor[i], dx = np.abs(np.mean(xx[:,1:]-xx[:,:-1])), tol_value = 1e-6)
    result = np.reshape(result, ori_shape)
    result = {"psi":result, "u":-central_diff(result, yy[:,0], n=-2, broadX=True), "v":central_diff(result, xx[0,:], n=-1, broadX=True)}
    for k in result:
        result[k][0,:]  = np.nan
        result[k][-1,:] = np.nan
        result[k][:,0]  = np.nan
        result[k][:,-1] = np.nan
    return result

def fillNAN(xx, yy, vor):
    meanvor = circleregion_mean(xx, yy, vor, distance = 5e3)
    vor[np.isnan(vor)] = meanvor[np.isnan(vor)]
    return vor