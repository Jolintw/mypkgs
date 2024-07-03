# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from collections.abc import Iterable

import mypkgs.plotter.plot_function as pf
from mypkgs.plotter.plot_function import pcolormeshcb_sub, contourfcb_sub
from mypkgs.variable.mycolormap import colorkw
from mypkgs.processor.timetools import timestamp_to_datetime, str_to_datetime_UTC

twinaxes_default_name = "origin"
class Plotter:
    def __init__(self, row = 1, column = 1, figsize = None, subfigsize_x = None, subfigsize_y = None, fontsize = None, subplot_kw={}, sharex = False, sharey = False):
        self.row        = row
        self.column     = column
        self.figsize    = self._autofigsize(figsize, subfigsize_x, subfigsize_y)
        self.fontsize   = self._autofontsize(fontsize)
        self.subplot_kw = subplot_kw
        self.sharex = sharex
        self.sharey = sharey
        
        self.newsubplots()
            
    def newsubplots(self):
        fig, axs      = plt.subplots(self.row, self.column, figsize=self.figsize,subplot_kw=self.subplot_kw,sharex=self.sharex, sharey=self.sharey)
        self.fig      = fig
        
        if isinstance(axs, np.ndarray):
            axs = axs.flatten()
            self.axs  = axs
        else:
            self.axs  = np.array([axs])
            
        self.ax       = axs
        self._set_ticksize()
        
    def suptitle(self, titlestr):
        self.fig.suptitle(titlestr, fontsize=self.fontsize * 1.4)
        
    def title(self, titlestr, loc = "left", axn = None, **pars):
        axs = self._axntoaxs(axn)
        for ax in axs:
            text = ax.set_title(titlestr, loc = loc, fontsize=self.fontsize * 1.2)
            text.set(**pars)
        
    def pcolormesh(self, axn, X, Y, var, colorkey = None, norm = None, cmap = None, cbtitle='', orientation='vertical', extend='neither', shrink=1, vmin=None, vmax=None, continuous=False, cbticks=None):
        ax  = self.axs[axn]
        fig = self.fig
        ft  = self.fontsize
        if colorkey:
            return pcolormeshcb_sub(ax=ax, fig=fig, X=X, Y=Y, var=var, **colorkw[colorkey], cbtitle=cbtitle, ft=ft,
                                orientation=orientation, extend=extend, shrink=shrink)
        else:
            return pcolormeshcb_sub(ax=ax, fig=fig, X=X, Y=Y, var=var, norm = norm, cmap = cmap, cbtitle=cbtitle, ft=ft,
                                orientation=orientation, extend=extend, shrink=shrink, vmin=vmin, vmax=vmax, continuous=continuous, cbticks=cbticks)
    
    def contourf(self, axn, X, Y, var, colorkey = None, norm = None, cmap = None, cbtitle='', orientation='vertical', extend='neither', shrink=1, vmin=None, vmax=None, continuous=False, cbticks=None):
        ax  = self.axs[axn]
        fig = self.fig
        ft  = self.fontsize
        if colorkey:
            return contourfcb_sub(ax=ax, fig=fig, X=X, Y=Y, var=var, **colorkw[colorkey], cbtitle=cbtitle, ft=ft,
                                orientation=orientation, extend=extend, shrink=shrink, continuous=continuous)
        else:
            return contourfcb_sub(ax=ax, fig=fig, X=X, Y=Y, var=var, norm = norm, cmap = cmap, cbtitle=cbtitle, ft=ft,
                                orientation=orientation, extend=extend, shrink=shrink, vmin=vmin, vmax=vmax, continuous=continuous, cbticks=cbticks)
    
    
    def contour(self, axn, X, Y, var, colors = None, levels = None, linewidths = None, clabel = False):
        linewidths = self._autolinewidths(linewidths)
        axs  = self._axntoaxs(axn)
        for ax in axs:
            cs = ax.contour(X, Y, var, colors = colors, levels = levels, linewidths = linewidths, zorder = 20)
            if clabel:
                ax.clabel(cs, cs.levels[:], inline=True, fontsize=self.fontsize - 2)

    def hline(self, y, axn = None, **pars):
        linewidth = self._autolinewidths()
        axs  = self._axntoaxs(axn)
        for ax in axs:
            xlim = ax.get_xlim()
            line = ax.plot([xlim[0], xlim[1]], [y, y], linewidth=linewidth)
            line[0].set(**pars)
        return line

    def quiverkey(self, qui, X, Y, U, label = "", labelpos = "E", fontsize = None, coordinates='figure', axn = None):
        axs = self._axntoaxs(axn)
        for ax in axs:
            ax.quiverkey(qui, X, Y, U, label, labelpos=labelpos, coordinates=coordinates, fontproperties={'size':self._autofontsize(fontsize)})
                
    def axisoff(self, axn = None):
        axs  = self._axntoaxs(axn)
        for ax in axs:
            ax.set_axis_off()
    
    def set_xlim(self, xlim, axn = None):
        axs  = self._axntoaxs(axn)
        for ax in axs:
            ax.set_xlim(xlim)

    def set_ylim(self, ylim, axn = None):
        axs  = self._axntoaxs(axn)
        for ax in axs:
            ax.set_ylim(ylim)
    
    def set_xticks(self, xticks, xticklabels, axn = None):
        axs  = self._axntoaxs(axn)
        for ax in axs:
            ax.set_xticks(xticks)
            ax.set_xticklabels(xticklabels)
            
    def set_yticks(self, yticks, yticklabels, axn = None):
        axs  = self._axntoaxs(axn)
        for ax in axs:
            ax.set_yticks(yticks)
            ax.set_yticklabels(yticklabels)

    def auto_set_xticks(self, intv, strfmt, start = None, end = None, axn = None):
        axs  = self._axntoaxs(axn)
        for ax in axs:
            ticks, ticklabels = self._auto_make_ticklabels(intv, strfmt, ax.get_xlim(), start, end)
            ax.set_xticks(ticks)
            ax.set_xticklabels(ticklabels)

    def auto_set_yticks(self, intv, strfmt, start = None, end = None, axn = None):
        axs  = self._axntoaxs(axn)
        for ax in axs:
            ticks, ticklabels = self._auto_make_ticklabels(intv, strfmt, ax.get_ylim(), start, end)
            ax.set_yticks(ticks)
            ax.set_yticklabels(ticklabels)
    
    def set_timeticks(self, start, end, intv, timefmt, startfmt = None, timezonehour = 0, axis = "x", axn = None):
        """
        start: (float) start timestamp of ticks
        end: (float) end timestamp of ticks
        intv: ticks interval
        """
        if startfmt is None:
            startfmt = timefmt
        if isinstance(start, str):
            start = str_to_datetime_UTC(start).timestamp()
        if isinstance(end, str):
            end   = str_to_datetime_UTC(end).timestamp()
            
        stamplist = np.arange(start, end, intv)
        timelist = timestamp_to_datetime(stamplist, timezonehour)
        labels = [time.strftime(timefmt) for time in timelist]
        if startfmt:
            labels[0] = timelist[0].strftime(startfmt)
        if axis == "x":
            self.set_xticks(stamplist, labels, axn)
        elif axis == "y":
            self.set_yticks(stamplist, labels, axn)
            
    def set_facecolor(self, color = "black", axn = None):
        axs  = self._axntoaxs(axn)
        for ax in axs:
            ax.set_facecolor(color)
    
    def set_xlabel(self, label, fontsize = None, axn = None, **pars):
        if fontsize is None:
            fontsize = self.fontsize
        axs  = self._axntoaxs(axn)
        textlist = []
        for ax in axs:
            text = ax.set_xlabel(label, fontsize = fontsize)
            text.set(**pars)
            textlist.append(text)
        return textlist
    
    def set_ylabel(self, label, fontsize = None, axn = None, **pars):
        if fontsize is None:
            fontsize = self.fontsize
        axs  = self._axntoaxs(axn)
        textlist = []
        for ax in axs:
            text = ax.set_ylabel(label, fontsize = fontsize)
            text.set(**pars)
            textlist.append(text)
        return textlist
    
    def grid(self, axn = None, **pars):
        axs  = self._axntoaxs(axn)
        for ax in axs:
            ax.grid()
        
    def savefig(self, path, picname, tight_layout = True):
        path.mkdir(parents=True, exist_ok=True)
        if tight_layout:
            self.fig.set_tight_layout(True)
        plt.savefig(path / picname)
        self.close()
        
    def _axntoaxs(self, axn):
        if axn is None:
            axn = range(self.row * self.column)
        if type(axn) is int:
            axn = [axn]
        return [self.axs[n] for n in axn]
    
    def _set_ticksize(self, axn = None):
        axs = self._axntoaxs(axn)
        for ax in axs:
            ax.tick_params(labelsize=self.fontsize)
    
    def _autofigsize(self, figsize, subfigsize_x, subfigsize_y):
        title_space = 0.25
        if subfigsize_x is None:
            subfigsize_x = 8
        if subfigsize_y is None:
            subfigsize_y = 6
        if figsize is None:
            self.subfigsize_x = subfigsize_x
            self.subfigsize_y = subfigsize_y
            return [subfigsize_x * self.column, subfigsize_y * (self.row + title_space)]
        else:
            self.subfigsize_x = figsize[0] / self.column
            self.subfigsize_y = figsize[1] / (self.row + title_space)
            return figsize
    
    def _autofontsize(self, fontsize):
        if fontsize is None:
            return self.figsize[1] * 0.9 + self.subfigsize_y * 1.8
        else:
            return fontsize
    
    def _autolinewidths(self, linewidths = None):
        if linewidths is None:
            return np.sqrt(self.subfigsize_x * self.subfigsize_y) / 2.5
        else:
            return linewidths
        
    def _auto_make_ticklabels(self, intv, strfmt, lim, start = None, end = None):
        if start is None:
            start = np.ceil(lim[0] / intv) * intv
        if end is None:
            end   = np.floor(lim[1] / intv) * intv + intv / 100
        ticks = np.arange(start, end, intv)
        ticklabels = [strfmt.format(tick) for tick in ticks]
        return ticks, ticklabels

    def close(self):
        plt.close(self.fig)
    
