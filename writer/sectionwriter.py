# -*- coding: utf-8 -*-
import netCDF4 as nc
from mypkgs.writer.filewriter import NCWriter
from pathlib import Path

def writer_section(CS, z, savepath, filename):
    """
    CS: CrossSection object\n
    z: z grid (nz,)
    """
    NCW = NCWriter()
    if isinstance(savepath, str):
        savepath = Path(savepath)
    savepath.mkdir(exist_ok = True, parents = True)
    NCW.newNCD = nc.Dataset(savepath / filename, "w")
    NCW.writeDims(dimensionDict = {"s":CS.s, "z":z})
    for varname in CS.variables.keys():
        NCW.writeVariable(varname, CS.variables[varname])
    NCW.writeVariable("data_coverage", CS.mask_ingrid.astype(int))
    NCW.writeVariable("x", CS.x)
    NCW.writeVariable("y", CS.y)
    NCW.done()