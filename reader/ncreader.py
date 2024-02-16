import netCDF4 as nc

from mypkgs.reader.databox import Databox
# from databox import Databox

class NCreader:
    def __init__(self, filename = None, dataset = None, databox = None):
        self.dataset = self._get_dataset(filename, dataset)
        self.databox = databox
        if databox is None:
            self.databox = Databox()
    
    def auto_read(self, varlist = [], read_all = False):
        self.copy_attributes()
        self.copy_dimensions()
        if read_all:
            varlist = [var for var in list(self.dataset.variables.keys()) if not var in self.databox.dimlist]
        self.read_variables(varlist)

    def copy_attributes(self):
        self.databox.setattrs(self.dataset.__dict__)

    def copy_dimensions(self):
        dimensions = self.dataset.dimensions
        variables = self.dataset.variables
        for name in dimensions:
            dimension = dimensions[name]
            if name in variables:
                variable = variables[name]
                self.databox.add_dimension(name, value=variable[:], attr=variable.__dict__)
            else:
                self.databox.add_dimension(name, value=dimension.size)
    
    def read_variables(self, varlist):
        for varname in varlist:
            self.read_variable(varname)

    def read_variables_with_newname(self, varlist, newnamelist):
        for varname, newname in zip(varlist, newnamelist):
            self.read_variable(varname, newname)

    def read_variable(self, varname, newname = None):
        if newname is None:
            newname = varname
        var = self.dataset[varname]
        data = self.databox
        data.add_field(newname, var[:], var.dimensions, attr=var.__dict__)

    def append_to_existed_variable(self, varname, axis = None, newdimname = "NOT_DEFINED"):
        var = self.dataset[varname]
        self.databox[varname].append(var, axis=axis, newdimname=newdimname)

    def _get_dataset(self, filename, dataset):
        if filename is None:
            return dataset
        else:
            return nc.Dataset(filename)
        
    def close(self):
        self.dataset.close()

if __name__ == "__main__":
    filename = "D:/TAHOPE/IOP3/SAMURAI_output/samurai_XYZ_analysis_20220606062400.nc"
    NCR = NCreader(filename = filename)
    NCR.auto_read(read_all=True)
    # NCR.copy_attributes()
    # NCR.copy_dimensions()
    # NCR.read_variables_with_newname("U", "u")
    print(NCR.databox)
    print(NCR.databox.dim)
    print(NCR.databox.field)
    print(NCR.databox["U"])
    #print(NCR.dataset["U"])
    #print(NCR.dataset["U"].ncattrs())
    NCR.close()