class MapPlotter(Plotter):
    def __init__(self, row = 1, column = 1, figsize = None, subfigsize_x = None, subfigsize_y = None, fontsize = None, subplot_kw={"projection":ccrs.PlateCarree()}):
        super().__init__(row=row, column=column, figsize=figsize, subfigsize_x=subfigsize_x, subfigsize_y=subfigsize_y, fontsize=fontsize, subplot_kw=subplot_kw)
        
    def coastlines(self, axn = None):
        axs = self._axntoaxs(axn)
        for ax in axs:
            ax.coastlines()
    
    def setlatlonticks(self, ticksitvl = [60,30], xlim = [0,360], ylim = [-90,90], axn = None):
        axs = self._axntoaxs(axn)
        for ax in axs:
            pf.setlatlonticks(ax, ticksitvl, xlim, ylim)
    
class TwinPlotter(Plotter):
    def newsubplots(self):
        fig, axs      = plt.subplots(self.row, self.column, figsize=self.figsize,subplot_kw=self.subplot_kw)
        self.fig      = fig
        
        if isinstance(axs, np.ndarray):
            axs = axs.flatten()
        else:
            axs  = np.array([axs])

        self.axs = [TwinAxesController(ax) for ax in axs]
        if len(self.axs) == 1:
            self.ax = self.axs[0]
        else:
            self.ax = self.axs
        self._set_ticksize()

    def twin(self, axesname = None, sub_num = None, xy = "x"):
        sub_num = self._auto_subnum(sub_num)
        for num in sub_num:
            if axesname is None:
                name = f"{len(self.axs[num])}"
            else:
                name = axesname
            ax = self.axs[num][0]
            if xy == "x":
                twin = ax.twinx()
            elif xy == "y":
                twin = ax.twiny()
            self.axs[num][name] = twin
            tick_xy = "xy".replace(xy, "")
            self.ticks_auto_pad(axesname=name, xy=tick_xy, sub_num=num)
            axn = (num, name)
            self._set_ticksize(axn)
        return twin
    
    def change_twinaxes_name(self, newname, oldname=twinaxes_default_name, sub_num = None):
        sub_num = self._auto_subnum(sub_num)
        for num in sub_num:
            self.axs[num].change_axes_name(newname, oldname=oldname)

    def ticks_auto_pad(self, axesname, xy, sub_num, padratio=0.09):
        axs  = self.axs[sub_num] 
        axes = self.axs[sub_num][axesname]
        if xy == "x":
            pos_to_pad = axes.xaxis.get_ticks_position()
        elif xy == "y":
            pos_to_pad = axes.yaxis.get_ticks_position()

        pad_number = 0
        for ax in axs:
            if ax is axes:
                break
            if xy == "x":
                pos = ax.xaxis.get_ticks_position()
            elif xy == "y":
                pos = ax.yaxis.get_ticks_position()
            if pos == pos_to_pad:
                pad_number += 1
        if pos_to_pad in ["left", "bottom"]:
            pad = 0 -  padratio * pad_number
        elif pos_to_pad in ["top", "right"]:
            pad = 1 +  padratio * pad_number
        axes.spines[pos_to_pad].set_position(("axes", pad))


    def _axntoaxs(self, axn):
        axs = self.axs
        if axn is None:
            axn = range(self.row * self.column)
            axn = [(ax, 0) for ax in axn]
        if type(axn) is int:
            return axs[axn]
        elif isinstance(axn, Iterable):
            if isinstance(axn[0], Iterable):
                return [axs[ax[0]][ax[1]] for ax in axn]
            else:
                return [axs[axn[0]][axn[1]]]
            
    def _auto_subnum(self, sub_num):
        if sub_num is None:
            sub_num = range(len(self.axs))
        if not isinstance(sub_num, Iterable):
            sub_num = [sub_num]
        return sub_num


class TwinAxesController():
    def __init__(self, ax, axname=None):
        if not axname:
            axname = twinaxes_default_name
        self.axdict = {axname:ax}
        self.axlist = [ax]

    def change_axes_name(self, newname, oldname=twinaxes_default_name):
        self.axdict[newname] = self.axdict.pop(oldname)

    def keys(self):
        return self.axdict.keys()
    
    def items(self):
        return self.axdict.items()
    
    def values(self):
        return self.axdict.values()
    
    def __getitem__(self, key):
        if isinstance(key, str):
            return self.axdict[key]
        else:
            return self.axlist[key]
        
    def __setitem__(self, key, value):
        self.axdict[key] = value
        self.axlist.append(value)
    
    def __len__(self):
        return len(self.axlist)
    
    def __repr__(self):
        return repr(self.axdict)
    
    def __str__(self):
        return repr(self)

    