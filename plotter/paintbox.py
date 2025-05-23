import numpy as np

from mypkgs.plotter.plot_function import pcolormeshcb_sub, contourfcb_sub, quiver_weight, get_ax_size
from mypkgs.variable.mycolormap import colorkw

class Paintbox:
    def __init__(self, fig = None, ax = None, ft = 20):
        self._renewfig(fig)
        self._renewax(ax)
        self.fontsize = ft

    def _get_necessary(self, fig, ax):
        self._renewax(ax)
        self._renewfig(fig)
        return self.fig, self.ax

    def _renewax(self, ax = None):
        if not ax is None:
            self.ax = ax

    def _renewfig(self, fig = None):
        if not fig is None:
            self.fig = fig
    
    def _get_fontsize(self, ft=None):
        if ft is None:
            return self.fontsize
        else:
            return ft

class Paintbox_2D(Paintbox):
    def __init__(self, field, X, Y, fig = None, ax = None, ft = 20, level = None):
        self.field = field
        self.X = X
        self.Y = Y
        self.setlevel(level)
        super().__init__(fig=fig, ax=ax, ft=ft)
        
    def add_field(self, name, var):
        self.field[name] = var.copy()
        
    def setlevel(self, level):
        self.level = level
    
    def pcolormesh(self, varname, fig = None, ax = None, colorkey = None, cmapdict = None, norm = None, cmap = None, cbtitle='', ft = None, orientation='vertical', extend=None, shrink=1, vmin=None, vmax=None, continuous=False, cbticks=None):
        X, Y, var, fig, ax = self._get_necessary(varname, fig, ax)
        ft = self._get_fontsize(ft)
        if colorkey:
            cmapdict = colorkw[colorkey]
        if cmapdict:
            return pcolormeshcb_sub(ax, fig, X=X, Y=Y, var=var, **cmapdict, cbtitle=cbtitle, ft=ft,
                                orientation=orientation, extend=extend, shrink=shrink)
        else:
            return pcolormeshcb_sub(ax, fig, X=X, Y=Y, var=var, norm = norm, cmap = cmap, cbtitle=cbtitle, ft=ft,
                                orientation=orientation, extend=extend, shrink=shrink, vmin=vmin, vmax=vmax, continuous=continuous, cbticks=cbticks)
        
    def contourf(self, varname, fig = None, ax = None, colorkey = None, cmapdict = None, norm = None, cmap = None, cbtitle='', ft = None, orientation='vertical', extend=None, shrink=1, vmin=None, vmax=None, continuous=False, cbticks=None):
        """
        return: contourf object, colorbar object
        """
        X, Y, var, fig, ax = self._get_necessary(varname, fig, ax)
        ft = self._get_fontsize(ft)
        if colorkey:
            cmapdict = colorkw[colorkey]
        if cmapdict:
            return contourfcb_sub(ax=ax, fig=fig, X=X, Y=Y, var=var, **cmapdict, cbtitle=cbtitle, ft=ft,
                                orientation=orientation, extend=extend, shrink=shrink)
        else:
            return contourfcb_sub(ax=ax, fig=fig, X=X, Y=Y, var=var, norm = norm, cmap = cmap, cbtitle=cbtitle, ft=ft,
                                orientation=orientation, extend=extend, shrink=shrink, vmin=vmin, vmax=vmax, continuous=continuous, cbticks=cbticks)
    
    
    def contour(self, varname, fig = None, ax = None, colors = None, levels = None, linewidths = None, clabel = False, ft = None, **kwargs):
        X, Y, var, fig, ax = self._get_necessary(varname, fig, ax)
        ft = self._get_fontsize(ft)
        cs = ax.contour(X, Y, var, colors = colors, levels = levels, linewidths = linewidths, zorder = 20, **kwargs)
        if clabel:
            cl = ax.clabel(cs, cs.levels[:], inline=True, fontsize=ft)
            return cs, cl
        return cs
           
    def _unitscoef(self, units):
        if units == "m/s":
            return 1
        elif units == "knots":
            return 0.5144
            
    def barbs(self, Uname, Vname, fig = None, ax = None,  length=7, xintv=12, yintv=12, inunit = "m/s", outunit = "knots", **kwargs):
        X, Y, var, fig, ax = self._get_necessary([Uname, Vname], fig, ax)
        U = var[0]
        V = var[1]
        coef = self._unitscoef(inunit) / self._unitscoef(outunit)
        
        X = X[::yintv, ::xintv]
        Y = Y[::yintv, ::xintv]
        U = U[::yintv, ::xintv] * coef
        V = V[::yintv, ::xintv] * coef
        return ax.barbs(X,Y,U,V,length=length, zorder=19, **kwargs)
    
    def auto_barbs(self, Uname, Vname, fig = None, ax = None,  length_mult = None, intv = None, barbnum = [10, 10], inunit = "m/s", outunit = "knots", **kwargs):
        """
        length_mult: multiply of standard length (float), None will auto determined\n
        intv: grid interval of barbs (**list of int** [xintv, yintv] or **int** intv=xintv=yintv)\n
        barbsnum: number of barbs in x(y)axis (**list of int** [x, y] or **int** x=y), only works when intv=None
        """
        def _determine_barbs_intv_and_length(intv, length_mult, barbnum, meanlen, length_ref):
            if isinstance(intv, int):
                intv = [intv, intv]
            if intv is None:
                if isinstance(barbnum, int):
                    barbnum = [barbnum, barbnum]
                intv = [max(int(np.floor(l / n)), 1) for l, n in zip(meanlen, barbnum)]
            elif isinstance(intv, list):
                barbnum = [int(np.floor(l / i)) for l, i in zip(meanlen, intv)]
            if length_mult is None:
                length_mult = 10 / max(barbnum)
            length = np.sqrt(length_mult) * length_ref
            return intv, length
        
        X, Y, var, fig, ax = self._get_necessary([Uname, Vname], fig, ax)
        length_ref = self._barbs_ref_length(fig=fig, ax=ax)
        meanlen = self._grids_number_in_axes(ax=ax)
        intv, length = _determine_barbs_intv_and_length(intv, length_mult, barbnum, meanlen, length_ref)
        
        return self.barbs(Uname, Vname, fig=fig, ax=ax, length=length, xintv=intv[0], yintv=intv[1], inunit=inunit, outunit=outunit, **kwargs)

    def _barbs_ref_length(self, fig = None, ax = None):
        if fig is None:
            fig = self.fig
        if ax is None:
            ax = self.ax
        width, height = get_ax_size(ax=ax, fig=fig)
        length_ref = np.sqrt(max(width, height) / fig.dpi) * 3
        return length_ref
    
    def quiver(self, Uname, Vname, fig = None, ax = None, scale_q=None, xintv=None, yintv=None, broadXY=True, weight=False, **pars):
        X, Y, var, fig, ax = self._get_necessary([Uname, Vname], fig, ax)
        U = var[0]
        V = var[1]
        scale_q, xintv, yintv = self._autoscale(scale_q, xintv, yintv)
        return quiver_weight(ax,fig,X,Y,U,V,scale_q,"k",xintv,yintv,broadXY=broadXY,weight=weight,**pars)
    
    def _autoscale(self, scale_q=None, xintv=None, yintv=None):
        n = 20.
        if xintv is None:
            xintv = int(np.round(self.X.shape[-1] / n))
        if yintv is None:
            yintv = int(np.round(self.Y.shape[0] / n))
        #if scale_q is None:
        #    scale_q = 15*max([self.X.shape[-1]/xintv, self.Y.shape[0]/yintv])
        return scale_q, xintv, yintv
    
    def _grids_number_in_axes(self, ax = None):
        """
        do this after set_xlim and set_ylim\n
        return length_ref, [meanXlen, meanYlen]
        """
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        X = self.X
        Y = self.Y
        X_inxlim = np.logical_and(X > xlim[0], X < xlim[1])
        Y_inylim = np.logical_and(Y > ylim[0], Y < ylim[1])
        meanXlen = np.mean(np.sum(X_inxlim, axis=1))
        meanYlen = np.mean(np.sum(Y_inylim, axis=0))
        return [meanXlen, meanYlen]

    def _get_necessary(self, varname, fig, ax):
        super()._get_necessary(fig=fig, ax=ax)
        if type(varname) is list:
            var = []
            for name in varname:
                var.append(self._get_var_level(self.field[name][...]))
        else:
            var = self._get_var_level(self.field[varname][...])
        return self.X, self.Y, var, self.fig, self.ax
    
    def _get_var_level(self, var, level = None):
        level = self._autolevel(level)
        if len(var.shape) == 3:
            return var[level]
        elif len(var.shape) == 4:
            return var[level[0], level[1], ...]
        else:
            return var
    
    def _autolevel(self, level = None):
        if level is None:
            return self.level
        else:
            return level
        
