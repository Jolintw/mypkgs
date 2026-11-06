import matplotlib as mpl
import numpy as np

from mypkgs.plotter.plotter import MapPlotter
from mypkgs.plotter.paintbox import Paintbox_2D
from mypkgs.plot.plotbase import MPbase

default_MPargs = {"figsize":[8, 6], "dpi":200}
figsize = [8, 6]
dpi = 200
xlim = [118, 123]
ylim = [20.5, 27]

@MPbase
def taiwan(lon, lat, terrain = None, lsm = None, MP:MapPlotter = None):
    PB2 = Paintbox_2D(field=dict(terrain=terrain,lsm=lsm), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    if not lsm is None:
        im, cb = PB2.contourf("lsm", colorkey="lsm")
        cb.remove()
    if not terrain is None:
        PB2.contourf("terrain", colorkey="terrain", cbtitle="[m]")
    return MP, PB2
    
@MPbase
def grayland(lon, lat, lsm = None, gray = 0.85, MP:MapPlotter = None):
    cmapdict = {}
    cmaparray = np.array([[gray, gray, gray]])
    cmapdict["cmap"] = mpl.colors.ListedColormap(cmaparray)
    bounds = np.array([0.5, 1.5])
    cmapdict["norm"] = mpl.colors.BoundaryNorm(bounds, cmapdict["cmap"].N)
    PB2 = Paintbox_2D(field=dict(lsm=lsm), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    if not lsm is None:
        im, cb = PB2.contourf("lsm", cmapdict=cmapdict)
        cb.remove()
    return MP, PB2