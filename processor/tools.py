import numpy as np

def sort_list_by_another_list(list_to_sort, ref_list):
    inds   = [ind for _,ind in sorted(zip(ref_list, list(range(len(list_to_sort)))))]
    result = [list_to_sort[ind] for ind in inds]
    return result

def indexing_dict(dict_of_data, index, varname_list = None):
    if varname_list is None:
        varname_list = [varname for varname in dict_of_data]
    new_dict = {}
    for varname in varname_list:
        var = dict_of_data[varname]
        if isinstance(var, np.ndarray):
            new_dict[varname] = var[index]
        elif isinstance(var, list):
            new_dict[varname] = [var[i] for i in index]
        else:
            new_dict[varname] = var
    return new_dict

def in_angle_range(angle, angle_range, angle_unit = "radius", angle_range_unit = "radius"):
    if angle_unit == "degree" or angle_unit == "deg":
        angle = angle / 180 * np.pi
    elif angle_unit == "radius" or angle_unit == "rad":
        pass
    else:
        print("wrong angle_unit:", angle_unit)

    if angle_range_unit == "degree" or angle_range_unit == "deg":
        angle_range = [ar / 180 * np.pi for ar in angle_range]
    elif angle_range_unit == "radius" or angle_range_unit == "rad":
        pass
    else:
        print("wrong angle_range_unit:", angle_range_unit)

    if angle_range[1] < angle_range[0]:
        result = (in_angle_range(angle, angle_range=[0, angle_range[1]]) or in_angle_range(angle, angle_range=[angle_range[0], 2*np.pi]))
    else:
        result = (angle <= angle_range[1]) and (angle >= angle_range[0])
    return result