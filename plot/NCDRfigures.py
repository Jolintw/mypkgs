from functools import wraps
import numpy as np

from mypkgs.plotter.plotter import MapPlotter
from mypkgs.plotter.paintbox import Paintbox_2D
from mypkgs.plot.plotbase import MPbase

length_mult = 0.6
barbnum = 16

def geopotential_height_contour(PB:Paintbox_2D, gpth_name:str, pressure_hpa, linewidths, **contour_kwargs):
    gpth_base = {950:290, 900:790, 850:1290, 800:1790, 700:2970, 500:5100, 300:8760, 200:10500}
    gpth_itvl = {950:30, 900:30, 850:30, 800:30, 700:30, 500:60, 300:120, 200:120}
    number    = {950:15, 900:15, 850:15, 800:30, 700:15, 500:15, 300:20, 200:30}
    thick_levels_dict = {key:np.arange(number[key]) * gpth_itvl[key] + gpth_base[key] for key in gpth_base}
    thin_levels_dict  = {key:np.arange(number[key]) * gpth_itvl[key] + gpth_base[key] + gpth_itvl[key]/2 for key in gpth_base}
    # thick_levels_dict = {850:np.arange(15)*30+1290, 700:np.arange(15)*30+2970, 500:np.arange(15)*60+5100, 300:np.arange(20)*120+8760, 200:np.arange(30)*120+10500}
    pressure_list = np.array(list(gpth_itvl.keys()))
    i_close = np.argmin(np.abs(pressure_list - pressure_hpa))
    pressure_close = pressure_list[i_close]
    PB.contour(varname=gpth_name, levels=thick_levels_dict[pressure_close], linewidths=linewidths, clabel=True, **contour_kwargs)
    PB.contour(varname=gpth_name, levels=thin_levels_dict[pressure_close], linewidths=linewidths / 2, **contour_kwargs)

# parameters of MPbase: (title = "", xlim = xlim, ylim = ylim, ticksitvl = [None, None], tick_fmt = ".1f", coastline = False, MPargs = MPargs)
@MPbase
def NCDR_surface(lon, lat, u = None, v = None, slp = None, cwv = None, thick_1000_500 = None, MP:MapPlotter = None):
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
def NCDR_850ept(lon, lat, u = None, v = None, z = None, T = None, ept = None, MP:MapPlotter = None):
    """
    MP is no need to give value
    """
    PB2 = Paintbox_2D(field=dict(u=u,v=v,z=z,T=T,ept=ept), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    if not ept is None:
        PB2.pcolormesh(varname="ept", colorkey="NCDR_ept", cbtitle="[K]")
    if not z is None:
        geopotential_height_contour(PB=PB2, gpth_name="z", pressure_hpa=850, linewidths=MP.linewidth, colors="k")
        # PB2.contour(varname="z", colors="k", levels=np.arange(15)*30+1290, linewidths=MP.linewidth, clabel=True)
        # PB2.contour(varname="z", colors="k", levels=np.arange(15)*30+1290+15, linewidths=MP.linewidth / 2)
    if not T is None:
        PB2.contour(varname="T", colors="tomato", levels=np.arange(10)*6-12, linewidths=MP.linewidth / 2, clabel=True, linestyles='dashed')
        PB2.contour(varname="T", colors="tomato", levels=np.arange(20)*2-12, linewidths=MP.linewidth / 4, linestyles='dashed')
    if not u is None:
        PB2.auto_barbs(Uname="u", Vname="v", length_mult=length_mult, color="darkturquoise", barbnum=barbnum)
    return MP, PB2

@MPbase
def NCDR_700rh(lon, lat, u = None, v = None, z = None, rh = None, div = None, MP:MapPlotter = None):
    """
    MP is no need to give value
    rh: relative humidity (%)
    div: divergence (s^-1)
    """
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
def NCDR_500vor(lon, lat, u = None, v = None, z = None, vor = None, MP:MapPlotter = None):
    """
    MP is no need to give value
    vor: vorticity (s^-1)
    """
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
def NCDR_300ws(lon, lat, u = None, v = None, z = None, ws = None, div = None, MP:MapPlotter = None):
    """
    MP is no need to give value
    ws: windspeed (m s^-1)
    """
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
def NCDR_200ws(lon, lat, u = None, v = None, z = None, ws = None, div = None, MP:MapPlotter = None):
    """
    MP is no need to give value
    ws: windspeed (m s^-1)
    """
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