import numpy as np

from mypkgs.plotter.plot_function import pcolormeshcb_sub, contourfcb_sub, quiver_weight
from mypkgs.variable.mycolormap import colorkw

class Paintbox_2D:
    def __init__(self, field, X, Y, fig = None, ax = None, level = None):
        self.field = field
        self.X = X
        self.Y = Y
        self._renewfig(fig)
        self._renewax(ax)
        self.setlevel(level)
        
    def add_field(self, name, var):
        self.field[name] = var.copy()
        
    def setlevel(self, level):
        self.level = level
    
    def pcolormesh(self, varname, fig = None, ax = None, colorkey = None, norm = None, cmap = None, cbtitle='', ft = 20, orientation='vertical', extend='neither', shrink=1, vmin=None, vmax=None, continuous=False, cbticks=None):
        X, Y, var, fig, ax = self._get_necessary(varname, fig, ax)
        if colorkey:
            return pcolormeshcb_sub(ax, fig, X=X, Y=Y, var=var, **colorkw[colorkey], cbtitle=cbtitle, ft=ft,
                                orientation=orientation, extend=extend, shrink=shrink)
        else:
            return pcolormeshcb_sub(ax, fig, X=X, Y=Y, var=var, norm = norm, cmap = cmap, cbtitle=cbtitle, ft=ft,
                                orientation=orientation, extend=extend, shrink=shrink, vmin=vmin, vmax=vmax, continuous=continuous, cbticks=cbticks)
        
    def contourf(self, varname, fig = None, ax = None, colorkey = None, norm = None, cmap = None, cbtitle='', ft = 20, orientation='vertical', extend='neither', shrink=1, vmin=None, vmax=None, continuous=False, cbticks=None):
        X, Y, var, fig, ax = self._get_necessary(varname, fig, ax)
        if colorkey:
            return contourfcb_sub(ax=ax, fig=fig, X=X, Y=Y, var=var, **colorkw[colorkey], cbtitle=cbtitle, ft=ft,
                                orientation=orientation, extend=extend, shrink=shrink)
        else:
            return contourfcb_sub(ax=ax, fig=fig, X=X, Y=Y, var=var, norm = norm, cmap = cmap, cbtitle=cbtitle, ft=ft,
                                orientation=orientation, extend=extend, shrink=shrink, vmin=vmin, vmax=vmax, continuous=continuous, cbticks=cbticks)
    
    
    def contour(self, varname, fig = None, ax = None, colors = None, levels = None, linewidths = None, clabel = False):
        X, Y, var, fig, ax = self._get_necessary(varname, fig, ax)
        cs = ax.contour(X, Y, var, colors = colors, levels = levels, linewidths = linewidths, zorder = 20)
        if clabel:
            cl = ax.clabel(cs, cs.levels[:], inline=True, fontsize=self.fontsize - 2)
            return cs, cl
        return cs
           
    def _unitscoef(self, units):
        if units == "m/s":
            return 1
        elif units == "knots":
            return 0.5144
            
    def barbs(self, Uname, Vname, fig = None, ax = None,  length=7, xintv=12, yintv=12, inunit = "m/s", outunit = "knots"):
        X, Y, var, fig, ax = self._get_necessary([Uname, Vname], fig, ax)
        U = var[0]
        V = var[1]
        coef = self._unitscoef(inunit) / self._unitscoef(outunit)
        
        X = X[::yintv, ::xintv]
        Y = Y[::yintv, ::xintv]
        U = U[::yintv, ::xintv] * coef
        V = V[::yintv, ::xintv] * coef
        return ax.barbs(X,Y,U,V,length=length, zorder=19)
    
    def _autoscale(self, scale_q=None, xintv=None, yintv=None):
        n = 20.
        if xintv is None:
            xintv = int(np.round(self.X.shape[-1] / n))
        if yintv is None:
            yintv = int(np.round(self.Y.shape[0] / n))
        #if scale_q is None:
        #    scale_q = 15*max([self.X.shape[-1]/xintv, self.Y.shape[0]/yintv])
        return scale_q, xintv, yintv
    
    def quiver(self, Uname, Vname, fig = None, ax = None, scale_q=None, xintv=None, yintv=None):
        X, Y, var, fig, ax = self._get_necessary([Uname, Vname], fig, ax)
        U = var[0]
        V = var[1]
        scale_q, xintv, yintv = self._autoscale(scale_q, xintv, yintv)
        quiver_weight(ax,fig,X,Y,U,V,scale_q,"k",xintv,yintv,broadXY=True)
    
    def _get_necessary(self, varname, fig, ax):
        if type(varname) is list:
            var = []
            for name in varname:
                var.append(self._get_var_level(self.field[name][...]))
        else:
            var = self._get_var_level(self.field[varname][...])
        self._renewax(ax)
        self._renewfig(fig)
        return self.X, self.Y, var, self.fig, self.ax
    
    def _get_var_level(self, var, level = None):
        level = self._autolevel(level)
        if len(var.shape) == 3:
            return var[level]
        else:
            return var
    
    def _autolevel(self, level = None):
        if level is None:
            return self.level
        else:
            return level

    def _renewax(self, ax = None):
        if not ax is None:
            self.ax = ax

    def _renewfig(self, fig = None):
        if not fig is None:
            self.fig = fig
    