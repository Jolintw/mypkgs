from functools import wraps
import numpy as np
from mypkgs.plotter.plotter import MapPlotter
from mypkgs.plotter.paintbox import Paintbox_2D

figsize = [10, 7.2]
xlim = [117, 123]
ylim = [20, 25]
dpi = 250
length_mult = 0.6
barbnum = 30

def MPbase(func):
    @wraps(func)
    def wraper(*args, **kwargs):
        print(kwargs)
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
