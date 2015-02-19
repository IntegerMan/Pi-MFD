# coding=utf-8

"""
This file contains TODO: Describe File
"""
from json import JSONEncoder, JSONDecoder
import pickle

__author__ = 'Matt Eland'

class PythonObjectEncoder(JSONEncoder, JSONDecoder):
    def default(self, obj):
        if isinstance(obj, (list, dict, str, unicode, int, float, bool, type(None))):
            return JSONEncoder.default(self, obj)
        return {'_python_object': pickle.dumps(obj)}

def as_python_object(dct):
    if '_python_object' in dct:
        return pickle.loads(str(dct['_python_object']))
    return dct