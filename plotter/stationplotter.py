import matplotlib.pyplot as plt

from mypkgs.plotter.paintbox import Paintbox_1D, Paintbox_2D
from mypkgs.plotter.plotter import TwinPlotter, MapPlotter

def timeseries_T_rh_rain(data, Tname, rhname, rainname, Uname, Vname, starttime, endtime, timename="timestamp"):
    """
    Docstring for timeseries_T_rh_rain
    
    :param data: dict like 1d data (one station)
    :param Tname: key of temperature (degree C)
    :param rhname: key of relative humidity
    :param rainname: key of rainfall (mm)
    :param Uname: key of u wind (m/s)
    :param Vname: key of v wind (m/s)
    :param starttime: start of xticks (time ticks), input "%Y%m%d%H%M%S" or float (sec)
    :param endtime: end of xticks (time ticks), input "%Y%m%d%H%M%S" or float (sec)
    :param timename: key of time (sec)
    """
    TP = TwinPlotter(figsize=[8,6])
    TP.twin(rhname)
    TP.twin(rainname)
    TP.change_twinaxes_name(newname=Tname)
    TP.set_timeticks(starttime, endtime, intv=120*60, timefmt="%H:%M")
    Pb1 = Paintbox_1D(X=data, Y=data, fig=TP.fig)
    Pb1.bar(Xname=timename, Yname=rainname, ax=TP.ax[rainname], color="b", width=300, zorder=0)
    Pb1.plot(Xname=timename, Yname=Tname, ax=TP.ax[Tname], color="r", zorder=10)
    Pb1.plot(Xname=timename, Yname=rhname, ax=TP.ax[rhname], color="k", zorder=11)
    TP.ax[rainname].set_ylim(0,10)
    TP.ax[rainname].set_zorder(1)
    TP.set_ylabel("$^oC$", axn=(0, Tname))
    TP.set_ylabel("mm", axn=(0, rainname))
    # TP.ticks_auto_pad(axesname=)
    for name in [Tname, rhname]:
        ylim = TP.ax[name].get_ylim()
        ylim = (ylim[0]+(ylim[0]-ylim[1])*0.5, ylim[1])
        TP.ax[name].set_ylim(ylim)
    Pb1.barbs_x(Uname, Vname, timename, yposition=0.3, fig = None, ax = None, intv=1)
    
    return TP, Pb1

def timeseries_T_p_rain(data, Tname, pname, rainname, Uname, Vname, starttime, endtime, timename="timestamp"):
    """
    Docstring for timeseries_T_rh_rain
    
    :param data: dict like 1d data (one station)
    :param Tname: key of temperature (degree C)
    :param pname: key of pressure (hPa)
    :param rainname: key of rainfall (mm)
    :param Uname: key of u wind (m/s)
    :param Vname: key of v wind (m/s)
    :param starttime: start of xticks (time ticks), input "%Y%m%d%H%M%S" or float (sec)
    :param endtime: end of xticks (time ticks), input "%Y%m%d%H%M%S" or float (sec)
    :param timename: key of time (sec)
    """
    TP = TwinPlotter(figsize=[8,6])
    TP.twin(pname)
    TP.twin(rainname)
    TP.change_twinaxes_name(newname=Tname)
    TP.set_timeticks(starttime, endtime, intv=120*60, timefmt="%H:%M")
    Pb1 = Paintbox_1D(X=data, Y=data, fig=TP.fig)
    Pb1.bar(Xname=timename, Yname=rainname, ax=TP.ax[rainname], color="b", width=300, zorder=0)
    Pb1.plot(Xname=timename, Yname=Tname, ax=TP.ax[Tname], color="r", zorder=10)
    Pb1.plot(Xname=timename, Yname=pname, ax=TP.ax[pname], color="k", zorder=11)
    TP.ax[rainname].set_ylim(0,10)
    TP.ax[rainname].set_zorder(1)
    TP.set_ylabel("$^oC$", axn=(0, Tname))
    TP.set_ylabel("hPa", axn=(0, pname))
    TP.set_ylabel("mm", axn=(0, rainname))
    TP.ticks_auto_pad(axesname=rainname, xy="y", sub_num=0, padratio=0.25)
    for name in [Tname, pname]:
        ylim = TP.ax[name].get_ylim()
        ylim = (ylim[0]+(ylim[0]-ylim[1])*0.5, ylim[1])
        TP.ax[name].set_ylim(ylim)
    Pb1.barbs_x(Uname, Vname, timename, yposition=0.3, fig = None, ax = None, intv=1)
    
    return TP, Pb1

def stationmap(data, xname="LON", yname="LAT", xlim=[120.1, 122.1], ylim=[24, 25.5], **kwargs):
    """
    plot stations on the map
    
    :param data: dict like 1D data (many stations)
    :param xname: key of lon
    :param yname: key of lat
    :param xlim: xlim (lon)
    :param ylim: ylim (lat)
    :param kwargs: other args to plot
    """
    if not "marker" in kwargs:
        kwargs["marker"] = "o"
    MP = MapPlotter()
    MP.setlatlonticks(ticksitvl=[1, 0.5], xlim=xlim, ylim=ylim)
    MP.coastlines()
    MP.ax.plot(data[xname], data[yname], lw=0, **kwargs)
    return MP

def stationvarmap(data, varname, xname="LON", yname="LAT", colorkey=None, cmapdict=None, xlim=[120.1, 122.1], ylim=[24, 25.5], cbkwargs={}, **kwargs):
    """
    scatter var of stations on the map
    
    :param data: dict like 1D data (many stations in the same time)
    :param varname: key of var 
    :param xname: key of lon
    :param yname: key of lat
    :param xlim: xlim (lon)
    :param ylim: ylim (lat)
    :param cbkwargs: other args to color bar of scatter
    :param kwargs: other args to scatter
    """
    MP = MapPlotter()
    MP.setlatlonticks(ticksitvl=[1, 0.5], xlim=xlim, ylim=ylim)
    MP.coastlines()
    Pb = Paintbox_1D(X=data, Y=data, fig=MP.fig, ax=MP.ax, ft=MP.fontsize)
    Pb.scatter(xname, yname, varname, colorkey, cmapdict, cbkwargs=cbkwargs, **kwargs)
    return MP, Pb