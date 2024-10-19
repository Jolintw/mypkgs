# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from mypkgs.processor.numericalmethod import central_diff

# boundary: zero gradient
def poisson_eq_relaxation(var, dx, tol_value = 1e-4):
    #plt.pcolormesh(var)
    #plt.show()
    extented_psi = np.zeros((var.shape[0]+2, var.shape[1]+2))
    diff = 9999
    i = 0
    while diff > tol_value:
        if i%50000 == 0 and i > 0:
            print(i, diff)
        #extented_psi[0, :]  = extented_psi[1, :]
        #extented_psi[-1, :] = extented_psi[-2, :]
        #extented_psi[:, 0]  = extented_psi[:, 1]
        #extented_psi[:, -1] = extented_psi[:, -2]
        psi  = (extented_psi[:-2,1:-1] + extented_psi[2:,1:-1] + extented_psi[1:-1,:-2] + extented_psi[1:-1,2:] - dx**2 * var) / 4
        diff = np.max(np.abs(extented_psi[1:-1, 1:-1] - psi))
        extented_psi[1:-1, 1:-1] = psi
        i += 1
    check = (extented_psi[:-2,1:-1] + extented_psi[2:,1:-1] + extented_psi[1:-1,:-2] + extented_psi[1:-1,2:]  - 4 * psi) / dx**2
    #plt.pcolormesh(check)
    #plt.show()
    #plt.pcolormesh(psi)
    #plt.show()
    return psi

def poisson_eq_relaxation_withnan(var, dx, tol_value = 1e-4):
    extented_psi = np.zeros((var.shape[0]+2, var.shape[1]+2))
    nanmask = np.isnan(var)
    diff = 9999
    i = 0
    while diff > tol_value:
        if i%500 == 0 and i > 0:
            print(i, diff)
        psi  = (extented_psi[:-2,1:-1] + extented_psi[2:,1:-1] + extented_psi[1:-1,:-2] + extented_psi[1:-1,2:] - dx**2 * var) / 4
        psi[nanmask] = 0
        diff = np.max(np.abs(extented_psi[1:-1, 1:-1] - psi))
        extented_psi[1:-1, 1:-1] = psi
        i += 1
    psi[nanmask] = np.nan
    return psi


def gradient_inversion_leastRMSEmethod(dvardx, dvardy, deltax, zeropoint, alpha = 0.1, tol_value = 1e-4):
    """
    assume deltax = deltay
    """
    var = np.zeros_like(dvardx)
    dvar = (dvardx[:,1:] + dvardx[:,:-1]) / 2.0 * deltax
    dvar = np.cumsum(-dvar[:, ::-1], axis=1)
    var[:, :-1] += dvar[:, ::-1]
    dvar = (dvardy[1:,:] + dvardy[:-1,:]) / 2.0 * deltax
    dvar = np.cumsum(dvar, axis=0)
    var[1:, :] += dvar
    var = var - np.nanmean(var)
    extented_ex  = np.zeros((var.shape[0]+2, var.shape[1]+2))
    extented_ey  = np.zeros((var.shape[0]+2, var.shape[1]+2))
    extented_var = np.zeros((var.shape[0]+2, var.shape[1]+2))
    # extented_dvardy = np.zeros((var.shape[0]+2, var.shape[1]+2))
    # extented_dvardy[1:-1, 1:-1] = dvardy
    # extented_dvardx = np.zeros((var.shape[0]+2, var.shape[1]+2))
    # extented_dvardx[1:-1, 1:-1] = dvardx
    def zerogradient_boundary_condition(var, extented_var):
        extented_var[1:-1, 1:-1] = var
        extented_var[0, 1:-1]  = var[0,:]
        extented_var[-1, 1:-1] = var[-1,:]
        extented_var[1:-1, 0]  = var[:,0]
        extented_var[1:-1, -1] = var[:,-1]
        return extented_var
    extented_var = zerogradient_boundary_condition(var, extented_var)
    nanmask = np.logical_and(np.isnan(dvardx), np.isnan(dvardy))
    diff = 9999
    loss = 9999999
    i = 0
    extented_ey[1:-1, 1:-1] = (extented_var[2:, 1:-1] - extented_var[:-2, 1:-1]) / 2  - dvardy*deltax
    extented_ex[1:-1, 1:-1] = (extented_var[1:-1, 2:] - extented_var[1:-1, :-2]) / 2  - dvardx*deltax
    while loss > 10 and diff > 0:
        if i%1000 == 0 and i > 0:
            diff = loss - nextloss
            loss = nextloss
            print(i, loss)
        esum = np.nansum([extented_ey[:-2, 1:-1], -extented_ey[2:, 1:-1], extented_ey[1:-1, :-2], -extented_ey[1:-1, 2:]], axis=0)
        deltavar = -alpha*esum*np.random.rand(*esum.shape)
        var = var + deltavar
        # var[zeropoint] = 0
        extented_var = zerogradient_boundary_condition(var, extented_var)
        extented_ey[1:-1, 1:-1] = (extented_var[2:, 1:-1] - extented_var[:-2, 1:-1]) / 2 - dvardy*deltax
        extented_ex[1:-1, 1:-1] = (extented_var[1:-1, 2:] - extented_var[1:-1, :-2]) / 2 - dvardx*deltax
        nextloss = np.nansum(np.array([np.power(extented_ey[1:-1, 1:-1], 2), np.power(extented_ex[1:-1, 1:-1], 2)]))
        # diff = loss - nextloss
        
        i += 1
    var[nanmask] = np.nan
    return var


"""    
if __name__ == '__main__':
    a = 1e6
    b = 1e6
    x = np.linspace(-2e6, 2e6, 301)
    y = np.linspace(-2e6, 2e6, 301)
    dx = abs(x[1] - x[0])
    xx, yy = np.meshgrid(x, y)
    vor = 1e-3 * np.exp(-(4*(xx/a)**2+(yy/b)**2))
    psi = poisson_eq_relaxation(vor, dx, tol_value = 1e-3)
    plt.pcolormesh(xx, yy, psi)
"""