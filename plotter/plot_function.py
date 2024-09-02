# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm
import cartopy.crs as ccrs

def onefigurebase(figsize=[18,18],ft=30,grid=True):
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(1, 1, 1)
    plt.tick_params(labelsize=ft)
    if grid:
        ax.grid()
    return ax, fig
"""
def setlatlonticks(ax,ticksitvl=[60,30],xlim=[0,360],ylim=[-90,90]):
    xtimax = 360
    xtimin = 0
    ytimax = 90
    ytimin = -90
    
    xticklabels = []
    for i in range(int(np.floor((xtimax-xtimin)/ticksitvl[0]))+1):
        lon_i = xtimin + i*ticksitvl[0]
        if lon_i==0:
            xticklabels.append('0')
        if lon_i==180:
            xticklabels.append('180')
        elif lon_i>180:
            xticklabels.append('{:.1f}W'.format(360-lon_i))
        elif lon_i<0:
            xticklabels.append('{:.1f}W'.format(-lon_i))
        elif lon_i>0:
            xticklabels.append('{:.1f}E'.format(lon_i))
    yticklabels = []
    for i in range(int(np.floor((ytimax-ytimin)/ticksitvl[1]))+1):
        lat_i = ytimin + i*ticksitvl[1]
        if lat_i==0:
            yticklabels.append('0')
        if lat_i<0:
            yticklabels.append('{:.1f}S'.format(-lat_i))
        if lat_i>0:
            yticklabels.append('{:.1f}N'.format(lat_i))
    
    ax.set_xticks(np.arange(xtimin,xtimax+0.01,ticksitvl[0]))
    ax.set_xticklabels(xticklabels)
    ax.set_yticks(np.arange(ytimin,ytimax+0.01,ticksitvl[1]))
    ax.set_yticklabels(yticklabels)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    return ax
"""
def get_lonticks(xtimin = 0, xtimax = 360, ticksitvl = 60, xlim = [0, 360]):
    xticks = np.arange(xtimin, xtimax+0.01, ticksitvl)
    xticks = xticks[np.logical_and(xticks >= xlim[0], xticks <= xlim[1])]
    xticklabels = []
    for lon_i in xticks:
        if lon_i==0:
            xticklabels.append('0')
        if lon_i==180:
            xticklabels.append('180')
        elif lon_i>180:
            xticklabels.append('{:.1f}W'.format(360-lon_i))
        elif lon_i<0:
            xticklabels.append('{:.1f}W'.format(-lon_i))
        elif lon_i>0:
            xticklabels.append('{:.1f}E'.format(lon_i))
    return xticks, xticklabels

def get_latticks(ytimin = -90, ytimax = 90, ticksitvl = 30, ylim = [-90, 90]):
    yticks = np.arange(ytimin, ytimax+0.01, ticksitvl)
    yticks = yticks[np.logical_and(yticks >= ylim[0], yticks <= ylim[1])]
    yticklabels = []
    for lat_i in yticks:
        if lat_i==0:
            yticklabels.append('0')
        if lat_i<0:
            yticklabels.append('{:.1f}S'.format(-lat_i))
        if lat_i>0:
            yticklabels.append('{:.1f}N'.format(lat_i))
    return yticks, yticklabels

def setlatlonticks(ax,ticksitvl=[60,30],xlim=[0,360],ylim=[-90,90], xtick_lim = [0, 360], ytick_lim = [-90, 90]):
    xtimax = xtick_lim[1]
    xtimin = xtick_lim[0]
    ytimax = ytick_lim[1]
    ytimin = xtick_lim[0]
    
    xticks, xticklabels = get_lonticks(xtimin, xtimax, ticksitvl[0], xlim)
    yticks, yticklabels = get_latticks(ytimin, ytimax, ticksitvl[1], ylim)    
    
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels)
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    return ax

def globalmapbase(figsize=[25,16],ft=30,ticksitvl=[60,30],xlim=[0,360],ylim=[-90,90],grid=True):
    ax, fig = onefigurebase(figsize=figsize, ft=ft, grid=grid)
    ax.set_aspect('equal', 'box')
    ax = setlatlonticks(ax,ticksitvl=ticksitvl,xlim=xlim,ylim=ylim)
    plt.setp(ax.get_xticklabels(),fontsize=ft-2)
    plt.setp(ax.get_yticklabels(),fontsize=ft-2)
    return ax,fig

