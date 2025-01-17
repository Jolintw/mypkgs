# -*- coding: utf-8 -*-
import netCDF4 as nc
from mypkgs.writer.filewriter             import NCWriter

def writer_section(CS, gridpoint, savepath, filename):
    NCW = NCWriter()
    savepath.mkdir(exist_ok = True, parents = True)
    NCW.newNCD = nc.Dataset(savepath / filename, "w")
    NCW.writeDims(dimensionDict = {"s":CS.s, "z":gridpoint["z_1D"]})
    #print(NCW.newNCD)
    for varname in CS.variables.keys():
        #print(varname)
        #print(CS.variables[varname].shape)
        NCW.writeVariable(varname, CS.variables[varname])
    NCW.writeVariable("data_coverage", CS.mask_ingrid.astype(int))
    NCW.writeVariable("x", CS.x)
    NCW.writeVariable("y", CS.y)
    NCW.done()