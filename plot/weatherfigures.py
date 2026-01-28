from functools import wraps
import numpy as np
from mypkgs.plotter.plotter import MapPlotter
from mypkgs.plotter.paintbox import Paintbox_2D
from mypkgs.variable.colormap_control import get_cmapdict, add_norm, multiply_norm

figsize = [10, 7.2]
xlim = [117, 123]
ylim = [20, 25]
ticksitvl = [1, 1]
dpi = 300
length_mult = 0.6
barbnum = 15

def customized_MP(ticksitvl, xlim=xlim, ylim=ylim, **kwargs):
    if not "figsize" in kwargs:
        kwargs["figsize"] = figsize
    if not "dpi" in kwargs:
        kwargs["dpi"] = dpi
    MP = MapPlotter(**kwargs)
    MP.setlatlonticks(ticksitvl=ticksitvl, xlim=xlim, ylim=ylim)
    return MP


def MPbase(func):
    @wraps(func)
    def wraper(*args, **kwargs):
        if not "MP" in kwargs:
            if "figsize" in kwargs:
                MP = MapPlotter(figsize=kwargs["figsize"], dpi=dpi)
            else:
                MP = MapPlotter(figsize=figsize, dpi=dpi)
            MP.setlatlonticks(ticksitvl=kwargs["ticksitvl"], xlim=kwargs["xlim"], ylim=kwargs["ylim"])
            kwargs["MP"] = MP
        MP, PB2 = func(*args, **kwargs)
        # MP.coastlines()
        if "title" in kwargs:
            MP.title(kwargs["title"], loc="left")
        MP.grid()
        MP.set_aspect()
        return MP, PB2
    return wraper

