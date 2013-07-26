'''ocap_file -- least-privilege interaction with the filesystem

Inspired by:

  The Sash file object is quite similar to (though different from) the
  E file object, which has proven in practice to supply simple,
  intuitive, pola-disciplined interaction with the file system::

    type readable = {
         isDir : unit -> bool;
         exists : unit -> bool;
         subRdFiles : unit -> readable list;
         subRdFile : string -> readable;
         inChannel : unit -> in_channel;
         getBytes : unit -> string;
         fullPath : unit -> string;
    }


 * `How Emily Tamed the Caml`__
   Stiegler, Marc; Miller, Mark
   HPL-2006-116

__ http://www.hpl.hp.com/techreports/2006/HPL-2006-116.html

'''

from encap import ESuite


class Readable(ESuite):
    '''Wrap the python file API in the Emily/E least-authority API.

    os.path.join might not seem to need any authority,
    but its output depends on platform, so it's not a pure function.

    >>> import os
    >>> cwd = Readable('.', os.path, os.listdir, open)
    >>> cwd.isDir()
    True

    >>> x = Readable('/x', os.path, os.listdir, open)
    >>> (x / 'y').fullPath()
    '/x/y'

    Authority only goes "down" in the filesystem:

    >>> cwd.subRdFile('../uncle_file')
    ... # doctest: +ELLIPSIS
    Traceback (most recent call last):
      ...
    LookupError: Path [../uncle_file] not subordinate ...

    >>> cwd.subRdFile('/etc/passwd')
    ... # doctest: +ELLIPSIS
    Traceback (most recent call last):
      ...
    LookupError: Path [/etc/passwd] not subordinate ...

    '''
    def __new__(cls, path0, os_path, os_listdir, openf):
        path = os_path.abspath(path0)

        def isDir(_):
            return os_path.isdir(path)

        def exists(_):
            return os_path.exists(path)

        def subRdFiles(_):
            return (subRdFile(n)
                    for n in os_listdir(path))

        def subRdFile(_, n):
            there = os_path.normpath(os_path.join(path, n))
            if not there.startswith(path):
                raise LookupError(
                    'Path [%s] not subordinate to %s' % (n, path))

            return Readable(there, os_path, os_listdir, openf)

        def inChannel(_):
            return openf(path)

        def getBytes(_):
            return openf(path).read()

        def fullPath(_):
            return os_path.abspath(path)

        return cls.make(isDir, exists, subRdFiles, subRdFile, inChannel,
                        getBytes, fullPath,
                        __div__=subRdFile,
                        __trueDiv=subRdFile)


class Editable(ESuite):
    '''
    >>> import os
    >>> x = Editable('/x', os, open)
    >>> (x / 'y').ro().fullPath()
    '/x/y'

    '''
    def __new__(cls, path, os, openf):
        def _openrd(p):
            return openf(p, 'r')
        _ro = Readable(path, os.path, os.listdir, _openrd)

        def ro(_):
            return _ro

        def subEdFiles(_):
            return (subEdFile(n)
                    for n in os.listdir(path))

        def subEdFile(_, n):
            there = os.path.join(path, n)
            if not there.startswith(path):
                raise LookupError('Path does not lead to a subordinate.')

            return Editable(there, os, openf)

        def outChannel(_):
            return openf(path, 'w')

        def setBytes(_, b):
            outChannel.write(b)

        def mkDir(_):
            os.mkdir(path)

        def createNewFile(_):
            setBytes('')

        def delete(_):
            os.remove(path)

        return cls.make(ro, subEdFiles, subEdFile, outChannel,
                        setBytes, mkDir, createNewFile, delete,
                        __div__=subEdFile,
                        __trueDiv=subEdFile)


def walk_ed(top):
    '''ocap analog to os.walk for editables
    '''
    for x in _walk(top, lambda ed: ed.subEdFiles()):
        yield x


def walk_rd(top):
    '''ocap analog to os.walk
    '''
    for x in _walk(top, lambda ed: ed.subRdFiles()):
        yield x


def _walk(top, sub_files):
    '''ocap analog to os.walk
    '''
    subs = [(sub, sub.ro().isDir())
            for sub in sub_files(top)]
    dirs = [s for (s, d) in subs if d]
    nondirs = [s for (s, d) in subs if not d]

    yield top, dirs, nondirs

    for subd in dirs:
        for x in _walk(subd, sub_files):
            yield x


def relName(ed, anc):
    '''Get the name of an Editable relative to an ancestor.
    '''
    apath = anc.ro().fullPath()
    epath = ed.ro().fullPath()
    assert(epath.startswith(apath))
    return epath[len(apath) + 1:]


def relName_rd(rd, anc):
    '''Get the name of a Readable relative to an ancestor.
    '''
    apath = anc.fullPath()
    path = rd.fullPath()
    assert(path.startswith(apath))
    return path[len(apath) + 1:]
