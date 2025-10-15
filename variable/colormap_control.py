
import copy
import matplotlib as mpl
from mypkgs.variable.mycolormap import colorkw

def get_cmapdict(name, colorkw=colorkw):
    return copy.deepcopy(colorkw[name])

def add_norm(cmapdict, add_number):
    bounds = cmapdict["norm"].boundaries
    cmapdict["norm"] = mpl.colors.BoundaryNorm(bounds + add_number, cmapdict["cmap"].N)

def multiply_norm(cmapdict, mul_number):
    bounds = cmapdict["norm"].boundaries
    cmapdict["norm"] = mpl.colors.BoundaryNorm(bounds * mul_number, cmapdict["cmap"].N)

