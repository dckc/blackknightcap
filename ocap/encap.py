'''encap -- lexical scoping for encapsulation
'''


class ESuite(object):
    def __repr__(self):
        return '%s(...)' % self.__class__.__name__

    @classmethod
    def make(cls, *args, **kwargs):
        suite = dict(dict([(f.__name__, f) for f in args]),
                     **kwargs)
        suite_ld = dict(suite, lift_doc=lambda _: cls.lift_doc(suite))
        return type(cls.__name__, (ESuite, object), suite_ld)()

    @classmethod
    def lift_doc(cls, suite):
        for n, f in suite.items():
            setattr(cls, n, f)


def edef(*methods, **kwargs):
    '''Imitate E method suite definition.

    .. todo:: factor out overlap with `sealing.EDef`
    .. todo:: consider using a metaclass instead
    ref http://stackoverflow.com/questions/100003/what-is-a-metaclass-in-python
    '''
    lookup = dict(kwargs, **dict([(f.__name__, f) for f in methods]))
    delegate = kwargs.get('delegate', None)

    class EObj(object):
        def __getattr__(self, n):
            if n in lookup:
                return lookup[n]
            if delegate is not None:
                return getattr(delegate, n)
            raise AttributeError(n)

        def __repr__(self):
            f = lookup.get('__repr__', None)

            return f() if f else 'obj(%s)' % lookup.keys()

    return EObj()
