# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import mypkgs.plotter.plot_function as pf
from mypkgs.plotter.plot_function import pcolormeshcb_sub, contourfcb_sub
from mypkgs.variable.mycolormap import colorkw
from mypkgs.processor.timetools import timestamp_to_datetime, str_to_datetime_UTC

    
class Plotter:
    def __init__(self, row = 1, column = 1, figsize = None, subfigsize_x = 8, subfigsize_y = 6, fontsize = None, subplot_kw={}):
        self.row        = row
        self.column     = column
        self.figsize    = self._autofigsize(figsize, subfigsize_x, subfigsize_y)
        self.fontsize   = self._autofontsize(fontsize)
        self.subplot_kw = subplot_kw
        
        self.newsubplots()
            
    def newsubplots(self):
        fig, axs      = plt.subplots(self.row, self.column, figsize=self.figsize,subplot_kw=self.subplot_kw)
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
        
    def title(self, titlestr, loc = "left", axn = None):
        axs = self._axntoaxs(axn)
        for ax in axs:
            ax.set_title(titlestr, loc = loc, fontsize=self.fontsize * 1.2)
        
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
    
    def set_timeticks(self, start, end, intv, timefmt, startfmt = None, axis = "x", axn = None):
        if startfmt is None:
            startfmt = timefmt
        if isinstance(start, str):
            start = str_to_datetime_UTC(start).timestamp()
        if isinstance(end, str):
            end   = str_to_datetime_UTC(end).timestamp()
            
        stamplist = np.arange(start, end, intv)
        timelist = timestamp_to_datetime(stamplist)
        labels = [time.strftime(timefmt) for time in timelist]
        labels[0] = timelist[0].strftime(startfmt)
        if axis == "x":
            self.set_xticks(stamplist, labels, axn)
        elif axis == "y":
            self.set_yticks(stamplist, labels, axn)
            
    def set_facecolor(self, color = "black", axn = None):
        axs  = self._axntoaxs(axn)
        for ax in axs:
            ax.set_facecolor(color)
    
    def set_xlabel(self, label, fontsize = None, axn = None):
        if fontsize is None:
            fontsize = self.fontsize
        axs  = self._axntoaxs(axn)
        for ax in axs:
            ax.set_xlabel(label, fontsize = fontsize)
    
    def set_ylabel(self, label, fontsize = None, axn = None):
        if fontsize is None:
            fontsize = self.fontsize
        axs  = self._axntoaxs(axn)
        for ax in axs:
            ax.set_ylabel(label, fontsize = fontsize)
    
    def grid(self, axn = None):
        axs  = self._axntoaxs(axn)
        for ax in axs:
            ax.grid()
        
    def savefig(self, path, picname):
        path.mkdir(parents=True, exist_ok=True)
        plt.savefig(path / picname)
        self.close()
        
    def _axntoaxs(self, axn):
        if axn is None:
            axn = range(self.row * self.column)
        if type(axn) is int:
            axn = [axn]
        return [self.axs[n] for n in axn]
    
    def _set_ticksize(self):
        for ax in self.axs:
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

    def close(self):
        plt.close(self.fig)
    
class MapPlotter(Plotter):
    def __init__(self, row = 1, column = 1, figsize = None, fontsize = None, subplot_kw={"projection":ccrs.PlateCarree()}):
        super().__init__(row, column, figsize, fontsize, subplot_kw)
        
    def coastlines(self, axn = None):
        axs = self._axntoaxs(axn)
        for ax in axs:
            ax.coastlines()
    
    def setlatlonticks(self, ticksitvl = [60,30], xlim = [0,360], ylim = [-90,90], axn = None):
        axs = self._axntoaxs(axn)
        for ax in axs:
            pf.setlatlonticks(ax, ticksitvl, xlim, ylim)
    
