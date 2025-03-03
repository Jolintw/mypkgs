# -*- coding: utf-8 -*-
import matplotlib as mpl
import numpy as np
from matplotlib import cm
import cmaps

def _kw(colorkw, name):
    colorkw[name] = {}
    return colorkw[name]

NCL_testmap = cmaps.testcmap.copy()
NCL_radar = cmaps.radar.copy()
NCL_nrl_sirkes = cmaps.nrl_sirkes.copy()
NCL_prcp_1 = cmaps.prcp_1.copy()
NCL_MPL_Spectral = cmaps.MPL_Spectral
NCL_MPL_RdBu_r = cmaps.MPL_RdBu_r
NCL_MPL_RdBu = cmaps.MPL_RdBu
NCL_wind_17lev = cmaps.wind_17lev
pycm_jet = cm.jet
NCL_WhiteBlueGreenYellowRed = cmaps.WhiteBlueGreenYellowRed
NCL_MPL_terrain = cmaps.MPL_terrain
NCL_cmocean_thermal = cmaps.cmocean_thermal
NCL_MPL_hot = cmaps.MPL_hot
NCL_WhiteBlue = cmaps.WhiteBlue
NCL_CBR_coldhot = cmaps.CBR_coldhot

colorkw = {}
name = "dbz_cwb"
kw = _kw(colorkw, name)
cmaparray = np.array([[0.0, 1.0, 1.0], [0.0, 0.9254901960784314, 1.0], [0.0, 0.8549019607843137, 1.0], [0.0, 0.7843137254901961, 1.0], [0.0, 0.7137254901960784, 1.0], [0.0, 0.6392156862745098, 1.0], [0.0, 0.5686274509803921, 1.0], [0.0, 0.4980392156862745, 1.0], [0.0, 0.42745098039215684, 1.0], [0.0, 0.3568627450980392, 1.0], [0.0, 0.2823529411764706, 1.0], [0.0, 0.21176470588235294, 1.0], [0.0, 0.1411764705882353, 1.0], [0.0, 0.07058823529411765, 1.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0], [0.0, 0.9568627450980393, 0.0], [0.0, 0.9137254901960784, 0.0], [0.0, 0.8705882352941177, 0.0], [0.0, 0.8274509803921568, 0.0], [0.0, 0.7843137254901961, 0.0], [0.0, 0.7450980392156863, 0.0], [0.0, 0.7058823529411765, 0.0], [0.0, 0.6666666666666666, 0.0], [0.0, 0.6274509803921569, 0.0], [0.0, 0.5882352941176471, 0.0], [0.2, 0.6705882352941176, 0.0], [0.4, 0.7529411764705882, 0.0], [0.6, 0.8352941176470589, 0.0], [0.8, 0.9176470588235294, 0.0], [1.0, 1.0, 0.0], [1.0, 0.9568627450980393, 0.0], [1.0, 0.9137254901960784, 0.0], [1.0, 0.8705882352941177, 0.0], [1.0, 0.8274509803921568, 0.0], [1.0, 0.7843137254901961, 0.0], [1.0, 0.7215686274509804, 0.0], [1.0, 0.6588235294117647, 0.0], [1.0, 0.596078431372549, 0.0], [1.0, 0.5333333333333333, 0.0], [1.0, 0.47058823529411764, 0.0], [1.0, 0.3764705882352941, 0.0], [1.0, 0.2823529411764706, 0.0], [1.0, 0.18823529411764706, 0.0], [1.0, 0.09411764705882353, 0.0], [1.0, 0.0, 0.0], [0.9568627450980393, 0.0, 0.0], [0.9137254901960784, 0.0, 0.0], [0.8705882352941177, 0.0, 0.0], [0.8274509803921568, 0.0, 0.0], [0.7843137254901961, 0.0, 0.0], [0.7450980392156863, 0.0, 0.0], [0.7058823529411765, 0.0, 0.0], [0.6666666666666666, 0.0, 0.0], [0.6274509803921569, 0.0, 0.0], [0.5882352941176471, 0.0, 0.0], [0.6705882352941176, 0.0, 0.2], [0.7529411764705882, 0.0, 0.4], [0.8352941176470589, 0.0, 0.6], [0.9176470588235294, 0.0, 0.8], [1.0, 0.0, 1.0], [0.9176470588235294, 0.0, 1.0], [0.8352941176470589, 0.0, 1.0], [0.7529411764705882, 0.0, 1.0], [0.6705882352941176, 0.0, 1.0], [0.5882352941176471, 0.0, 1.0]])
kw["cmap"] = mpl.colors.ListedColormap(cmaparray)
bounds = np.arange(kw["cmap"].N+1)
kw["norm"] = mpl.colors.BoundaryNorm(bounds, kw["cmap"].N)

