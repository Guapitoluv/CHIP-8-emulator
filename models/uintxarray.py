from typing import Self
import numpy as np

class UIntXArray(np.ndarray):
    def __array_finalize__(self, obj):
        if obj is None: 
            return
        self.info = getattr(obj, 'info', None)
    
    @staticmethod
    def _set_input_array(input_data, dtype):
        if isinstance(input_data, (int, float, np.integer)):
            size = int(input_data)
            return np.zeros(size, dtype=dtype)
        else:
            return np.asarray(input_data, dtype=dtype)


class UInt8Array(UIntXArray):
    def __new__(cls, input_data, info=None):
        input_array = cls._set_input_array(input_data, np.uint8)
        obj = input_array.view(cls)
        obj.info = info
        return obj


class UInt16Array(UIntXArray):
    def __new__(cls, input_data, info=None):
        input_array = cls._set_input_array(input_data, np.uint16)
        obj = input_array.view(cls)
        obj.info = info
        return obj