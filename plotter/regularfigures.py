from mypkgs.plotter.plotter import MapPlotter
from mypkgs.plotter.paintbox import Paintbox_2D
import numpy as np

# figsize = [10, 10]

def NCDR_surface(lat, lon, u10 = None, v10 = None, slp = None, cwv = None, thick_1000_500 = None, title = "", figsize = [14, 10], xlim = [108, 128], ylim = [15, 35], ticksitvl = [None, None]):
    MP = MapPlotter(figsize=figsize)
    PB2 = Paintbox_2D(field=dict(u10=u10,v10=v10,slp=slp,cwv=cwv,thick_1000_500=thick_1000_500), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    MP.coastlines()
    MP.setlatlonticks(ticksitvl=ticksitvl, xlim=xlim, ylim=ylim)
    MP.title(title, loc="left")
    PB2.pcolormesh(varname="cwv", colorkey="NCDR_cwv", cbtitle="[mm]")
    PB2.contour(varname="slp", colors="k", levels=np.arange(15)*6+960, linewidths=MP.linewidth, clabel=True)
    PB2.contour(varname="slp", colors="k", levels=np.arange(45)*2+960, linewidths=MP.linewidth / 2)
    PB2.contour(varname="thick_1000_500", colors="darkviolet", levels=np.arange(10)*30+5730, linewidths=MP.linewidth)
    MP.grid()
    return MP, PB2