@MPbase
def wind(lon, lat, u = None, v = None, lsm = None, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None], intv=None, MP:MapPlotter = None):
    """
    MP is no need to give value
    """
    ws = np.sqrt(u**2 + v**2)
    gray = 0.9
    MP.ax.set_facecolor(color = [gray, gray, gray])
    PB2 = Paintbox_2D(field=dict(u=u,v=v,ws=ws,lsm=lsm), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    if not u is None:
        PB2.auto_barbs(Uname="u", Vname="v", length_mult=length_mult, color="k", barbnum=barbnum, intv=intv)
        PB2.contourf(varname="ws", colorkey="ws_small", cbtitle="m/s")
    if not lsm is None:
        PB2.contour(varname="lsm", levels=[0.5], colors="k", linewidths=MP.linewidth)
    return MP, PB2

@MPbase
def dbz(lon, lat, dbz = None, lsm = None, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None], MP:MapPlotter = None):
    """
    MP is no need to give value
    """
    PB2 = Paintbox_2D(field=dict(dbz=dbz,lsm=lsm), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    gray = 0.9
    MP.ax.set_facecolor(color = [gray, gray, gray])
    if not dbz is None:
        PB2.pcolormesh(varname="dbz", colorkey="dbz", cbtitle="dB$Z$")
    if not lsm is None:
        PB2.contour(varname="lsm", levels=[0.5], colors="k", linewidths=MP.linewidth)
    return MP, PB2

@MPbase
def accumulated_rainfall(lon, lat, rain = None, lsm = None, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None], MP:MapPlotter = None):
    """
    MP is no need to give value
    """
    PB2 = Paintbox_2D(field=dict(rain=rain,lsm=lsm), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    if not rain is None:
        PB2.pcolormesh(varname="rain", colorkey="precipetation_cwb", cbtitle="mm")
    if not lsm is None:
        PB2.contour(varname="lsm", levels=[0.5], colors="k", linewidths=MP.linewidth)
    return MP, PB2

@MPbase
def VEL(lon, lat, VEL = None, lsm = None, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None], MP:MapPlotter = None):
    PB2 = Paintbox_2D(field=dict(VEL=VEL,lsm=lsm), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    # gray = 0.9
    # MP.ax.set_facecolor(color = [gray, gray, gray])
    if not VEL is None:
        PB2.pcolormesh(varname="VEL", colorkey="VEL", cbtitle="m/s")
    if not lsm is None:
        PB2.contour(varname="lsm", levels=[0.5], colors="k", linewidths=MP.linewidth)
    return MP, PB2

@MPbase
def w_DBZ(lon, lat, w = None, DBZ = None, lsm = None, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None], MP:MapPlotter = None):
    PB2 = Paintbox_2D(field=dict(w=w, DBZ=DBZ,lsm=lsm), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    # gray = 0.9
    # MP.ax.set_facecolor(color = [gray, gray, gray])
    if not w is None:
        PB2.pcolormesh(varname="w", colorkey="w", cbtitle="m/s")
    if not DBZ is None:
        PB2.contour(varname="DBZ", levels=[40])
    if not lsm is None:
        PB2.contour(varname="lsm", levels=[0.5], colors="k", linewidths=MP.linewidth)
    return MP, PB2

@MPbase
def VEL_discrete(lon, lat, wind, lsm = None, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None], MP:MapPlotter = None):
    PB2 = Paintbox_2D(field=dict(wind=wind,lsm=lsm), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    if not wind is None:
        PB2.pcolormesh(varname="wind", colorkey="radial_wind", cbtitle="m/s")
    if not lsm is None:
        PB2.contour(varname="lsm", levels=[0.5], colors="k", linewidths=MP.linewidth)
    return MP, PB2

@MPbase
def P_perturbation(lon, lat, p, lsm = None, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None], MP:MapPlotter = None):
    PB2 = Paintbox_2D(field=dict(p=p,lsm=lsm), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    if not p is None:
        PB2.contourf(varname="p", colorkey="Pperturbation", cbtitle="hPa")
    if not lsm is None:
        PB2.contour(varname="lsm", levels=[0.5], colors="k", linewidths=MP.linewidth)
    return MP, PB2

@MPbase
def Pressure(lon, lat, p, p_base, u = None, v = None, lsm = None, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None], MP:MapPlotter = None):
    PB2 = Paintbox_2D(field=dict(p=p,u=u,v=v,lsm=lsm), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    cmapdict = get_cmapdict("Pperturbation")
    add_norm(cmapdict, p_base)
    if not p is None:
        PB2.contourf(varname="p", cmapdict = cmapdict, cbtitle="hPa")
    if not u is None:
        PB2.auto_barbs(Uname="u", Vname="v", length_mult=length_mult, color="k", barbnum=barbnum)
        # PB2.contourf(varname="ws", colorkey="ws_small", cbtitle="m/s")
    if not lsm is None:
        PB2.contour(varname="lsm", levels=[0.5], colors="k", linewidths=MP.linewidth)
    return MP, PB2

@MPbase
def temperature(lon, lat, T, lsm = None, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None], MP:MapPlotter = None):
    PB2 = Paintbox_2D(field=dict(T=T,lsm=lsm), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    if not T is None:
        PB2.contourf(varname="T", colorkey="SST", cbtitle="K")
    if not lsm is None:
        PB2.contour(varname="lsm", levels=[0.5], colors="k", linewidths=MP.linewidth)
    return MP, PB2

@MPbase
def temperature_2sides(lon, lat, T, T_base=0, u=None, v=None, lsm = None, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None], MP:MapPlotter = None):
    PB2 = Paintbox_2D(field=dict(T=T,u=u,v=v,lsm=lsm), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    gray = 0.9
    MP.ax.set_facecolor(color = [gray, gray, gray])
    cmapdict = get_cmapdict("Tperturbation")
    add_norm(cmapdict, T_base)
    if not T is None:
        PB2.contourf(varname="T", cmapdict = cmapdict, cbtitle="\u00B0C")
    if not u is None:
        PB2.auto_barbs(Uname="u", Vname="v", length_mult=length_mult, color="k", barbnum=barbnum)
    if not lsm is None:
        PB2.contour(varname="lsm", levels=[0.5], colors="k", linewidths=MP.linewidth)
    return MP, PB2