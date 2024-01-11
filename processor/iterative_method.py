# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

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