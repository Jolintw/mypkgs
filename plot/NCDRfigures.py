from functools import wraps
import numpy as np
from mypkgs.plotter.plotter import MapPlotter
from mypkgs.plotter.paintbox import Paintbox_2D

figsize = [8, 6]
xlim = [108, 128]
ylim = [15, 35]
dpi = 300
length_mult = 0.45
barbnum = 20

def MPbase(func):
    @wraps(func)
    def wraper(*args, **kwargs):
        MP = MapPlotter(figsize=figsize, dpi=dpi)
        MP.setlatlonticks(ticksitvl=kwargs["ticksitvl"], xlim=kwargs["xlim"], ylim=kwargs["ylim"])
        kwargs["MP"] = MP
        MP, PB2 = func(*args, **kwargs)
        MP.coastlines()
        MP.title(kwargs["title"], loc="left")
        MP.grid()
        MP.set_aspect()
        return MP, PB2
    return wraper

@MPbase
def NCDR_surface(lon, lat, u = None, v = None, slp = None, cwv = None, thick_1000_500 = None, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None], MP:MapPlotter = None):
    """
    MP is no need to give value
    """
    PB2 = Paintbox_2D(field=dict(u=u,v=v,slp=slp,cwv=cwv,thick_1000_500=thick_1000_500), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    if not cwv is None:
        PB2.pcolormesh(varname="cwv", colorkey="NCDR_cwv", cbtitle="[mm]")
    if not slp is None:
        PB2.contour(varname="slp", colors="k", levels=np.arange(15)*6+960, linewidths=MP.linewidth, clabel=True)
        levels = np.arange(30, dtype=int)
        levels = (levels+levels//2)*2+962
        PB2.contour(varname="slp", colors="k", levels=np.arange(45)*2+960, linewidths=MP.linewidth / 2)
    if not thick_1000_500 is None:
        PB2.contour(varname="thick_1000_500", colors="darkviolet", levels=np.arange(10)*30+5730, linewidths=MP.linewidth, clabel=True)
    if not u is None:
        PB2.auto_barbs(Uname="u", Vname="v", length_mult=length_mult, color="darkturquoise", barbnum=barbnum)
    return MP, PB2


@MPbase
def NCDR_850ept(lon, lat, u = None, v = None, z = None, T = None, ept = None, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None], MP:MapPlotter = None):
    """
    MP is no need to give value
    """
    PB2 = Paintbox_2D(field=dict(u=u,v=v,z=z,T=T,ept=ept), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    if not ept is None:
        PB2.pcolormesh(varname="ept", colorkey="NCDR_ept", cbtitle="[K]")
    if not z is None:
        PB2.contour(varname="z", colors="k", levels=np.arange(15)*30+1290, linewidths=MP.linewidth, clabel=True)
        PB2.contour(varname="z", colors="k", levels=np.arange(15)*30+1290+15, linewidths=MP.linewidth / 2)
    if not T is None:
        PB2.contour(varname="T", colors="tomato", levels=np.arange(10)*6-12, linewidths=MP.linewidth / 2, clabel=True, linestyles='dashed')
        PB2.contour(varname="T", colors="tomato", levels=np.arange(20)*2-12, linewidths=MP.linewidth / 4, linestyles='dashed')
    if not u is None:
        PB2.auto_barbs(Uname="u", Vname="v", length_mult=length_mult, color="darkturquoise", barbnum=barbnum)
    return MP, PB2

@MPbase
def NCDR_700rh(lon, lat, u = None, v = None, z = None, rh = None, div = None, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None], MP:MapPlotter = None):
    """
    MP is no need to give value
    rh: relative humidity (%)
    div: divergence (s^-1)
    """
    # MP = MapPlotter(figsize=figsize, dpi=dpi)
    # MP.setlatlonticks(ticksitvl=ticksitvl, xlim=xlim, ylim=ylim)
    PB2 = Paintbox_2D(field=dict(u=u,v=v,z=z,rh=rh,div=div), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    if not rh is None:
        PB2.pcolormesh(varname="rh", colorkey="NCDR_rh", cbtitle="[%]")
    if not z is None:
        PB2.contour(varname="z", colors="k", levels=np.arange(15)*30+2970, linewidths=MP.linewidth, clabel=True)
        PB2.contour(varname="z", colors="k", levels=np.arange(15)*30+2970+15, linewidths=MP.linewidth / 2)
    if not div is None:
        PB2.contour(varname="div", colors="purple", levels=[-1e-5], linewidths=MP.linewidth / 2, linestyles="dashed")
    if not u is None:
        PB2.auto_barbs(Uname="u", Vname="v", length_mult=length_mult, color="darkorange", barbnum=barbnum)
    return MP, PB2

@MPbase
def NCDR_500vor(lon, lat, u = None, v = None, z = None, vor = None, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None], MP:MapPlotter = None):
    """
    MP is no need to give value
    vor: vorticity (s^-1)
    """
    # MP = MapPlotter(figsize=figsize, dpi=dpi)
    # MP.setlatlonticks(ticksitvl=ticksitvl, xlim=xlim, ylim=ylim)
    PB2 = Paintbox_2D(field=dict(u=u,v=v,z=z,vor=vor*1e5), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    if not vor is None:
        PB2.pcolormesh(varname="vor", colorkey="NCDR_vorticity", cbtitle="[$10^5\ s^{-1}$]")
    if not z is None:
        PB2.contour(varname="z", colors="k", levels=np.arange(15)*60+5100, linewidths=MP.linewidth, clabel=True)
        PB2.contour(varname="z", colors="k", levels=np.arange(15)*60+5100+30, linewidths=MP.linewidth / 2)
    if not u is None:
        PB2.auto_barbs(Uname="u", Vname="v", length_mult=length_mult, color="blue", barbnum=barbnum)
    return MP, PB2

@MPbase
def NCDR_300ws(lon, lat, u = None, v = None, z = None, ws = None, div = None, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None], MP:MapPlotter = None):
    """
    MP is no need to give value
    ws: windspeed (m s^-1)
    """
    # MP = MapPlotter(figsize=figsize, dpi=dpi)
    # MP.setlatlonticks(ticksitvl=ticksitvl, xlim=xlim, ylim=ylim)
    PB2 = Paintbox_2D(field=dict(u=u,v=v,z=z,ws=ws,div=div), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    if not ws is None:
        PB2.pcolormesh(varname="ws", colorkey="NCDR_ws", cbtitle="[$m/s$]")
    if not z is None:
        PB2.contour(varname="z", colors="k", levels=np.arange(20)*120+8760, linewidths=MP.linewidth, clabel=True)
        PB2.contour(varname="z", colors="k", levels=np.arange(20)*120+8760-60, linewidths=MP.linewidth / 2)
    if not div is None:
        PB2.contour(varname="div", colors="red", levels=[1e-5], linewidths=MP.linewidth / 2, linestyles="solid")
    if not u is None:
        PB2.auto_barbs(Uname="u", Vname="v", length_mult=length_mult, color="blue", barbnum=barbnum)
    return MP, PB2

@MPbase
def NCDR_200ws(lon, lat, u = None, v = None, z = None, ws = None, div = None, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None], MP:MapPlotter = None):
    """
    MP is no need to give value
    ws: windspeed (m s^-1)
    """
    # MP = MapPlotter(figsize=figsize, dpi=dpi)
    # MP.setlatlonticks(ticksitvl=ticksitvl, xlim=xlim, ylim=ylim)
    PB2 = Paintbox_2D(field=dict(u=u,v=v,z=z,ws=ws,div=div), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    if not ws is None:
        PB2.pcolormesh(varname="ws", colorkey="NCDR_ws", cbtitle="[$m/s$]")
    if not z is None:
        PB2.contour(varname="z", colors="k", levels=np.arange(30)*120+10500, linewidths=MP.linewidth, clabel=True)
        PB2.contour(varname="z", colors="k", levels=np.arange(30)*120+10500+60, linewidths=MP.linewidth / 2)
    if not div is None:
        PB2.contour(varname="div", colors="red", levels=[1e-5], linewidths=MP.linewidth / 2, linestyles="solid")
    if not u is None:
        PB2.auto_barbs(Uname="u", Vname="v", length_mult=length_mult, color="blue", barbnum=barbnum)
    return MP, PB2