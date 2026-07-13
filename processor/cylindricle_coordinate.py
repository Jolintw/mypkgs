import numpy as np
from mypkgs.processor.numericalmethod import RightAngleInterpolater
from mypkgs.processor.geometry import vector_by_angle_length

def create_cylindricle(phi_n, r_intv, r_max, center_x, center_y):
    cyl = {}
    cyl["phi_1D"] = np.arange(phi_n) / 180 * np.pi
    cyl["r_1D"] = np.arange(r_intv, r_max+r_intv, r_intv)
    cyl["phi"], cyl["r"] = np.meshgrid(cyl["phi_1D"], cyl["r_1D"])
    cyl["x"], cyl["y"] = vector_by_angle_length(angle=cyl["phi"], length=cyl["r"])
    cyl["x"], cyl["y"] = cyl["x"] + center_x, cyl["y"] + center_y
    return cyl
    

def create_cylindricle_interpolate_data(x, y, data, var_to_interpolate, phi_n, r_intv, r_max, center_x, center_y):
    cyl = create_cylindricle(phi_n, r_intv, r_max, center_x, center_y)
    RAI = RightAngleInterpolater(X=(y, x), newX=(cyl["y"], cyl["x"]), equidistance=True)
    for var in var_to_interpolate:
        cyl[var] = RAI.interpolate(data[var])
    return cyl