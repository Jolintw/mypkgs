# -*- coding: utf-8 -*-
import netCDF4 as nc
import numpy as np

def getsectioninfor(ds):
    var = {}
    for key in ["lon", "lat", "s", "z", "data_coverage"]:
        if key in ds.variables:
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

def read_sections(sectionfiles):
    """
    return: infor, field
    """
    for i_file, file in enumerate(sectionfiles):
        temp_infor, temp_field = read_section(file, auto_mask=False)
        if i_file == 0:
            infor = adddim(temp_infor)
            field = adddim(temp_field)
        else:
            infor = npappend(infor, adddim(temp_infor), axis = 0)
            field = npappend(field, adddim(temp_field), axis = 0)
    return infor, field

def read_sections_withfilter(sectionfiles, filter):
    """
    return: infor, field
    """
    for i_file, file in enumerate(sectionfiles):
        temp_infor, temp_field = read_section(file, auto_mask=False)
        if filter(temp_infor, temp_field):
            if i_file == 0:
                infor = adddim(temp_infor)
                field = adddim(temp_field)
            else:
                infor = npappend(infor, adddim(temp_infor), axis = 0)
                field = npappend(field, adddim(temp_field), axis = 0)
    return infor, field

def mean_sections(section_dict, coverage_tolerance = 0.7, to_masked_array = True):
    """
    section_dict: can be infor or field returned by read_section\n
    coverage_tolerance: mean value will be nan when not nan data ratio lower then this value
    """
    new_section_dict = {}
    for key, value in section_dict.items():
        datacoverage = value.mask|np.isnan(value.data)
        datacoverage = np.nanmean(~datacoverage, axis=0)
        meanvalue = np.nanmean(value.data, axis=0)
        meanvalue[datacoverage < coverage_tolerance] = np.nan
        new_section_dict[key] = meanvalue
    if to_masked_array:
        new_section_dict = _to_mask_array(new_section_dict)
        for key, value in new_section_dict.items():
            if len(value.shape) > 1:
                new_section_dict[key].mask = value.mask|np.isnan(value.data)
    return new_section_dict


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

def adddim(field):
    for key in field.keys():
        field[key] = np.reshape(field[key], (1,*field[key].shape))
    return field

def npappend(field1, field2, axis = 0):
    for key in field1.keys():
        field1[key] = np.append(field1[key], field2[key], axis = axis)
    return field1