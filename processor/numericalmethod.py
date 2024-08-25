# -*- coding: utf-8 -*-
import numpy as np

def central_diff(Y,X,n=0,broadX=False,cyclic=False): #partial Y/partial X
    Ys = np.swapaxes(Y,0,n)
    Yshape = np.shape(Ys)
    Ys = np.reshape(Ys,(Yshape[0],-1))
    if broadX:
        Xs = np.swapaxes(np.broadcast_to(X,(np.shape(Ys)[1],np.shape(Ys)[0])),0,1)
    else:
        Xs = np.swapaxes(X,0,n)
        Xs = np.reshape(Xs,(Yshape[0],-1))
    
    dY = Ys[2:,:] - Ys[:-2,:]
    dX = Xs[2:,:] - Xs[:-2,:]
    
    re = np.zeros_like(Ys)
    if cyclic:
        re[0,:] = (Ys[1,:] - Ys[-1,:])/dX[0]
        re[-1,:] = (Ys[0,:] - Ys[-2,:])/dX[0]
    else:
        re[0,:] = (Ys[1,:] - Ys[0,:])/(Xs[1,:] - Xs[0,:])
        re[-1,:] = (Ys[-1,:] - Ys[-2,:])/(Xs[-1,:] - Xs[-2,:])
    
    re[1:-1,:] = dY/dX
    
    re = np.reshape(re,Yshape)
    re = np.swapaxes(re,0,n)
    return re

def central_diff_4thorder(Y,X,n=0,broadX=False,cyclic=False): #partial Y/partial X
    Ys = np.swapaxes(Y,0,n)
    Yshape = np.shape(Ys)
    Ys = np.reshape(Ys,(Yshape[0],-1))
    if broadX:
        Xs = np.swapaxes(np.broadcast_to(X,(np.shape(Ys)[1],np.shape(Ys)[0])),0,1)
    else:
        Xs = np.swapaxes(X,0,n)
        Xs = np.reshape(Xs,(Yshape[0],-1))
    
    dY = (Ys[3:-1,:] - Ys[1:-3,:])*2/3 - (Ys[4:,:] - Ys[:-4,:])/12
    dX = Xs[1:,:] - Xs[:-1,:]
    
    re = np.zeros_like(Ys)
    if cyclic:
        Ytemp = np.roll(Ys,2,axis=0)
        re[:2,:] = ((Ytemp[3:5,:] - Ytemp[1:3,:])*2/3 - (Ytemp[4:6,:] - Ytemp[0:2,:])/12)/dX[0]
        Ytemp = np.roll(Ys,-2,axis=0)
        re[-2:,:] = ((Ytemp[-3:-1,:] - Ytemp[-5:-3,:])*2/3 - (Ytemp[-2:,:] - Ytemp[-6:-4,:])/12)/dX[0]
    else:
        re[0,:] = (Ys[1,:]*2 - Ys[0,:]*3/2 - Ys[2,:]/2)/dX[0]
        re[1,:] = (Ys[2,:] - Ys[0,:])/2/dX[0]
        re[-1,:] = (-Ys[-2,:]*2 + Ys[-1,:]*3/2 + Ys[-3,:]/2)/dX[0]
        re[-2,:] = (Ys[-1,:] - Ys[-3,:])/2/dX[0]
    
    re[2:-2,:] = dY/dX[0]
    
    re = np.reshape(re,Yshape)
    re = np.swapaxes(re,0,n)
    return re

# n > 0
def movingaverage(var, n = 3, axis = 0):
    var   = np.swapaxes(var,0,axis)
    zeros = np.zeros(shape = (1,*var.shape[1:]))
    acc_var = np.append(zeros, np.nancumsum(var, axis = 0), axis = 0)
    result = (acc_var[n:, ...] - acc_var[:-n, ...]) / n
    result = np.swapaxes(result, 0, axis)
    return result
    
    
