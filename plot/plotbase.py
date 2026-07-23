from functools import wraps
import numpy as np
from mypkgs.plotter.plotter import MapPlotter
from mypkgs.plotter.paintbox import Paintbox_2D


figsize = [10, 7.2]
dpi = 300
MPargs = dict(figsize=figsize, dpi=dpi)
xlim = [117, 123]
ylim = [20, 25]
ticksitvl = [1, 1]

def auto_build_MP(**kwargs):
    if not "figsize" in kwargs:
        kwargs["figsize"] = figsize
    if not "dpi" in kwargs:
        kwargs["dpi"] = dpi
    MP = MapPlotter(**kwargs)
    return MP

def customized_MP(ticksitvl, xlim=xlim, ylim=ylim, **kwargs):
    MP = auto_build_MP(**kwargs)
    MP.setlatlonticks(ticksitvl=ticksitvl, xlim=xlim, ylim=ylim)
    return MP

def MPbase(func):
    @wraps(func)
    def wraper(*args, title = "", xlim = xlim, ylim = ylim, ticksitvl = [None, None], tick_fmt = ".1f", coastline = False, MPargs = MPargs, **kwargs):
        if not "MP" in kwargs:
            MP = auto_build_MP(**MPargs)
            MP.setlatlonticks(ticksitvl=ticksitvl, xlim=xlim, ylim=ylim, fmt=tick_fmt)
            kwargs["MP"] = MP
        
        MP, PB2 = func(*args, **kwargs)
        if coastline:
            MP.coastline()
        MP.title(title, loc="left")
        MP.grid()
        MP.set_aspect()
        return MP, PB2
    return wraper