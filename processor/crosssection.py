# -*- coding: utf-8 -*-
import numpy as np
from mypkgs.processor.numericalmethod import RightAngleInterpolater
from mypkgs.writer.sectionwriter import writer_section

class CrossSection:
    """
    attrs: x(n,), y(n,), s(n,), variables(dict)
    """
    # x.shape == y.shape
    def __init__(self, x, y, s = None):
        self.x = x
        self.y = y
        self.n = x.shape[0]
        self.s = self._autos(s)
        self.start_point = [x[0], y[0]]
        self.end_point   = [x[-1], y[-1]]
        self.variables = {}
        
    def create_interpolater(self, gridx_1D, gridy_1D):
        x = self.x
        y = self.y
        mask_ingrid = np.logical_and(self._inrange(x, gridx_1D), self._inrange(y, gridy_1D))
        self.mask_ingrid = mask_ingrid
        self.ind_ingrid  = np.arange(x.shape[0], dtype = int)[self.mask_ingrid]
        x_ingrid = x[mask_ingrid]
        y_ingrid = y[mask_ingrid]
        
        self.RAI = RightAngleInterpolater(X = (gridy_1D, gridx_1D), newX = (y_ingrid, x_ingrid))
        
    def interpolate(self, var):
        newvar = np.zeros_like(self.x)
        newvar = newvar + np.nan
        newvar = np.broadcast_to(newvar, (*var.shape[:-2], self.n))
        newvar = np.array(newvar)
        if len(newvar.shape) >= 2:
            newvar[:, self.ind_ingrid] = self.RAI.interpolate(var)
        elif len(newvar.shape) == 1:
            newvar[self.ind_ingrid] = self.RAI.interpolate(var)
        return newvar
    
    def add_variable(self, varname, var):
        self.variables[varname] = var
        return var
    
    def reset_variable(self):
        self.variables = {}
        
    def _inrange(self, newx, oldx):
        return np.logical_and(newx > oldx[0], newx < oldx[-1])
    
    def _autos(self, s):
        x = self.x
        y = self.y
        if s is None:
            return np.sqrt((x - x[0])**2 + (y - y[0])**2)
        else:
            return s
        
# point_place = "head" or "mid" or "end",
# means (x0, y0) will be the first, middle, or last point of crosssec
# distance between every two point will be: length / (number - 1)
def create_CS_by_pointandangle(x, y, angle, length, number = 101, point_place = "head", angle_unit = "radius"):
    if angle_unit == "degree":
        angle = angle / 180 * np.pi
    if point_place == "head" or point_place ==  "end":
        x0 = x
        y0 = y
        x1 = x0 + length * np.cos(angle)
        y1 = y0 + length * np.sin(angle)
    elif point_place == "mid":
        x0 = x - length * np.cos(angle) / 2.
        y0 = y - length * np.sin(angle) / 2.
        x1 = x0 + length * np.cos(angle)
        y1 = y0 + length * np.sin(angle)
    x_arr = np.linspace(x0, x1, number)
    y_arr = np.linspace(y0, y1, number)
    if point_place == "end":
        x_arr = x_arr[::-1]
        y_arr = y_arr[::-1]
    CS = CrossSection(x_arr, y_arr)
    return CS

# angle is the positive direction
# angle: math angle
def radial_wind(u, v, angle, angle_unit = "radius"):
    if angle_unit == "degree":
        angle = angle / 180 * np.pi
    return u * np.cos(angle) + v * np.sin(angle)

def cross_wind(u, v, angle, angle_unit = "radius"):
    if angle_unit == "degree":
        angle = angle / 180 * np.pi
    return u * np.sin(angle) - v * np.cos(angle)

# ref_uv = [u, v]
def add_relativewind_to_dict(windfield, ref_uv = [], angle = None, angle_unit = "radius"):
    if len(ref_uv) >= 2:
        ref_u = ref_uv[0]
        ref_v = ref_uv[1]
        windfield["rel_u"] = windfield["u"] - ref_u
        windfield["rel_v"] = windfield["v"] - ref_v
    if not angle is None:
        windfield["radial_wind"] = radial_wind(windfield["u"], windfield["v"], angle, angle_unit)
        windfield["cross_wind"]  = cross_wind(windfield["u"], windfield["v"], angle, angle_unit) 
        if len(ref_uv) >= 2:
            windfield["rel_radial_wind"] = radial_wind(windfield["rel_u"], windfield["rel_v"], angle, angle_unit) 
            windfield["rel_cross_wind"] = cross_wind(windfield["rel_u"], windfield["rel_v"], angle, angle_unit)
    return windfield

def interpolate_and_write_with_CS(CS:CrossSection, x, y, z, field, varlist, savepath = None, filename = None):
    """
    CS: CrossSection object\n
    x: x grid (nx,)\n
    y: y grid (ny,)\n
    z: z grid (nz,)
    """
    CS.create_interpolater(x, y)
    for varname in varlist:
        if isinstance(field[varname], np.ma.core.MaskedArray):
            field[varname][field[varname].mask] = np.nan
        CS.add_variable(varname, CS.interpolate(field[varname]))
    
    if not (savepath is None or filename is None):
        writer_section(CS, z, savepath, filename)
        CS.reset_variable()
        
    return CS