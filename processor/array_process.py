# -*- coding: utf-8 -*-
import numpy as np

# n is point to the index which your array start to match the shape
# example: array.shape = (2,3) and shape = (5,2,3,4) then n = 1
# function can find n by itself but if the shape of array is repeated in the shape
# like: array.shape = (2,3) and shape = (5,2,3,2,3,5)
# then it will be better if user can specify the "n" because this function find the first "n"
def broadcast_to_any(array, shape, n = None):
    if array.shape == shape:
        return array
    
    shape_len = len(shape)
    array_len = len(array.shape)
    
    if n is None:
        for i in range(shape_len):
            if array.shape == shape[i:i+array_len]:
                n = i
                break
    if not array.shape == shape[n:n+array_len]:
        print("n is not match")
    
    new_array = broadcast_to_high(array, shape[n:])
    new_array = np.broadcast_to(new_array, shape)
    
    return new_array
        
def broadcast_to_high(array, shape):
    if array.shape == shape:
        return array
    shape_len = len(shape)
    array_len = len(array.shape)
    ind       = np.arange(shape_len, dtype=int)
    newarray  = np.broadcast_to(array, (*shape[array_len:], *shape[:array_len]))
    newarray  = np.transpose(newarray, (*ind[-array_len:], *ind[:-array_len]))
    return newarray

def in_range_mask(X, range):
    """
    X: np array\n
    range: (Xmin, Xmax)
    """
    return (X > range[0]) & (X < range[1])

def get_columns_by_2Dmask(array, mask):
    """
    array: np array with shape (..., ny, nx)\n
    mask: np bool array with shape (ny, nx)
    """
    xind, yind = np.meshgrid(np.arange(mask.shape[1], dtype=int), np.arange(mask.shape[0], dtype=int))
    xind_inmask, yind_inmask = xind[mask], yind[mask]
    return array[..., yind_inmask, xind_inmask]

if __name__ == "__main__":
    a = np.arange(4)
    print(np.arange(4))
    print("\ncopy to high axis (right hand side):")
    print(broadcast_to_high(a, (4,2)))
    print("shape =", broadcast_to_high(a, (4,2)).shape)
    print("\ncopy to low axis (right hand side):")
    print(np.broadcast_to(a, (2,4)))
    print("shape =", np.broadcast_to(a, (2,4)).shape)
    
    print(broadcast_to_any(a, (4,2)))
    print(broadcast_to_any(a, (2,4)))
    print("\ncopy to both side:")
    print(broadcast_to_any(a, (3,4,2)),"\nshape:", broadcast_to_any(a, (3,4,2)).shape)
    
    print("\nstill works when array is not 1 dim:")
    a = np.arange(4).reshape((2,2))
    print(a)
    print(broadcast_to_any(a, (3,2,2,3), n=1))
    print(broadcast_to_any(a, (3,2,2,3)).shape)