name = "dbz"
kw = _kw(colorkw, name)
sat = 0.15
bri = 0.9
cmaparray = np.array([[sat, 0.9, 1.0], [sat+0.1, 1.0, sat], [1.0, 1.0, sat], [1.0, 0.7, sat], [1.0, sat, sat]])
cmaparray = cmaparray * bri
kw["cmap"] = mpl.colors.ListedColormap(cmaparray)
bounds = np.array([0, 15, 30, 40, 45, 50])
kw["norm"] = mpl.colors.BoundaryNorm(bounds, kw["cmap"].N)
kw["cmap"].set_over(np.array([0.7, sat, 1])*bri)
kw["cmap"].set_under(np.array([1, 1, 1]))
kw["cmap"].colorbar_extend = "both"


name = "DBZ_large"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_MPL_Spectral
bounds = np.arange(16) + 40
kw["norm"] = mpl.colors.BoundaryNorm(bounds, kw["cmap"].N)

name = "precipetation_cwb"
kw = _kw(colorkw, name)
kw["cmap"] = mpl.colors.ListedColormap(['#a0fffa','#00cdff','#0096ff','#0069ff','#329600','#32ff00','#ffff00','#ffc800', '#ff9600','#ff0000','#c80000','#a00000', '#96009b','#c800d2','#ff00f5'])
bounds = [1.,2.,6.,10.,15.,20.,30.,40.,50.,70.,90.,110.,130.,150.,200.,300.]
kw["cbticks"] = bounds
kw["cmap"].set_over(color='#ffccff')
kw["cmap"].set_under(color=(1, 1, 1))
kw["cmap"].colorbar_extend = "both"
kw["norm"] = mpl.colors.BoundaryNorm(bounds, kw["cmap"].N)

name = "VEL"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_testmap
kw["vmax"] = 30
kw["vmin"] = -30

name = "RHOHV"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_MPL_Spectral
kw["vmax"] = 1.1
kw["vmin"] = 0
kw["continuous"] = True

name = "WIDTH"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_MPL_Spectral
kw["vmax"] = 8
kw["vmin"] = 0
kw["continuous"] = True

name = "NCP"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_MPL_Spectral
kw["vmax"] = 1.1
kw["vmin"] = 0
kw["continuous"] = True

name = "ZDR"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_MPL_Spectral
kw["vmax"] = 2.5
kw["vmin"] = -0.5
kw["continuous"] = True

name = "ZDR_discrete"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_MPL_Spectral
bounds = np.arange(13)/12*3 - 0.5
kw["norm"] = mpl.colors.BoundaryNorm(bounds,kw["cmap"].N)

name = "KDP"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_MPL_Spectral
kw["vmax"] = 2.5
kw["vmin"] = -0.5
kw["continuous"] = True

name = "KDP_discrete"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_MPL_Spectral
bounds = np.arange(15)/14*3.5 - 0.5
kw["norm"] = mpl.colors.BoundaryNorm(bounds,kw["cmap"].N)

name = "rel_radial_wind"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_testmap
bounds = [-18, -15, -12, -9, -6, -4, -2, 2, 4, 6, 9, 12, 15, 18]#(np.arange(10)-4.5)*4
kw["norm"] = mpl.colors.BoundaryNorm(bounds,kw["cmap"].N)

name = "radial_wind"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_testmap
bounds = [-18, -15, -12, -9, -6, -4, -2, 2, 4, 6, 9, 12, 15, 18]#(np.arange(10)-4.5)*4
kw["norm"] = mpl.colors.BoundaryNorm(bounds,kw["cmap"].N)

name = "DIV"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_MPL_RdBu
bounds = [-30, -20,-10,-5,-2,2,5,10,20,30]
kw["norm"] = mpl.colors.BoundaryNorm(bounds,kw["cmap"].N)

name = "VOR"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_MPL_RdBu_r
bounds = [-60,-40,-25,-15,-5,5,15,25,40,60]
kw["norm"] = mpl.colors.BoundaryNorm(bounds,kw["cmap"].N)

name = "VVB"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_MPL_RdBu_r
bounds = [-10,-8,-6,-4,-2,2,4,6,8,10]
kw["norm"] = mpl.colors.BoundaryNorm(bounds,kw["cmap"].N)

name = "UyVx"
kw = _kw(colorkw, name)
kw["cmap"] = cm.bwr_r
bounds = [-20,-10,-5,-2,-0.5,0.5,2,5,10,20]
kw["norm"] = mpl.colors.BoundaryNorm(bounds,kw["cmap"].N)

name = "rel_cross_wind"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_nrl_sirkes
bounds = (np.arange(10)-4.5)*6
kw["norm"] = mpl.colors.BoundaryNorm(bounds,kw["cmap"].N)