class Paintbox_1D(Paintbox):
    def __init__(self, X, Y, fig = None, ax = None, ft = 20):
        self.X = X
        self.Y = Y
        super().__init__(fig=fig, ax=ax, ft=ft)

    def plot(self, Xname, Yname, fig = None, ax = None, **set_dict):
        X, Y, fig, ax = self._get_necessary(Xname, Yname, fig, ax)
        linewidth = self._auto_linewidth(fig, ax)
        p = ax.plot(X, Y, linewidth=linewidth)
        p[0].set(**set_dict)
        return p
    
    def quiver_y(self, Uname, Vname, Yname, xposition, fig = None, ax = None, scale_q=150, intv=1):
        """
        a line of quiver along y\n
        position: 0~1
        """
        var, Y, fig, ax = self._get_necessary([Uname, Vname], Yname, fig, ax)
        U = var[0]
        V = var[1]
        X = self._make_same_x_array_by_xposition(Y, xposition, ax)
        return ax.quiver(X[::intv], Y[::intv], U[::intv], V[::intv], scale=scale_q, headaxislength=2.5, headlength=3.5, headwidth=4)

    def quiver_x(self, Uname, Vname, Xname, yposition, fig = None, ax = None, scale_q=150, intv=1):
        """
        a line of quiver along x\n
        position: 0~1
        """
        X, var, fig, ax = self._get_necessary(Xname, [Uname, Vname], fig, ax)
        U = var[0]
        V = var[1]
        Y = self._make_same_y_array_by_yposition(X, yposition, ax)
        return ax.quiver(X[::intv], Y[::intv], U[::intv], V[::intv], scale=scale_q, headaxislength=2.5, headlength=3.5, headwidth=4)

    def barbs_x(self, Uname, Vname, Xname, yposition, fig = None, ax = None, intv=1):
        """
        a line of quiver along x\n
        position: 0~1
        """
        X, var, fig, ax = self._get_necessary(Xname, [Uname, Vname], fig, ax)
        U = var[0]
        V = var[1]
        Y = self._make_same_y_array_by_yposition(X, yposition, ax)
        return ax.barbs(X[::intv], Y[::intv], U[::intv], V[::intv])

    def scatter(self, Xname, Yname, Cname, colorkey=None, cmapdict=None, fig = None, ax = None, cbkwargs={}, **kwargs):
        X, C, fig, ax = self._get_necessary([Xname, Yname], Cname, fig, ax)
        X, Y = X[0], X[1]
        ft = self._get_fontsize()
        scatterargs = {}
        cbtitle = None
        if colorkey:
            cmapdict = colorkw[colorkey]
        scatterargs = cmapdict.copy()
        
        del scatterargs["cbticks"]
        im = ax.scatter(X, Y, c=C, **scatterargs, **kwargs)
        if "title" in cbkwargs:
            cbtitle = cbkwargs["title"]
            del cbkwargs["title"]
        cb = fig.colorbar(im, **cbkwargs)
        cb.ax.tick_params(labelsize=ft-2)
        if cbtitle:
            cb.ax.set_title(cbtitle, fontdict={'size':ft})
        return im, cb

    def plotmark_y(self, Y, xposition, fig = None, ax = None, **pars):
        """
        a line of mark along y\n
        position: 0~1
        """
        _, __, fig, ax = self._get_necessary([], [], fig, ax)
        X = self._make_same_x_array_by_xposition(Y, xposition, ax)
        p = ax.plot(X, Y, linestyle="", marker="o", markersize=self._auto_markersize(fig, ax))
        p[0].set(**pars)
        return p
    
    def bar(self, Xname, Yname, fig = None, ax = None, **pars):
        X, Y, fig, ax = self._get_necessary(Xname, Yname, fig, ax)
        ax.bar(X, Y, **pars)
    
    def boxplot(self, Yname, fig = None, ax = None, **pars):
        """
        pars:
        https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.boxplot.html#matplotlib.axes.Axes.boxplot
        """
        if isinstance(Yname, str):
            Yname = [Yname]
        _, Y, fig, ax = self._get_necessary([], Yname, fig, ax)
        for i_Y in range(len(Y)):
            Y[i_Y] = Y[i_Y][~np.isnan(Y[i_Y])]
        if "labels" not in pars:
            pars["labels"] = Yname
        for i_label, y in enumerate(Y):
            pars["labels"][i_label] += "\n({:d})".format(y.shape[0])
        return ax.boxplot(x=Y, **pars)

    def _auto_markersize(self, fig, ax):
        width, height = get_ax_size(ax, fig)
        markersize = np.sqrt(width*height)*0.015
        return markersize

    def _auto_linewidth(self, fig, ax):
        width, height = get_ax_size(ax, fig)
        linewidth = np.sqrt(width*height)*0.005
        return linewidth
    
    def _make_same_x_array_by_xposition(self, Y, xposition, ax):
        X = ax.get_xlim()
        X = X[0] + (X[1] - X[0]) * xposition
        X = X + np.zeros_like(Y)
        return X
    
    def _make_same_y_array_by_yposition(self, X, yposition, ax):
        Y = ax.get_ylim()
        Y = Y[0] + (Y[1] - Y[0]) * yposition
        Y = Y + np.zeros_like(X)
        return Y

    def _get_necessary(self, Xname, Yname, fig, ax):
        super()._get_necessary(fig=fig, ax=ax)
        if type(Xname) is list:
            X = []
            for name in Xname:
                X.append(self._auto_l2a(self.X[name]))
        else:
            X = self._auto_l2a(self.X[Xname])
        if type(Yname) is list:
            Y = []
            for name in Yname:
                Y.append(self._auto_l2a(self.Y[name]))
        else:
            Y = self._auto_l2a(self.Y[Yname])
        return X, Y, self.fig, self.ax
    
    def _auto_l2a(self, var):
        if isinstance(var, list):
            return np.array(var)
        else:
            return var