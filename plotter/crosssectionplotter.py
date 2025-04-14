# -*- coding: utf-8 -*-
from mypkgs.processor.crosssection   import add_relativewind_to_dict
from mypkgs.plotter.paintbox import Paintbox_2D
from mypkgs.plotter.plotter import Plotter

class CrossSectionPlotter:
    def __init__(self, plotter:Plotter, paintbox_wind:Paintbox_2D, patinbox_other:Paintbox_2D=None):
        self.PT       = plotter
        self.PB_wind  = paintbox_wind
        self.PB_other = patinbox_other
        
    def auto_pc(self, varname, axn = None, **args):
        """
        args: colorkey, cbtitle
        """
        axs = self.PT._axntoaxs(axn)
        for ax in axs:
            PB = self._findPB(varname)
            PB.pcolormesh(varname, ax = ax, **args)

    def auto_cf(self, varname, axn = None, **args):
        """
        args: colorkey, cbtitle
        """
        axs = self.PT._axntoaxs(axn)
        for ax in axs:
            PB = self._findPB(varname)
            PB.contourf(varname, ax = ax, **args)
            
    def auto_ct(self, varname, levels, colors = "k", linewidths = None, axn = None, **args):
        """
        args: clabel
        """
        axs = self.PT._axntoaxs(axn)
        linewidths = self.PT._autolinewidths(linewidths) * 2
        for ax in axs:
            PB = self._findPB(varname)
            PB.contour(varname, ax = ax, colors = colors, levels = levels, linewidths = linewidths, **args)

    def auto_quiver(self, scale_q=None, xintv=None, yintv=None, uwindname = "radial_wind", vwindname="w", axn = None, **args):
        axs = self.PT._axntoaxs(axn)
        
        for ax in axs:
            Q = self.PB_wind.quiver(uwindname, vwindname, self.PT.fig, ax, scale_q, xintv, yintv, **args)
        return Q
            
    def add_relativewind(self, ref_u, ref_v, angle, angle_unit = "radius"):
        PB_wind = self.PB_wind
        add_relativewind_to_dict(PB_wind.field, ref_uv = [ref_u, ref_v], angle = angle, angle_unit = angle_unit)

    def _findPB(self, varname):
        if varname in self.PB_wind.field:
            return self.PB_wind
        if varname in self.PB_other.field:
            return self.PB_other
        else:
            print(varname, "doesn't exist")