name = "w"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_MPL_RdBu_r
bounds = [-15, -10,-5,-2,-0.5,0.5,2,5,10, 15]
kw["norm"] = mpl.colors.BoundaryNorm(bounds,kw["cmap"].N)

name = "ws"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_prcp_1[1:]
bounds = np.array([10,12,14,16,18,20,20,20,20,22,24,26,28,30,34,38,42]) - 4
kw["cbticks"] = np.array([10,12,14,16,18,20,22,24,26,28,30,34,38,42]) - 4
kw["norm"] = mpl.colors.BoundaryNorm(bounds,kw["cmap"].N)

name = "T"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_prcp_1
bounds = np.arange(15) + 280
kw["norm"] = mpl.colors.BoundaryNorm(bounds,kw["cmap"].N)

# name = "ws_small"
# kw = _kw(colorkw, name)
# kw["cmap"] = NCL_prcp_1[1:]
# bounds = np.array([10,12,14,16,18,20,20,20,20,22,24,26,28,30,34,38,42]) - 10
# kw["cbticks"] = np.array([10,12,14,16,18,20,22,24,26,28,30,34,38,42]) - 10
# kw["norm"] = mpl.colors.BoundaryNorm(bounds,kw["cmap"].N)
name = "ws_small"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_wind_17lev
bounds = np.array([10,12,14,16,18,20,22,24,26,28,30,34,38,42]) - 10
kw["norm"] = mpl.colors.BoundaryNorm(bounds,kw["cmap"].N)

name = "CFAD_DBZ"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_prcp_1
bounds = np.arange(12) * 1.0
#bounds[0] = 1e-10
kw["cbticks"] = ["{:.0f}".format(i) for i in bounds]
#kw["cbticks"][0] = ""
kw["norm"] = mpl.colors.BoundaryNorm(bounds,kw["cmap"].N)
kw["cmap"].set_over("#FFE4E1")
kw["cmap"].set_under("white")

name = "CFAD_w"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_prcp_1[1:]
bounds = np.arange(11)*2 -4.0
bounds[0] = 1e-11
bounds[1] = 0.1
bounds[2] = 0.5
kw["cbticks"] = ["", "0.1", "0.5", "2", "4", "6", "8", "10", "12", "14", "16"]
kw["norm"] = mpl.colors.BoundaryNorm(bounds,kw["cmap"].N)
kw["cmap"].set_over("#FFE4E1")


name = "CFAD_KDP"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_prcp_1[1:]
bounds = [1e-11, 0.1, 1, 5, 10, 15, 20, 30, 40, 50, 9990]
kw["cbticks"] = ["", "0.1", "1", "5", "10", "15", "20", "30", "40", "50", ""]
kw["norm"] = mpl.colors.BoundaryNorm(bounds,kw["cmap"].N)
kw["cmap"].set_over("#FFE4E1")

name = "CFAD_ZDR"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_prcp_1[1:]
bounds = [1e-11, 0.1, 1, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20, 22.5, 25]
kw["cbticks"] = ["", "0.1", "1", "", "5", "", "10", "", "15", "", "20", "", "25"]
kw["norm"] = mpl.colors.BoundaryNorm(bounds,kw["cmap"].N)
kw["cmap"].set_over("#FFE4E1")

name = "CFAD_RHOHV"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_prcp_1[1:]
bounds = [1e-11, 0.1, 1, 5, 10, 15, 20, 30, 40, 50, 9990]
kw["cbticks"] = ["", "0.1", "1", "5", "10", "15", "20", "30", "40", "50", ""]
kw["norm"] = mpl.colors.BoundaryNorm(bounds,kw["cmap"].N)
kw["cmap"].set_over("#FFE4E1")

name = "NCDR_cwv"
kw = _kw(colorkw, name)
kw["cmap"] = mpl.colors.ListedColormap(['#ffee99','#ffcc65','#ff9932','#f5691d','#fc3d3d'])
kw["cmap"].set_over(color='#d10f1b')
kw["cmap"].set_under(color='1',alpha=0)
kw["cmap"].colorbar_extend = "both"
bounds = np.arange(40,100,10)
kw["norm"] = mpl.colors.BoundaryNorm(bounds,kw["cmap"].N)

name = "NCDR_ept"
kw = _kw(colorkw, name)
kw["cmap"] = mpl.colors.ListedColormap(['#36ff01','#f8ff03','#fdcb08','#ff930c'])
kw["cmap"].set_over(color='#fa0401')
kw["cmap"].set_under(color='1',alpha=0)
kw["cmap"].colorbar_extend = "both"
bounds = np.arange(339,354,3)
kw["norm"] = mpl.colors.BoundaryNorm(bounds,kw["cmap"].N)

