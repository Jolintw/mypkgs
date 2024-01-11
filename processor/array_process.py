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