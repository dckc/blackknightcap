

def Readable(path, os_path, os_listdir, openf):
    '''
    >>> import os
    >>> Readable('.', os.path, os.listdir, open).isDir()
    True
    '''
    def isDir():
        return os_path.isdir(path)

    def exists():
        return os_path.exists(path)

    def subRdFiles():
        return (Readable(os_path.join(path, n), os_path, os_listdir, openf)
                for n in os_listdir(path))

    def subRdFile(n):
        return Readable(os_path.join(path, n), os_path, os_listdir, openf)

    def inChannel():
        return openf(path)

    def getBytes():
        return openf(path).read()

    def fullpath():
        return os_path.abspath(path)

    return edef(isDir, exists, subRdFiles, subRdFile, inChannel,
                getBytes, fullpath)


class Editable(object):
    #ro : readable;
    #subEdFiles : unit -> editable list;
    #subEdFile : string -> editable;
    #outChannel : unit -> out_channel;
    #setBytes : string -> unit;
    #mkDir : unit -> unit;
    #createNewFile : unit -> unit;
    #delete : unit -> unit;
    pass


def edef(*methods):
    '''imitate E method suite definition
    '''
    lookup = dict([(f.__name__, f) for f in methods])

    class EObj(object):
        def __getattr__(self, n):
            if n in lookup:
                return lookup[n]
            raise AttributeError(n)

    return EObj()