name = "NCDR_rh"
kw = _kw(colorkw, name)
kw["cmap"] = mpl.colors.ListedColormap(['#95ffff','#0797fa'])
kw["cmap"].set_over(color='#0166ff')
kw["cmap"].set_under(color='1',alpha=0)
kw["cmap"].colorbar_extend = "both"
bounds = np.arange(70,100,10)
kw["norm"] = mpl.colors.BoundaryNorm(bounds,kw["cmap"].N)

name = "NCDR_vorticity"
kw = _kw(colorkw, name)
kw["cmap"] = mpl.colors.ListedColormap(['#ffd2ff','#ffa5ff','#ff73ff','#ff41ff','#f100f1','#bb00bb','#870087','#540454'])
kw["cmap"].set_over(color='#300730')
kw["cmap"].set_under(color='1',alpha=0)
kw["cmap"].colorbar_extend = "both"
bounds = [1,3,5,7,9,11,14,17,20]
kw["norm"] = mpl.colors.BoundaryNorm(bounds,kw["cmap"].N)

name = "NCDR_ws"
kw = _kw(colorkw, name)
kw["cmap"] = mpl.colors.ListedColormap(['#bbf0bb','#86f586','#00f500','#00be00','#008800','#005101'])
kw["cmap"].set_over(color='#061b0a')
kw["cmap"].set_under(color='1',alpha=0)
kw["cmap"].colorbar_extend = "both"
bounds = np.arange(30,100,10)
kw["norm"] = mpl.colors.BoundaryNorm(bounds,kw["cmap"].N)

name = "ratio"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_prcp_1[:-1]
bounds = np.arange(11) * 10
#kw["cbticks"] = ["", "0.1", "1", "5", "10", "15", "20", "30", "40", "50", ""]
kw["norm"] = mpl.colors.BoundaryNorm(bounds,kw["cmap"].N)
#kw["cmap"].set_over("#FFE4E1")

name = "HM_w"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_MPL_RdBu_r[64-2*8:]
bounds = np.arange(11) * 0.25 - 0.5
kw["norm"] = mpl.colors.BoundaryNorm(bounds,kw["cmap"].N)

name = "EPT_sounding"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_WhiteBlueGreenYellowRed.copy()
kw["cmap"].set_over((0.4, 0.06, 0.08, 1.0))
bounds = np.arange(308, 351, 2)
kw["cbticks"] = []
for b in bounds:
    if (b - 304) % 6 == 0:
        kw["cbticks"].append(f"{b:.0f}")
    else:
        kw["cbticks"].append("")
kw["norm"] = mpl.colors.BoundaryNorm(bounds, kw["cmap"].N)
# kw["norm"] = mpl.colors.BoundaryNorm(bounds, kw["cmap"].N // len(bounds) * (len(bounds) - 1))

name = "terrain"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_MPL_terrain[32:]
kw["cmap"].set_under(NCL_MPL_terrain(15))
kw["cmap"].colorbar_extend = "min"
bounds = [0, 250, 500, 750, 1000, 1500, 2000, 3000, 4000]
kw["norm"] = mpl.colors.BoundaryNorm(bounds, kw["cmap"].N)

name = "lsm"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_MPL_terrain[15:33:17]
bounds = [0, 0.5, 1]
kw["norm"] = mpl.colors.BoundaryNorm(bounds, kw["cmap"].N)

name = "SST"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_cmocean_thermal
bounds = np.arange(12+1) * 1.5 + 15
kw["cmap"].colorbar_extend = "both"
kw["norm"] = mpl.colors.BoundaryNorm(bounds, kw["cmap"].N)

name = "Tgradient"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_WhiteBlue.copy()
bounds = np.arange(10) * 1e-4
kw["cmap"].colorbar_extend = "max"
kw["norm"] = mpl.colors.BoundaryNorm(bounds, kw["cmap"].N)

name = "Tperturbation"
kw = _kw(colorkw, name)
kw["cmap"] = NCL_CBR_coldhot.copy()
bounds = (np.arange(12) - 5.5) * 1.0
kw["cmap"].colorbar_extend = "both"
kw["norm"] = mpl.colors.BoundaryNorm(bounds, kw["cmap"].N)


# name = "STK"
# kw = _kw(colorkw, name)
# kw["cmap"] = NCL_MPL_hot
# bounds = np.arange(12+1) * 3
# kw["cmap"].set_over
# kw["norm"] = mpl.colors.BoundaryNorm(bounds, kw["cmap"].N)


for k in colorkw:
    kw = colorkw[k]
    #kw["cbticks"] = None
    for key in ["cmap", "cbticks", "norm", "vmax", "vmin"]:
        if key not in kw:
            kw[key] = None

if __name__ == "__main__":
    print(colorkw["SST"]["norm"].boundaries)