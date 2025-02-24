import numpy as np

def get_distance(point1, point2):
    distance = 0
    for X0, X1 in zip(point1, point2):
        distance += (X0 - X1)**2
    distance = np.sqrt(distance)
    return distance

def find_nearestgrid_2D(point, grids):
    """
    point: (x, y)\n
    grids: (X, Y)\n
    return: (ind_y, ind_x)
    """
    dis = get_distance(point, grids)
    nearind = np.argmin(dis)
    nearind_2D = (nearind//dis.shape[1], nearind%dis.shape[1])
    return nearind_2D

def mask_in_distance(xx, yy, x, y, distance):
    distance_array = get_distance((xx, yy), (x, y))
    return distance_array <= distance

def continuous_to_discrete_distance(xx, yy, mind, maxd):
    ny, nx   = xx.shape
    xind_mid = nx // 2
    yind_mid = ny // 2
    xmid     = xx[yind_mid, xind_mid]
    ymid     = yy[yind_mid, xind_mid]
    distance = get_distance((xmid, ymid), (xx, yy))
    distance = distance[np.logical_and(distance <= maxd, distance > mind)]
    distance_list = [mind]
    while distance.size > 0:
        distance_list.append(np.min(distance))
        distance = distance[distance > distance_list[-1]]
    distance_list.append(maxd)
    distance_mid = [(distance_list[i] + distance_list[i+1]) / 2 for i in range(len(distance_list) - 1)]
    return distance_list, distance_mid

def _getshift(xind, yind, xind_mid, yind_mid):
    yshift = yind - yind_mid
    xshift = xind - xind_mid
    return xshift, yshift

def _getindinmask(xshift, yshift, xind_midmask, yind_midmask, nx, ny):
    yind_mask = yind_midmask + yshift
    xind_mask = xind_midmask + xshift
    yind_mask = yind_mask[np.logical_and(xind_mask < nx, xind_mask >= 0)]
    xind_mask = xind_mask[np.logical_and(xind_mask < nx, xind_mask >= 0)]
    xind_mask = xind_mask[np.logical_and(yind_mask < ny, yind_mask >= 0)]
    yind_mask = yind_mask[np.logical_and(yind_mask < ny, yind_mask >= 0)]
    return xind_mask, yind_mask

def _getmid_midmask(xx, yy, distance):
    ny, nx = xx.shape
    xxind, yyind = np.meshgrid(np.arange(nx), np.arange(ny))
    xind_mid     = nx // 2
    yind_mid     = ny // 2
    xmid         = xx[yind_mid, xind_mid]
    ymid         = yy[yind_mid, xind_mid]
    _mask        = mask_in_distance(xx, yy, xmid, ymid, distance)
    xind_midmask = xxind[_mask]
    yind_midmask = yyind[_mask]
    return xind_mid, yind_mid, xind_midmask, yind_midmask

# xx.shape == (ny, nx)
# var.shape == (..., ny, nx)
# return mean of var within a radius of "distance" around every grid point 
def circleregion_mean(xx, yy, var, distance):
    ny, nx = xx.shape
    varshape     = var.shape
    var          = np.reshape(var, (-1, ny, nx))
    meanvar      = np.zeros_like(var)
    
    xind_mid, yind_mid, xind_midmask, yind_midmask = _getmid_midmask(xx, yy, distance)
    for yind in range(ny):
        for xind in range(nx):
            xshift, yshift         = _getshift(xind, yind, xind_mid, yind_mid)
            xind_mask, yind_mask   = _getindinmask(xshift, yshift, xind_midmask, yind_midmask, nx, ny)
            meanvar[:, yind, xind] = np.nanmean(var[:, yind_mask, xind_mask], axis=(-1))
        
    meanvar = np.reshape(meanvar, varshape)
    return meanvar

# return a array which has same shape with xx and 
# value == True if the distance between grid and (yind, xind) < "distance"
def circleregion_mask(xx, yy, xinds, yinds, distance):
     ny, nx = xx.shape
     result = np.zeros_like(xx, dtype = bool)
     xind_mid, yind_mid, xind_midmask, yind_midmask = _getmid_midmask(xx, yy, distance)
     for xind, yind in zip(xinds, yinds):
         xshift, yshift         = _getshift(xind, yind, xind_mid, yind_mid)
         xind_mask, yind_mask   = _getindinmask(xshift, yshift, xind_midmask, yind_midmask, nx, ny)
         result[yind_mask, xind_mask] = True
     return result