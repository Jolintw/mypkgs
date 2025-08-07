# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from mypkgs.processor.crosssection   import add_relativewind_to_dict
from mypkgs.processor.numericalmethod import RightAngleInterpolater
from mypkgs.plotter.plotter          import Plotter
from mypkgs.plotter.paintbox         import Paintbox_2D
from mypkgs.plotter.crosssectionplotter import CrossSectionPlotter

ylim = [0, 12]
xlim = [15, 80]
plotterargs = dict(subfigsize_x=10, subfigsize_y=6)

# def get_titlestr(varname):
#     titlestr_dict = {"DBZ": "SPOL reflectivity",
#                      "DBZ_large": "SPOL reflectivity",
#                      "ws" : "wind speed",
#                      "DIV": "divergence",
#                      "VOR": "vorticity",
#                      "ZDR": "SPOL $Z_{DR}$",
#                      "KDP": "SPOL $K_{DP}$",
#                      "VVB": "total RHS",
#                      "VOR_t": "vorticity tendency",
#                      "T": "temperature",
#                      "wind_gradient_multiply_h": "$u_zw_x+v_zw_y$"}
#     if varname in titlestr_dict:
#         return titlestr_dict[varname]
#     else:
#         return varname

def secplotbase(field_wind, infor_wind, field_other=None, infor_other=None, plotterargs = plotterargs, xlim = xlim, ylim = ylim, xshift = False, row=1, column=1, facecolor=[0.9, 0.9, 0.9]):
    sub_number = row*column
    xlabelaxn = [i + row - 1 for i in range(int(np.round(sub_number/row)))]
    ylabelaxn = [i * 2 for i in range(row)]

    PT         = Plotter(row=row, column=column, **plotterargs)
    PB_wind    = Paintbox_2D(field_wind, infor_wind["s"][...] / 1e3, infor_wind["z"][...] / 1e3, fig = PT.fig)
    if not field_other is None:
        PB_other = Paintbox_2D(field_other, infor_other["s"][...] / 1e3, infor_other["z"][...] / 1e3, fig = PT.fig)
    else:
        PB_other = None
    CSP        = CrossSectionPlotter(PT, PB_wind, PB_other)

    PT.set_facecolor(color = facecolor)
    auto_set_lim(CSP, xlim, xshift, ylim)
    PT.set_xlabel("distance (km)", axn = xlabelaxn)
    PT.set_ylabel("height (km)", axn = ylabelaxn)

    return CSP
    
def auto_suptitle(PT, timelist):
    startstr  = timelist[0].strftime("%Y/%m/%d %H:%M:%S")
    endstr    = timelist[1].strftime("%H:%M:%S")
    titlestr  = "dual doppler {:s} ~ {:s} UTC \n".format(startstr, endstr)
    PT.suptitle(titlestr)
    
def auto_rel_wind(CSP, convection_center, timelist, angle, angle_unit, param_wt):
    if param_wt["if_relative"]:
        midtime     = (timelist[0].timestamp() + timelist[1].timestamp()) / 2.
        """
        RIA = RightAngleInterpolater(X = convection_center["time"], newX = np.array([midtime]), equidistance = False)
        velocity_x = RIA.interpolate(convection_center["velocity_x"])[0]
        velocity_y = RIA.interpolate(convection_center["velocity_y"])[0]
        """
        timemeanrange = [midtime - 1800, midtime + 1800]
        if timemeanrange[0] < convection_center["time"][0]:
           timemeanrange[0] = convection_center["time"][0]
        if timemeanrange[1] > convection_center["time"][-1]:
           timemeanrange[1] = convection_center["time"][-1]
           
        RIA = RightAngleInterpolater(X = convection_center["time"], newX = np.array(timemeanrange), equidistance = False)
        cc_x = RIA.interpolate(convection_center["x"])
        cc_y = RIA.interpolate(convection_center["y"])
        velocity_x = (cc_x[1] - cc_x[0]) / (timemeanrange[1] - timemeanrange[0])
        velocity_y = (cc_y[1] - cc_y[0]) / (timemeanrange[1] - timemeanrange[0])
        CSP.add_relativewind(velocity_x, velocity_y, angle = angle, angle_unit = angle_unit)
    else:
        add_relativewind_to_dict(CSP.PB_wind.field, angle = angle, angle_unit = angle_unit)
        
def auto_set_lim(CSP, xlim, xshift, ylim = None):
    if xshift:
        CSP.PB_wind.X = CSP.PB_wind.X - xlim[0]
        CSP.PB_radar.X = CSP.PB_radar.X - xlim[0]
        xlim = [lim - xlim[0] for lim in xlim]
    
    CSP.PT.set_xlim(xlim)
    CSP.PT.set_ylim([0, 15])
    if not ylim is None:
        CSP.PT.set_ylim(ylim)