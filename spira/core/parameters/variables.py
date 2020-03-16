import numpy as np
import networkx as nx
from spira.core.parameters.restrictions import RestrictType, RestrictRange
from spira.core.parameters.descriptor import RestrictedParameter


NUMBER = RestrictType((int, float, np.int32, np.int64, np.float))
FLOAT = RestrictType((float, np.float))
INTEGER = RestrictType((int, np.int32, np.int64))
COMPLEX = RestrictType(complex) & NUMBER
STRING = RestrictType(str)
BOOL = RestrictType(bool)
DICTIONARY = RestrictType(dict)
LIST = RestrictType(list)
TUPLE = RestrictType(tuple)
NUMPY_ARRAY = RestrictType(np.ndarray)
GRAPH = RestrictType(nx.Graph)


# class NumberParameter:
#     def __new__(cls, restriction=None, **kwargs):
#         if 'default' not in kwargs:
#             kwargs['default'] = 0
#         R = NUMBER & restriction
#         return RestrictedParameter(restriction=R, **kwargs)


def NumberParameter(restriction=None, **kwargs):
    if 'default' not in kwargs:
        kwargs['default'] = 0
    R = NUMBER & restriction
    return RestrictedParameter(restriction=R, **kwargs)


def ComplexParameter(restriction=None, **kwargs):
    if 'default' not in kwargs:
        kwargs['default'] = 0

    R = COMPLEX & restriction
    return RestrictedParameter(restriction=R, **kwargs)


def IntegerParameter(restriction=None, preprocess=None, **kwargs):
    if 'default' not in kwargs:
        kwargs['default'] = 0
    R = INTEGER & restriction
    # P = preprocess
    # return RestrictedParameter(restriction=R, preprocess=P, **kwargs)
    return RestrictedParameter(restriction=R, **kwargs)


def FloatParameter(restriction=None, **kwargs):
    if 'default' not in kwargs:
        kwargs['default'] = 0.0
    R = FLOAT & restriction
    return RestrictedParameter(restriction=R, **kwargs)


def StringParameter(restriction=None, **kwargs):
    if 'default' not in kwargs:
        kwargs['default'] = ''
    R = STRING & restriction
    return RestrictedParameter(restriction=R, **kwargs)


def BoolParameter(restriction=None, **kwargs):
    if 'default' not in kwargs:
        kwargs['default'] = False
    R = BOOL & restriction
    return RestrictedParameter(restriction=R, **kwargs)


def ListParameter(restriction=None, **kwargs):
    if 'default' not in kwargs:
        kwargs['default'] = []
    R = LIST & restriction
    return RestrictedParameter(restriction=R, **kwargs)


def TupleParameter(restriction=None, **kwargs):
    if 'default' not in kwargs:
        kwargs['default'] = []
    R = TUPLE & restriction
    return RestrictedParameter(restriction=R, **kwargs)


def DictParameter(local_name=None, restriction=None, **kwargs):
    if 'default' not in kwargs:
        kwargs['default'] = {}
    R = DICTIONARY & restriction
    return RestrictedParameter(local_name, restriction=R, **kwargs)


def NumpyArrayParameter(restriction=None, **kwargs):
    if 'default' not in kwargs:
        kwargs['default'] = np.array([])
    R = NUMPY_ARRAY & restriction
    return RestrictedParameter(restriction=R, **kwargs)


def GraphParameter(restriction=None, **kwargs):
    if 'default' not in kwargs:
        kwargs['default'] = nx.Graph()
    R = GRAPH & restriction
    return RestrictedParameter(restriction=R, **kwargs)


def TimeParameter(local_name=None, restriction=None, **kwargs):
    import time
    if not 'default' in kwargs:
        kwargs['default'] = time.time()
    R = NUMBER & restriction
    return RestrictedParameter(local_name, restriction=R, **kwargs)