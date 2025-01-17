# -*- coding: utf-8 -*-
import netCDF4 as nc
import numpy as np

def getsectioninfor(ds):
    var = {}
    for key in ["lon", "lat", "s", "z", "data_coverage"]:
        var[key] = ds[key][:]
    return var

def getsectionfield(ds):
    var = {}
    for key in ds.variables:
        if len(ds[key].shape) >= 1:
            var[key] = ds[key][:]
    return var

def read_section(section_file, auto_mask = True):
    ds    = nc.Dataset(section_file)
    infor = getsectioninfor(ds)
    field = _to_mask_array(getsectionfield(ds))
    ds.close()
    if auto_mask:
        for value in field.values():
            if len(value.shape) > 1:
                add_mask(field, np.isnan(value))
                break
    return infor, field

def _to_mask_array(field_dict, keys = None, NOT_keys = []):
    if keys is None:
        keys = list(field_dict.keys())
    
    for key in keys:
        if key in NOT_keys:
            continue
        if type(field_dict[key]) is np.ndarray:
            field_dict[key] = np.ma.masked_array(field_dict[key], mask = False)
    return field_dict

def add_mask(field_dict, mask, keys = None, NOT_keys = []):
    if keys is None:
        keys = list(field_dict.keys())
    for key in keys:
        if key in NOT_keys:
            continue
        if type(field_dict[key]) is np.ma.core.MaskedArray and len(field_dict[key].shape) > 1:
            field_dict[key].mask = np.logical_or(mask, field_dict[key].mask)