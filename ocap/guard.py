import sys

from inspect import getargs
from sys import _getframe as get_frame
from types import FunctionType, GeneratorType, FrameType

# ------------------------------------------------------------------------------
# guard dekorator
# ------------------------------------------------------------------------------

_marker = object()

def guard(**spec):

    def __decorator(function):

        if type(function) is not FunctionType:
            raise TypeError("Argument to the guard decorator is not a function.")

        func_args = getargs(sys.get_func_code(function))[0]
        len_args = len(func_args) - 1

        def __func(*args, **kwargs):
            for i, param in enumerate(args):
                req = spec.get(func_args[i], _marker)
                if req is not _marker and type(param) is not req:
                    raise TypeError(
                        "%s has to be %r" % (func_args[i], req)
                        )
            for name, param in kwargs.iteritems():
                if name in spec and type(param) is not spec[name]:
                    raise TypeError("%s has to be %r" % (name, spec[name]))
            return function(*args, **kwargs)

        __func.__name__ = function.__name__
        __func.__doc__ = function.__doc__

        return __func

    return __decorator
