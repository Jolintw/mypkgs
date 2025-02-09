import warnings

import numpy as np

class Variable:
    def __init__(self, name, data, dim = None, attr = {}):
        """ data: array like data
        dim: tuple with dimensions name (dim_name1, dim_name2)
        attr: attributes dict
        """
        self.name = name
        self.data = data
        self.dim = tuple(dim)
        self.attr = {}
        self.__originkeys = list(self.__dict__.keys())
        self.setattrs(attr)
        
    def __getitem__(self, *key):
        return self.data[key]
    
    def __setitem__(self, key, value):
        self.data[key] = value

    def __str__(self):
        result = "<class databox.Variable>\n"
        result += "{:s}{:s}\n".format(self.name, str(self.dim))
        for key, value in self.attr.items():
            result += "    {:s}: {:s}\n".format(key, str(value))
        return result
    
    def __repr__(self):
        result = "{:s}{:s}".format(self.name, str(self.dim))
        return result
    
    def append(self, newdata, axis = None, newdimname = "NOT_DEFINED"):
        nowshape = self.data.shape
        newshape = newdata.shape
        if axis is None:
            if newshape == nowshape:
                if not len(newshape) == len(nowshape):
                    raise Exception("need specified axis if numbers of dimensions are not the same")
                for axis in range(len(nowshape)):
                    if nowshape[axis] == 1:
                        self.data = self.data.append(self.data, newdata, axis=axis)
                axis = "new"
            else:
                for axis in range(len(nowshape)):
                    if not nowshape[axis] == newshape[axis]:
                        self.data = self.data.append(self.data, newdata, axis=axis)
                        return None
        
        if axis == "new":
            self.data = self.data.append(self.data[np.newaxis, ...], newdata[np.newaxis, ...], axis=0)
            self.dim = tuple([newdimname] + list(self.dim))
        elif isinstance(axis, int):
            if not len(newshape) == len(nowshape): # add newaxis to 
                list(newshape).insert(axis, 1)
                newshape = tuple(newshape)
                newdata  = newdata.reshape(newshape)
            self.data = self.data.append(self.data, newdata, axis=axis)

    def setattrs(self, attr):
        for key, value in attr.items():
            self.attr[key] = value
            if isinstance(key, str):
                if key in self.__originkeys:
                    warnings.warn("\"{:s}\" is protected, so it will be skip".format(key))
                    continue
            setattr(self, key, value)

class Dimension(Variable):
    def __init__(self, name, data_or_length, attr = {}):
        self._auto_setdata(data_or_length)
        super().__init__(name, self.data, (name, ), attr)

    def __str__(self):
        result = "<class databox.Dimension>\n"
        result += "{:s}{:s}\n".format(self.name, str(self.data.shape))
        for key, value in self.attr.items():
            result += "    {:s}: {:s}\n".format(key, str(value))
        return result
    
    def __repr__(self):
        result = "{:s}{:s}".format(self.name, str(self.data.shape))
        return result

    def _auto_setdata(self, data_or_length):
        if isinstance(data_or_length, int):
            self.length = data_or_length
            self.data = np.arange(data_or_length)
        else:
            if isinstance(data_or_length, list):
                data_or_length = np.array(data_or_length)
            self.data = data_or_length
            self.length = len(data_or_length)

class Databox:
    def __init__(self):
        self.dim = {}
        self.field = {}
        self.grid = {}
        self.attr = {}
        self.data = {}
        self.dimlist = []
        self.auto_generate_dim_name_format = "auto_generate_dimension{:d}"
        self.__originkeys = list(self.__dict__.keys())

    def __getitem__(self, key):
        if isinstance(key, int):
            self.dim[self.dimlist[key]]
                
        domains = [self.dim, self.field, self.grid]
        for domain in domains:
            if key in domain:
                return domain[key]
        raise KeyError("no \"{:s}\" in this Databox")
    
    def __str__(self):
        result = "Databox:\n"
        result += "    dim: " + str(self.dim) + "\n"
        result += "    field: " + str(self.field) + "\n"
        result += "    grid: " + str(self.grid) + "\n"
        for key, value in self.attr.items():
            result += "    {:s}: {:s}\n".format(key, str(value))
        return result
    __repr__ = __str__
    
    def add_dimension(self, name, value, attr = {}):
        self.dim[name] = Dimension(name, value, attr)
        self.dimlist.append(name)
        self.data[name] = self.dim[name].data

    def add_dimensions(self, dim_dict = None):
        for name, value in dim_dict.items():
            self.add_dimension(name, value)

    def add_field(self, name, data, dim = None, attr = {}):
        if dim is None:
            dim = self._auto_find_dim(data)
        self.field[name] = Variable(name, data, dim=dim, attr=attr)
        self.data[name] = self.field[name].data
    
    def add_grid(self, name, data, dim = None, attr = {}):
        if dim is None:
            dim = self._auto_find_dim(data)
        self.grid[name] = Variable(name, data, dim=dim, attr=attr)
        self.data[name] = self.grid[name].data

    def resort_dim_order_like(self, fieldname):
        refdim = self.field[fieldname].dim
        newdimlist = list(refdim)
        newdimlist += [other_dim for other_dim in self.dimlist if not other_dim in refdim]
        self.dimlist = newdimlist

    def resort_dim_order(self, neworder):
        """neworder is a list(array) filled with int from 0~n, n+1 is number of dims
        """
        if not len(self.dimlist) == len(neworder):
            raise Exception("length of new order needs to be equal to number of dimensions")
        newdimlist = []
        for i in neworder:
            newdimlist.append(self.dimlist[i])
        self.dimlist = newdimlist

    def setattrs(self, attr):
        for key, value in attr.items():
            self.attr[key] = value
            if isinstance(key, str):
                if key in self.__originkeys:
                    warnings.warn("\"{:s}\" is protected, so it will be skip".format(key))
                    continue
            setattr(self, key, value)

    def merge(self, databox):
        # check/copy dimensions
        for key in databox.dim:
            if key in self.dim:
                if databox.dim[key].data.shape != self.dim[key].data.shape:
                    warnings.warn("the dims shape between 2 databox are not the same")
            else:
                self.add_dimension(name=key, value=databox.dim[key].data, attr=databox.dim[key].attr)
        # copy field
        for key in databox.field:
            if not key in self.field:
                self.add_field(name=key, data=databox.field[key].data, dim=databox.field[key].dim, attr=databox.field[key].attr)

    def _auto_find_dim(self, data):
        dim = []
        dimlist = self.dimlist.copy()
        for i_length, length in enumerate(data.shape):
            for dim_name in dimlist:
                if length == self.dim[dim_name].length:
                    dim.append(dim_name)
                    dimlist.remove(dim_name)
                    break
            if i_length == len(dim): # find no dim in dimlist
                auto_created_dim = self._auto_create_dim(length) # no existed usefull dim
                dim.append(auto_created_dim)
        return dim

    def _auto_create_dim(self, length):
        name_format = self.auto_generate_dim_name_format
        agdim_number = 0
        name = name_format.format(agdim_number)
        while name in self.dim.keys():
            agdim_number += 1
            name = name_format.format(agdim_number)
        self.add_dimension(name, length)
        return name
        
if __name__ == "__main__":
    a = Variable("", np.arange(6).reshape(2, 3), attr = {"unit":"m"})
    #print(a.__dict__)
    #print(np.arange(6).reshape(2, 3))
    print(a[...])
    a[1][2] = 10
    #print(a[:])