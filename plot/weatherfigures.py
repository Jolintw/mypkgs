from functools import wraps
import numpy as np
from mypkgs.plotter.plotter import MapPlotter
from mypkgs.plotter.paintbox import Paintbox_2D
from mypkgs.variable.mycolormap import get_cmapdict, add_norm, multiply_norm

figsize = [10, 7.2]
xlim = [117, 123]
ylim = [20, 25]
dpi = 250
length_mult = 0.6
barbnum = 30

def MPbase(func):
    @wraps(func)
    def wraper(*args, **kwargs):
        MP = MapPlotter(figsize=figsize, dpi=dpi)
        MP.setlatlonticks(ticksitvl=kwargs["ticksitvl"], xlim=kwargs["xlim"], ylim=kwargs["ylim"])
        kwargs["MP"] = MP
        MP, PB2 = func(*args, **kwargs)
        MP.coastlines()
        if "title" in kwargs:
            MP.title(kwargs["title"], loc="left")
        MP.grid()
        MP.set_aspect()
        return MP, PB2
    return wraper

@MPbase
def wind(lat, lon, u = None, v = None, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None], MP = None):
    """
    MP is no need to give value
    """
    ws = np.sqrt(u**2 + v**2)
    PB2 = Paintbox_2D(field=dict(u=u,v=v,ws=ws), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    if not u is None:
        PB2.auto_barbs(Uname="u", Vname="v", length_mult=length_mult, color="k", barbnum=barbnum)
        PB2.contourf(varname="ws", colorkey="ws_small", cbtitle="m/s")
    return MP, PB2

@MPbase
def dbz(lat, lon, dbz = None, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None], MP = None):
    """
    MP is no need to give value
    """
    PB2 = Paintbox_2D(field=dict(dbz=dbz), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    gray = 0.9
    MP.ax.set_facecolor(color = [gray, gray, gray])
    if not dbz is None:
        PB2.pcolormesh(varname="dbz", colorkey="dbz", cbtitle="dB$Z$")
    return MP, PB2

@MPbase
def accumulated_rainfall(lat, lon, rain = None, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None], MP = None):
    """
    MP is no need to give value
    """
    PB2 = Paintbox_2D(field=dict(rain=rain), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    if not rain is None:
        PB2.pcolormesh(varname="rain", colorkey="precipetation_cwb", cbtitle="mm")
    return MP, PB2

@MPbase
def VEL(lat, lon, VEL = None, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None], MP = None):
    PB2 = Paintbox_2D(field=dict(VEL=VEL), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    # gray = 0.9
    # MP.ax.set_facecolor(color = [gray, gray, gray])
    if not VEL is None:
        PB2.pcolormesh(varname="VEL", colorkey="VEL", cbtitle="m/s")
    return MP, PB2

@MPbase
def w_DBZ(lat, lon, w = None, DBZ = None, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None], MP = None):
    PB2 = Paintbox_2D(field=dict(w=w, DBZ=DBZ), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    # gray = 0.9
    # MP.ax.set_facecolor(color = [gray, gray, gray])
    if not w is None:
        PB2.pcolormesh(varname="w", colorkey="w", cbtitle="m/s")
    if not DBZ is None:
        PB2.contour(varname="DBZ", levels=[40])
    return MP, PB2

@MPbase
def VEL_discrete(lat, lon, wind, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None], MP = None):
    PB2 = Paintbox_2D(field=dict(wind=wind), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    if not wind is None:
        PB2.pcolormesh(varname="wind", colorkey="radial_wind", cbtitle="m/s")
    return MP, PB2

@MPbase
def P_perturbation(lat, lon, p, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None], MP = None):
    PB2 = Paintbox_2D(field=dict(p=p), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    if not p is None:
        PB2.contourf(varname="p", colorkey="Pperturbation", cbtitle="hPa")
    return MP, PB2

@MPbase
def Pressure(lat, lon, p, p_base, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None], MP = None):
    PB2 = Paintbox_2D(field=dict(p=p), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    cmapdict = get_cmapdict("Pperturbation")
    add_norm(cmapdict, p_base)
    if not p is None:
        PB2.contourf(varname="p", cmapdict = cmapdict, cbtitle="hPa")
    return MP, PB2

@MPbase
def temperature(lat, lon, T, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None], MP = None):
    PB2 = Paintbox_2D(field=dict(T=T), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    if not T is None:
        PB2.contourf(varname="T", colorkey="SST", cbtitle="K")
    return MP, PB2