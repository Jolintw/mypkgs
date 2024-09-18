import abc
import numpy as np
from mypkgs.processor.gridmethod import get_distance

class ConnectedGrids_2D:
    """
    get_indexarray(): (y_index_array, x_index_array)\n
    get_boolarray(shape)

    """
    count = 0
    def __init__(self):
        self.y = np.array([], dtype=int)
        self.xl = np.array([], dtype=int)
        self.xr = np.array([], dtype=int)
        self._serial_number = self.count
        ConnectedGrids_2D.count += 1

    def get_indexarray(self):
        """
        return (y_index_array, x_index_array)
        """
        if hasattr(self, "indexarray"):
            return self.indexarray
        else:
            gridnumber = self.grids_number()
            x, y = np.zeros(gridnumber, dtype=int), np.zeros(gridnumber, dtype=int)
            i = 0
            for y_iter, (xl_iter, xr_iter) in zip(self.y, zip(self.xl, self.xr)):
                length = xr_iter - xl_iter + 1
                y[i:i+length] = y_iter
                x[i:i+length] = np.arange(xl_iter, xr_iter+1, dtype=int)
                i = i + length
            self.indexarray = (y, x)
        return self.indexarray
    
    def get_boolarray(self, shape):
        """
        return boolean array with **shape**
        """
        boolarray = np.zeros(shape, dtype=bool)
        boolarray[self.get_index_array()] = True
        return boolarray
    
    def get_boundary(self):
        """
        return (x0, x1, y0, y1)
        """
        CGindexarray = self.get_indexarray()
        left_boundary = np.min(CGindexarray[1])
        right_boundary = np.max(CGindexarray[1])
        under_boundary = np.min(CGindexarray[0])
        upper_boundary = np.max(CGindexarray[0])
        return (left_boundary, right_boundary, under_boundary, upper_boundary)

    def grids_number(self):
        """
        return the area(number) of connected grids
        """
        return np.sum(self.xr - self.xl + 1, dtype=int)
    
    def add_connectedline(self, y, xl, xr):
        self.y = np.append(self.y, y)
        self.xl = np.append(self.xl, xl)
        self.xr = np.append(self.xr, xr)

    def merge(self, another_CG):
        """
        merge with another connected grids
        """
        if another_CG.serial_number() == self.serial_number():
            pass
        else:
            self.add_connectedline(y=another_CG.y, xl=another_CG.xl, xr=another_CG.xr)

    def serial_number(self):
        return self._serial_number
    
