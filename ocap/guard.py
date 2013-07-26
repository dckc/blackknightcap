'''guard -- decorator for soft-typing

based on `E Guards`__

__ http://wiki.erights.org/wiki/Guard

adapted from: `safelite.py`__ by tav

__ https://github.com/tav/scripts/blob/master/safelite.py

Guards can be types::

  >>> @guard(x=int)
  ... def f(x):
  ...     return x
  >>> f('junk')
  Traceback (most recent call last):
    ...
  TypeError: x ('junk') has to be int

  >>> f(10.5)
  Traceback (most recent call last):
    ...
  TypeError: x (10.5) has to be int

Or predicate functions::

  >>> @guard(x=int_ge(5))
  ... def f(x):
  ...     return x
  >>> f(1)
  Traceback (most recent call last):
    ...
  TypeError: x (1) has to be int >= 5

'''

from inspect import getargspec
from types import FunctionType


def guard(**spec):
    _marker = object()

    def __decorator(function):

        if type(function) is not FunctionType:
            raise TypeError(
                "Argument to the guard decorator is not a function.")

        func_args, _, _, _ = getargspec(function)

        def __func(*args, **kwargs):
            for i, param in enumerate(args):
                req = spec.get(func_args[i], _marker)
                if req is not _marker and not _satisfies(param, req):
                    raise TypeError(
                        "%s (%r) has to be %s" % (
                            func_args[i], param, req.__name__)
                        )
            for name, param in kwargs.iteritems():
                if name in spec and not _satisfies(param, spec[name]):
                    raise TypeError("%s (%r) has to be %s" % (
                            name, param, spec[name].__name__))
            return function(*args, **kwargs)

        __func.__name__ = function.__name__
        __func.__doc__ = function.__doc__

        return __func

    return __decorator


def _satisfies(x, req):
    return (req(x) if type(req) is FunctionType
            else type(x) is req)


def int_ge(i):
    def req(x):
        return type(x) is int and x >= i
    req.__name__ = 'int >= %d' % i
    return req


def int_in(lo, hi):
    def req(x):
        return type(x) is int and lo >= x >= hi
    req.__name__ = '%d .. hi' % (lo)
    return req
