from mypkgs.plotter.plotter import MapPlotter
from mypkgs.plotter.paintbox import Paintbox_2D

figsize = [7, 6]
xlim = [118, 123]
ylim = [20.5, 27]
dpi = 200

def _plot(PB, varname, plottype):
    if plottype == "contourf":
        return PB.contourf(varname, colorkey=varname)
    elif plottype == "pcolormesh":
        return PB.pcolormesh(varname, colorkey=varname)

def SSTplot(lon, lat, SST = None, terrain = None, xlim = xlim, ylim = ylim, ticksitvl = [None, None], plottype = "contourf"):
    MP = MapPlotter(figsize=figsize, dpi=dpi)
    PB2 = Paintbox_2D(field=dict(terrain=terrain,SST=SST), X=lon, Y=lat, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    
    if not terrain is None:
        im, cb = PB2.contourf("terrain", colorkey="terrain")
        cb.remove()
    if not SST is None:
        _plot(PB2, "SST", plottype)
    # MP.coastlines()
    MP.setlatlonticks(ticksitvl=ticksitvl, xlim=xlim, ylim=ylim)
    return MP, PB2