class RightAngleInterpolater:
    """
    X: a tuple containing positions of every corrdinate. X = (x1, x2) x1.shape = (n1,) # usually it will be X = (y, x)
    X can be x1 or (x1, x2, x3, ...)
    newX: new coordinates newX = (nx1, nx2) # shape of nx1 can be any just make sure nx1.shape == nx2.shape and len(X) == len(newX)
    equidistance: if value in X is equidistance
    newX_out_of_X: if True, won't print warning about newX out of X's range. And when interpolate the outer part will be filled with nan  
    var: var.shape == (..., n1, n2)
    """
    newXnotarray = False
    def __init__(self, X, newX, equidistance = True, newX_out_of_X = False):
        self.newX_out_of_X = newX_out_of_X
        if isinstance(X, np.ndarray):
            X = (X, )
            newX = (newX, )
        if not isinstance(newX[0], np.ndarray):
            self.newXnotarray = True
            newX = [np.array([x]) for x in newX]
        rsnewX = tuple([np.reshape(nX, (-1)) for nX in newX])
        Xshape = tuple([x.shape[0] for x in X])
        self.X = X
        self.Xshape             = Xshape
        self.original_newX      = newX
        self.original_newXshape = newX[0].shape
        self.newX       = rsnewX
        self.newXlen    = rsnewX[0].shape[0]
        self.equidistance       = equidistance
        self._Xcheck()
        self._indmatch()
        self._distanceandratio()
        
        
    def interpolate(self, var):
        """
        var: var.shape == (..., n1, n2)
        return: array has same shape with newX
        """
        self._inputcheck(var)
        varshape = var.shape
        var = np.reshape(var, (-1, *self.Xshape))
        
        var_on_point = self._get_var_on_point(var)
        newvar       = self._compute_interpolation(var_on_point)
    
        newvar = np.reshape(newvar, (*varshape[:-len(self.X)], *self.original_newXshape))
        if self.newX_out_of_X:
            newvar[self.outer_mask] = np.nan
        if self.newXnotarray:
            newvar = newvar[0]
        return newvar
    # newvar = var[ind+1]*ratio1 + var[ind+0]*ratio0
    # ratio0 = (X[ind+1] - newX) / (X[ind+1] - X[ind+0])
    # linear interpolation
    def _indmatch(self):
        X = self.X
        newX = self.newX
        if self.equidistance:
            Xdiff   = [np.mean(x[1:]-x[:-1]) for x in X]    
            X0      = [x[0] for x in X]
            newXind = [np.floor((_newX - _X0) / _Xdiff).astype(int) for _newX, _X0, _Xdiff in zip(newX, X0, Xdiff)]
        else:
            newXind = []
            for _newX, _X in zip(newX, X):
                ifincrease = _X[-1] > _X[0]
                ind = np.zeros_like(_newX).astype(int)
                if ifincrease:
                    for i_x, x in enumerate(_X):
                        ind[_newX > x] = i_x
                else:
                    for i_x, x in enumerate(_X):
                        ind[_newX < x] = i_x
                newXind.append(np.copy(ind))
        self.newXind = tuple(newXind)
    
    def _distanceandratio(self):
        ratio = []
        for _X, _newX, _ind in zip(self.X, self.newX, self.newXind):
            diff = _X[_ind + 1] - _X[_ind]
            distance_to_next     = _X[_ind + 1] - _newX
            distance_to_previous = _newX - _X[_ind]
            ratio_next_var       = distance_to_previous / diff
            ratio_previous_var   = distance_to_next / diff
            ratio.append((ratio_previous_var, ratio_next_var))
        self.ratio     = tuple(ratio)
    
    # example for X dimension is 2:
    # var_on_point[0] = var[dim0ind, ind0 + 0, ind1 + 0]
    # var_on_point[1] = var[dim0ind, ind0 + 1, ind1 + 0]
    # var_on_point[2] = var[dim0ind, ind0 + 0, ind1 + 1]
    # var_on_point[3] = var[dim0ind, ind0 + 1, ind1 + 1]
    def _get_var_on_point(self, var):
        varlen = var.shape[0]
        dim0ind = np.arange(varlen)
        dim0ind = np.broadcast_to(dim0ind, (self.newXlen, varlen)).T
        
        dimn = len(self.X)
        
        point_list = [[dim0ind] for i in range(2**dimn)] # need 2**n point for n dimension interpolation
        for i_ind, ind in enumerate(self.newXind):
            divisor = 2**i_ind
            for i_point, point in enumerate(point_list):
                plus = i_point // divisor % 2
                point.append(ind + plus)
        
        var_on_point = [var[tuple(point)] for point in point_list]
        return var_on_point
    
    # first average (var_on_point[0], var_on_point[1]) and (var_on_point[2], var_on_point[3])
    # with the weight of ratio
    def _compute_interpolation(self, var_on_point):
        dimn = len(self.X)
        for i_ratio, ratio in enumerate(self.ratio):
            n_group = 2**dimn // (2**i_ratio) // 2
            templist = []
            for i_group in range(n_group):
                templist.append(var_on_point[i_group*2] * ratio[0] + var_on_point[i_group*2 + 1] * ratio[1])
            var_on_point = templist
        newvar = var_on_point[0]
        return newvar
        
    def _inputcheck(self, var):
        X = self.X
        for i in range(len(X)):
            ind = -i - 1
            if not var.shape[ind] == X[ind].shape[0]:
                print("dimension is not match between var and X, last {:d} dim of var should be equal to X".format(len(self.X)))
                break
    
    def _Xcheck(self):
        X = self.X
        newX = self.newX
        for i in range(len(X)):
            if self.newX_out_of_X:
                masks = []
                masks.append(np.logical_or(newX[i] > np.max(X[i]), newX[i] < np.min(X[i])))
                if i == len(X)-1:
                    outer_mask = masks[0].copy()
                    for mask in masks:
                        outer_mask = np.logical_or(outer_mask, mask)
                    self.outer_mask = outer_mask
                continue
            if np.max(newX[i]) > np.max(X[i]) or np.min(newX[i]) < np.min(X[i]):
                print("newX is out of the range of X")
                print("newX:", "min:", np.min(newX[i]), "max:", np.max(newX[i]))
                print("X:", "min:", np.min(X[i]), "max:", np.max(X[i]))
                break

class NonEquidistanceSmoother_1D:
    def __init__(self, X, smoothrange):
        self.X = X
        self.smoothrange = smoothrange
        self._create_smoothmasklist()

    def _create_smoothmasklist(self):
        X = self.X
        smoothrange = self.smoothrange
        halfrange = smoothrange / 2
        Xmin = np.min(X)
        Xmax = np.max(X)
        smoothmasklist = []
        for x in X:
            smoothmask = np.logical_and(X >= x - halfrange, X <= x + halfrange)
            # if x == Xmin or x == Xmax:
            #     smoothmask = (x == X)
            # else:
            #     if x < Xmin + halfrange:
            #         exact_range = x - Xmin
            #     elif x > Xmax - halfrange:
            #         exact_range = Xmax - x
            #     else:
            #         exact_range = halfrange
            #     smoothmask = np.logical_and(X >= x - exact_range, X <= x + exact_range)
            smoothmasklist.append(smoothmask)
        self.smoothmasklist = smoothmasklist

    def smooth(self, var):
        newvar = np.zeros_like(var)
        for i, smoothmask in enumerate(self.smoothmasklist):
            newvar[i] = np.nanmean(var[smoothmask])
        return newvar
    