def globalmapbase_ccrs(figsize=[25,16],ft=30,ticksitvl=[60,30],xlim=[0,360],ylim=[-90,90]):
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.coastlines()
    ax.tick_params(labelsize=ft)
    ax = setlatlonticks(ax,ticksitvl=ticksitvl,xlim=xlim,ylim=ylim)
    plt.setp(ax.get_xticklabels(),fontsize=ft-2)
    plt.setp(ax.get_yticklabels(),fontsize=ft-2)
    return ax,fig

def get_ax_size(ax, fig):
    """
    return width, height
    """
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width, height = bbox.width, bbox.height
    width *= fig.dpi
    height *= fig.dpi
    return width, height
    
def lineplot(ax, X, Ydict, legend=True, ft=30, colordict={}, linestyledict={}, markerdict={}, labeldict={}, linewidth=7, markersize=5):
    pd = {}
    for k in Ydict.keys():
        pd[k] = ax.plot(X,Ydict[k],label=k, linewidth=linewidth, markersize=markersize)[0]
    
    if colordict:
        for k in Ydict.keys():
            pd[k].set_color(colordict[k])
    if linestyledict:
        for k in Ydict.keys():
            pd[k].set_linestyle(linestyledict[k])
    if markerdict:
        for k in Ydict.keys():
            pd[k].set_marker(markerdict[k])
    if labeldict:
        for k in Ydict.keys():
            pd[k].set_label(labeldict[k])
    if legend:
        ax.legend(fontsize=ft)
    return pd

def _autosetting(var, norm, cmap, vmin, vmax):
    if cmap is None:
        cmap = cm.rainbow
    if vmin is None:
        vmin = np.min(var)
    if vmax is None:
        vmax = np.max(var)
    if norm is None:
        norm = mpl.colors.BoundaryNorm(np.arange(11)/10*(vmax-vmin)+vmin, cmap.N)
    return norm, cmap, vmin, vmax

def pcolormeshcb(ax,fig,X,Y,var,norm=None,cmap=None,cbtitle='',ft=30,orientation='vertical',extend='neither',shrink=1, vmin=None, vmax=None, continuous=False):
    norm, cmap, vmin, vmax = _autosetting(var, norm, cmap, vmin, vmax)
    if continuous:
        im = ax.pcolormesh(X, Y, var, shading='auto', vmin=vmin, vmax=vmax, cmap = cmap)
    else:
        im = ax.pcolormesh(X, Y, var, shading='auto', norm=norm, cmap = cmap)
    cax = fig.add_axes([ax.get_position().x1+0.03,ax.get_position().y0,0.03,ax.get_position().height])
    cb = fig.colorbar(im, orientation = orientation, extend=extend, shrink = shrink, cax=cax)
    cb.ax.set_title(cbtitle, fontdict={'size':ft})
    cb.ax.tick_params(labelsize=ft-2)
    return im, cb

def pcolormeshcb_sub(ax,fig,X,Y,var,norm=None,cmap=None,cbtitle='',ft=30,orientation='vertical',extend=None,shrink=1, vmin=None, vmax=None, continuous=False, cbticks=None):
    norm, cmap, vmin, vmax = _autosetting(var, norm, cmap, vmin, vmax)
    if extend is None:
        if cmap.colorbar_extend:
            extend = cmap.colorbar_extend
        else:
            extend = "neither"
    if continuous:
        im = ax.pcolormesh(X, Y, var, shading='auto', vmin=vmin, vmax=vmax, cmap = cmap)
    else:
        im = ax.pcolormesh(X, Y, var, shading='auto', norm=norm, cmap = cmap)
    if cbticks is None:
        cb = fig.colorbar(im, orientation = orientation, extend=extend, shrink = shrink, ax=ax)
    else:
        cb = fig.colorbar(im, orientation = orientation, extend=extend, shrink = shrink, ax=ax,boundaries=cbticks, values=cbticks[:-1], ticks=cbticks)
    cb.ax.set_title(cbtitle, fontdict={'size':ft})
    cb.ax.tick_params(labelsize=ft-2)
    return im, cb
    
