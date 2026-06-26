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