class ConnectedGridsController(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def find_connectedgrids(self):
        return NotImplemented
    
    @abc.abstractmethod
    def get_numberarray(self):
        if hasattr(self, "numberarray"):
            return self.numberarray
        else:
            return self.make_numberarray()
    
    @abc.abstractmethod
    def make_numberarray(self):
        return NotImplemented

    @abc.abstractmethod
    def find_CGnumbers_from_ind(self, ind):
        """
        give index of grids and get the index of CG
        """
        return NotImplemented

class ConnectedGridsController_1D(ConnectedGridsController):
    def __init__(self, boolarray):
        self.boolarray = boolarray
        self.find_connectedgrids()

    def find_connectedgrids(self):
        boolarray = self.boolarray.astype(int)
        boolarray = np.append(boolarray, [0])
        boolarray = np.append([0], boolarray)
        diff = boolarray[1:] - boolarray[:-1]
        indarray = np.arange(diff.shape[0], dtype=int)
        self.xl = indarray[diff==1]
        self.xr = indarray[diff==-1] - 1
        self.CGnumbers = np.arange(self.xr.shape[0], dtype=int)
        
    def get_numberarray(self):
        return super().get_numberarray()
        
    def make_numberarray(self):
        numberarray = np.zeros_like(self.boolarray, dtype=int) - 1
        xl = self.xl
        xr = self.xr
        for i in self.CGnumbers:
            numberarray[xl[i]:xr[i]+1] = i
        self.numberarray = numberarray
        return numberarray
    
    def find_CGnumbers_from_ind(self, ind):
        return self.get_numberarray()[ind]

class ConnectedGridsController_2D(ConnectedGridsController):
    def __init__(self, boolarray):
        self.boolarray = boolarray
        self.find_connectedgrids()

    def find_connectedgrids(self):
        self._declarate_CGlists()
        self._create_new_CGs(y=0)
        self._prepareto_moveindex()

        for i_y in range(1, self.boolarray.shape[0]):
            self._create_new_CGs(y=i_y)
            self._merge_connectedCGs()
            self._prepareto_moveindex()
        self._prepareto_moveindex()
        self.CGlist = self._CGconfirmedlist
        self.CGnumbers = np.arange(len(self.CGlist))

    def get_numberarray(self):
        return super().get_numberarray()
        
    def make_numberarray(self):
        numberarray = np.zeros_like(self.boolarray, dtype=int) - 1
        for i_CG, CG in enumerate(self.CGlist):
            numberarray[CG.get_indexarray()] = i_CG
        return numberarray
    
    def find_CGnumbers_from_ind(self, ind):
        return self.get_numberarray()[ind]
    
    def find_CG_from_ind(self, ind):
        """
        give index of grids and get the CG
        """
        return self.CGlist[self.find_CGnumbers_from_ind(ind)]
    
    def find_CG_from_nearpoint(self, point, grid):
        """
        point: (x, y) x and y should be a number
        grid: (X, Y) and Y.shape == X.shape == boolarray.shape
        """
        mindis = np.inf
        for CG in self.CGlist:
            X = np.mean(grid[0][CG.get_indexarray()])
            Y = np.mean(grid[1][CG.get_indexarray()])
            dis = get_distance((X, Y), point)
            if dis < mindis:
                nearpoint_CG = CG
                mindis = dis
        return nearpoint_CG

    def _declarate_CGlists(self):
        self._CGnowlist = []
        self._CGnextlist = []
        self._CGconfirmedlist = []

    def _create_new_CGs(self, y):
        self._CGCnext = ConnectedGridsController_1D(self.boolarray[y])
        for xl, xr in zip(self._CGCnext.xl, self._CGCnext.xr):
            self._CGnextlist.append(ConnectedGrids_2D())
            self._CGnextlist[-1].add_connectedline(y, xl, xr)

    def _merge_connectedCGs(self):
        CGnowlist = self._CGnowlist
        CGnextlist = self._CGnextlist
        CGnow_serialnumber = np.array([CG.serial_number() for CG in CGnowlist])
        CGnext_serialnumber = np.array([CG.serial_number() for CG in CGnextlist])
        CGCnow = self._CGCnow
        CGCnext = self._CGCnext
        CGCdiff = ConnectedGridsController_1D(np.logical_and(CGCnow.boolarray, CGCnext.boolarray))
        CGnumbernow_tomerge = CGCnow.find_CGnumbers_from_ind(CGCdiff.xl)
        CGnumbernext_tomerge = CGCnext.find_CGnumbers_from_ind(CGCdiff.xl)
        for numnow, numnext in zip(CGnumbernow_tomerge, CGnumbernext_tomerge):
            baseCG, mergedCG     = CGnowlist[numnow], CGnextlist[numnext]
            baseCGsn, mergedCGsn = baseCG.serial_number(), mergedCG.serial_number()
            baseCG.merge(mergedCG)
            mergedCGnumbernow  = np.arange(CGnow_serialnumber.shape[0], dtype=int)[CGnow_serialnumber==mergedCGsn]
            mergedCGnumbernext = np.arange(CGnext_serialnumber.shape[0], dtype=int)[CGnext_serialnumber==mergedCGsn]
            CGnow_serialnumber[CGnow_serialnumber==mergedCGsn]   = baseCGsn
            CGnext_serialnumber[CGnext_serialnumber==mergedCGsn] = baseCGsn
            for mergednumber in mergedCGnumbernow:
                CGnowlist[mergednumber] = baseCG
            for mergednumber in mergedCGnumbernext:
                CGnextlist[mergednumber] = baseCG

    def _prepareto_moveindex(self):
        self._add_confirmedCG()
        self._CGnowlist = self._CGnextlist
        self._CGCnow    = self._CGCnext
        self._CGnextlist = []

    def _add_confirmedCG(self):
        for CG in self._CGnowlist:
            if (not CG in self._CGnextlist) and (not CG in self._CGconfirmedlist):
                self._CGconfirmedlist.append(CG)