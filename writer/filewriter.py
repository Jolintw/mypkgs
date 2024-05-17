import netCDF4 as nc
import numpy as np
from pathlib import Path

class NCWriter:
    newNCD = None
    def create_newNCD(self, filename, **pars):
        if isinstance(filename, Path):
            filename.parent.mkdir(parents=True, exist_ok=True)
        self.newNCD = nc.Dataset(filename, "w", **pars)
        return self.newNCD

    def writeVariable(self, varName: str, var, newNCD=None, dim=None, atts=None, fill_value = None):
        if newNCD is None:  # if new nc dataset not set, then use instance new nc dataset
            newNCD = self.newNCD

        if not dim:
            keys = list(newNCD.dimensions.keys())
            
            dim = []
            for dimlen in np.shape(var):
                for key in keys:
                    if newNCD.dimensions[key].size == dimlen:
                        dim.append(key)
                        keys.remove(key)
                        break
                    if key == keys[-1]:
                        for key in keys:
                            if (newNCD.dimensions[key].size is None) or (newNCD.dimensions[key].size == 0):
                                dim.append(key)
                                keys.remove(key)
                                break
                        break
            dim = tuple(dim)

        newVar = newNCD.createVariable(varName, var.dtype, dim, fill_value=fill_value)
        #newNCD.set_fill_on()
        if atts:
            newVar.setncatts(atts)
        
        newVar[...] = var
        
        return newVar

    # dimensionDict = {
    #     "t": 12,
    #     "y": np.arange(50) * 100,
    #     "x": {"var": np.arange(40), "atts": {"units": "meter"}},
    # }
    def writeDims(self, dimensionDict, newNCD=None):
        if newNCD is None:  # if new nc dataset not set, then use instance new nc dataset
            newNCD = self.newNCD

        for key, dimension in dimensionDict.items():

            if dimension is None:
                newNCD.createDimension(key, None)

            elif type(dimension) == int:
                if dimension == 0:
                    newNCD.createDimension(key, None)
                else:
                    newNCD.createDimension(key, dimension)

            elif type(dimension) == np.ndarray or type(dimension) == np.ma.core.MaskedArray:
                newNCD.createDimension(key, np.shape(dimension)[0])
                temp = newNCD.createVariable(key, dimension.dtype, (key,))
                temp[...] = dimension

            elif type(dimension) == dict:
                newNCD.createDimension(key, np.shape(dimension["var"])[0])
                self.writeVariable(key, dimension["var"], dim=(key,), atts=dimension["atts"])

        self.newNCD = newNCD

    # filename: name of creating nc file
    # refDataset: nc.Dataset(inFileName), inFileName is the file that you want to copy the basis of. Optional if inFileName is given
    # inFileName: The file that you want to copy the basis of. Optional if refDataset is given
    # dimensionVariable: create and copy the variables which have the same name of dimensions.(but unlimited dimension will not) Default=True
    # copyAtts: copy attributes of refDataset. Default=True
    def createNCFileLike(
        self, filename, refDataset=None, inFileName="", format="NETCDF4", dimensionVariable=True, copyAtts=True,
    ):
        if not refDataset:
            refDataset = nc.Dataset(inFileName)
        self.newNCD = nc.Dataset(filename, mode="w", format=format)
        dimensions = refDataset.dimensions
        dimensionDict = {}
        if dimensionVariable:
            for key in dimensions:
                if dimensions[key].isunlimited():
                    dimensionDict[key] = None
                elif key in refDataset.variables:
                    dimensionDict[key] = {
                        "var": refDataset.variables[key][...],
                        "atts": refDataset.variables[key].__dict__,
                    }
                else:
                    dimensionDict[key] = dimensions[key].size
        else:
            for key in dimensions:
                if dimensions[key].isunlimited():
                    dimensionDict[key] = None
                else:
                    dimensionDict[key] = dimensions[key].size
        self.writeDims(dimensionDict)

        if copyAtts:
            self.newNCD.setncatts(refDataset.__dict__)

        return self.newNCD
    
    # CopyVariables: 'all': copy all variables (be careful!!!!)
    # [varname1, varname2,...]: copy variables in list
    def copyNCFile(self, filename, refDataset=None, inFileName="", format="NETCDF4", CopyVariables=[]):
        self.createNCFileLike(filename, refDataset=refDataset, inFileName=inFileName, format=format, dimensionVariable=False)
        if not refDataset:
            refDataset = nc.Dataset(inFileName)
            
        if CopyVariables=='all':
            for varName, var in refDataset.variables.items():
                self.writeVariable(varName=varName, var=var[...], dim=var.dimensions, atts=var.__dict__)
        elif type(CopyVariables)==list:
            for varName in CopyVariables:
                var = refDataset[varName]
                self.writeVariable(varName=varName, var=var[...], dim=var.dimensions, atts=var.__dict__)
        
        return self.newNCD
    
    def createVariableLike(self, refVariable, newNCD=None):
        if newNCD is None:  # if new nc dataset not set, then use instance new nc dataset
            newNCD = self.newNCD
        otherargs = {}
        if "_FillValue" in refVariable.__dict__:
            otherargs["fill_value"] = refVariable.__dict__["_FillValue"]
        newVar = newNCD.createVariable(refVariable.name, refVariable.datatype, refVariable.dimensions, **otherargs)
        newVar.setncatts(refVariable.__dict__)

        return newVar
    
    def done(self):
        self.newNCD.close()