def contourfcb_sub(ax,fig,X,Y,var,levels=None,norm=None,cmap=None,cbtitle='',ft=30,orientation='vertical',extend=None,shrink=1, vmin=None, vmax=None, continuous=False,cbticks=None):
    norm, cmap, vmin, vmax = _autosetting(var, norm, cmap, vmin, vmax)
    if extend is None:
        if cmap.colorbar_extend:
            extend = cmap.colorbar_extend
        else:
            extend = "neither"
    if levels is None:
        levels = norm.boundaries
    if continuous:
        im = ax.contourf(X, Y, var, vmin=vmin, vmax=vmax, cmap = cmap, extend=extend)
    else:
        vmin = levels[0]
        vmax = levels[-1]
        im = ax.contourf(X, Y, var, levels=levels, norm=norm, cmap = cmap, extend=extend)
    if cbticks is None:
        cb = fig.colorbar(im, orientation = orientation, extend=extend, shrink = shrink, ax=ax)
    else:
        cb = fig.colorbar(im, orientation = orientation, extend=extend, shrink = shrink, ax=ax, ticks=norm.boundaries)
        if orientation == "vertical":
            cb.ax.set_yticklabels(cbticks)
        if orientation == "horizontal":
            cb.ax.set_xticklabels(cbticks)
    cb.ax.set_title(cbtitle, fontdict={'size':ft})
    cb.ax.tick_params(labelsize=ft-2)
    return im, cb

def quiverandkey(ax,fig,X,Y,U,V,scale_q=0,color='k',iflegend=True,quiverlegend={},nx_q=1,ny_q=1):
    u_q = U[::ny_q,::nx_q]
    v_q = V[::ny_q,::nx_q]
    if not scale_q:
        scale_q = np.max(np.sqrt(u_q**2+v_q**2))*20
    xx_q, yy_q = np.meshgrid(X[::nx_q], Y[::ny_q])
    qui = ax.quiver(xx_q, yy_q, u_q, v_q, scale=scale_q,color=color)
    if iflegend:
        if not 'fontsize' in quiverlegend.keys():
            quiverlegend['fontsize']=26
        if not 'U' in quiverlegend.keys():
            maxws = scale_q/20
            order = 10**int(np.floor(np.log10(maxws)))
            quiverlegend['U'] = maxws*np.floor(maxws/order)/2
        if not 'label' in quiverlegend.keys():
            Ulog = int(np.floor(np.log10(quiverlegend['U'])))
            if Ulog>=0:
                quiverlegend['label'] = '{:.0f}'.format(quiverlegend['U'])
            else:
                quiverlegend['label'] = ('{:.'+str(int(-Ulog))+'f}').format(quiverlegend['U'])
        if not 'X' in quiverlegend.keys():
            quiverlegend['X'] = ax.get_position().x1 - len(quiverlegend['label'])*quiverlegend['fontsize']/fig.get_figheight()/100*0.8
        if not 'Y' in quiverlegend.keys():
            quiverlegend['Y'] = ax.get_position().y1 + quiverlegend['fontsize']/2/fig.get_figheight()/100 + 0.0025
        
        ax.quiverkey(qui,quiverlegend['X'],quiverlegend['Y'],quiverlegend['U'],quiverlegend['label'],coordinates='figure',labelpos='E',fontproperties={'size':quiverlegend['fontsize']})
    return qui
    
def quiver_weight(ax,fig,X,Y,U,V,scale_q=None,color='k',nx_q=1,ny_q=1,broadXY=True,weight=True,**pars):
    u_q = U[::ny_q,::nx_q]
    v_q = V[::ny_q,::nx_q]
    if weight:
        width, height = get_ax_size(ax,fig)
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        x_unit_len = (xlim[1]-xlim[0])/width
        y_unit_len = (ylim[1]-ylim[0])/height
        v_q = v_q/y_unit_len*x_unit_len
    if not scale_q:
        scale_q = np.max(np.sqrt(u_q**2+v_q**2)) * max(u_q.shape) / 2.
    if broadXY:
        xx_q, yy_q = np.meshgrid(X[::nx_q], Y[::ny_q])
    else:
        xx_q = X[::ny_q,::nx_q]
        yy_q = Y[::ny_q,::nx_q]
    qui = ax.quiver(xx_q, yy_q, u_q, v_q, scale=scale_q,color=color,angles="uv",pivot="mid",**pars)

    return qui