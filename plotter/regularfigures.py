from mypkgs.plotter.plotter import MapPlotter
from mypkgs.plotter.paintbox import Paintbox_2D
import numpy as np

figsize = [10, 8]
xlim = [108, 128]
ylim = [15, 35]

def NCDR_surface(lat, lon, u10 = None, v10 = None, slp = None, cwv = None, thick_1000_500 = None, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None]):
    MP = MapPlotter(figsize=figsize, dpi=150)
    PB2 = Paintbox_2D(field=dict(u10=u10,v10=v10,slp=slp,cwv=cwv,thick_1000_500=thick_1000_500), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    MP.coastlines()
    MP.setlatlonticks(ticksitvl=ticksitvl, xlim=xlim, ylim=ylim)
    MP.title(title, loc="left")
    if not cwv is None:
        PB2.pcolormesh(varname="cwv", colorkey="NCDR_cwv", cbtitle="[mm]")
    if not slp is None:
        PB2.contour(varname="slp", colors="k", levels=np.arange(15)*6+960, linewidths=MP.linewidth, clabel=True)
        PB2.contour(varname="slp", colors="k", levels=np.arange(45)*2+960, linewidths=MP.linewidth / 2)
    if not thick_1000_500 is None:
        PB2.contour(varname="thick_1000_500", colors="darkviolet", levels=np.arange(10)*30+5730, linewidths=MP.linewidth, clabel=True)
    if not u10 is None:
        PB2.auto_barbs(Uname="u10", Vname="v10")
    MP.grid()
    return MP, PB2

def NCDR_850ept(lat, lon, u = None, v = None, z = None, T = None, ept = None, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None]):
    MP = MapPlotter(figsize=figsize, dpi=150)
    PB2 = Paintbox_2D(field=dict(u=u,v=v,z=z,T=T,ept=ept), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    MP.coastlines()
    MP.setlatlonticks(ticksitvl=ticksitvl, xlim=xlim, ylim=ylim)
    MP.title(title, loc="left")
    if not ept is None:
        PB2.pcolormesh(varname="ept", colorkey="NCDR_ept", cbtitle="[K]")
    if not z is None:
        PB2.contour(varname="z", colors="k", levels=np.arange(15)*30+1290, linewidths=MP.linewidth, clabel=True)
        PB2.contour(varname="z", colors="k", levels=np.arange(30)*15+1290, linewidths=MP.linewidth / 2)
    if not T is None:
        PB2.contour(varname="T", colors="red", levels=np.arange(10)*6-12, linewidths=MP.linewidth, clabel=True, linestyles='dashed')
        PB2.contour(varname="T", colors="red", levels=np.arange(20)*2-12, linewidths=MP.linewidth / 2, linestyles='dashed')
    if not u is None:
        PB2.auto_barbs(Uname="u", Vname="v")
    MP.grid()
    return MP, PB2

def NCDR_850ept(lat, lon, u = None, v = None, z = None, T = None, ept = None, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None]):
    MP = MapPlotter(figsize=figsize, dpi=150)
    PB2 = Paintbox_2D(field=dict(u=u,v=v,z=z,T=T,ept=ept), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    MP.coastlines()
    MP.setlatlonticks(ticksitvl=ticksitvl, xlim=xlim, ylim=ylim)
    MP.title(title, loc="left")
    if not ept is None:
        PB2.pcolormesh(varname="ept", colorkey="NCDR_ept", cbtitle="[K]")
    if not z is None:
        PB2.contour(varname="z", colors="k", levels=np.arange(15)*30+1290, linewidths=MP.linewidth, clabel=True)
        PB2.contour(varname="z", colors="k", levels=np.arange(30)*15+1290, linewidths=MP.linewidth / 2)
    if not T is None:
        PB2.contour(varname="T", colors="red", levels=np.arange(10)*6-12, linewidths=MP.linewidth, clabel=True, linestyles='dashed')
        PB2.contour(varname="T", colors="red", levels=np.arange(20)*2-12, linewidths=MP.linewidth / 2, linestyles='dashed')
    if not u is None:
        PB2.auto_barbs(Uname="u", Vname="v")
    MP.grid()
    return MP, PB2

def NCDR_700rh(lat, lon, u = None, v = None, z = None, rh = None, div=None, title = "", figsize = figsize, xlim = xlim, ylim = ylim, ticksitvl = [None, None]):
    MP = MapPlotter(figsize=figsize, dpi=150)
    PB2 = Paintbox_2D(field=dict(u=u,v=v,z=z,rh=rh), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    MP.coastlines()
    MP.setlatlonticks(ticksitvl=ticksitvl, xlim=xlim, ylim=ylim)
    MP.title(title, loc="left")
    if not rh is None:
        PB2.pcolormesh(varname="rh", colorkey="NCDR_rh", cbtitle="[%]")
    if not z is None:
        PB2.contour(varname="z", colors="k", levels=np.arange(15)*30+2970, linewidths=MP.linewidth, clabel=True)
        PB2.contour(varname="z", colors="k", levels=np.arange(30)*15+2970, linewidths=MP.linewidth / 2)
    if not div is None:
        PB2.contour(varname="z", colors="purple", levels=[1e-5], linewidths=MP.linewidth / 2, linestyles="dashed")
    if not u is None:
        PB2.auto_barbs(Uname="u", Vname="v")
    MP.grid()
    return MP, PB2