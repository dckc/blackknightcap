'''sealing -- E's Rights Amplification mechanism

From  `Rights Amplification section of ELib: Inter-Object Semantics`__:

  Sealer/unsealer pairs are similar in concept to public/private key
  pairs. The sealer is like an encryption key, and the unsealer like a
  decryption key. The provided primitive, makeBrandPair, makes and
  returns such a pair. When the sealer is asked to seal an object it
  returns an envelope which can only be unsealed by the corresponding
  unsealer.

__ http://www.erights.org/elib/capability/ode/ode-capabilities.html#rights-amp

.. note:: This probably doesn't provide all of the security properties
          it's supposed to due to python's stack introspection
          mechanisms.

See also:
  * `javadoc for org.erights.e.elib.sealing`__
  * `Sealers and Unsealers on the ERights Wiki`__

__ http://www.erights.org/javadoc/org/erights/e/elib/sealing/package-summary.html
__ http://wiki.erights.org/wiki/Walnut/Secure_Distributed_Computing/Capability_Patterns#Sealers_and_Unsealers

'''

__author__ = 'Dan Connolly'
__contact__ = 'http://informatics.kumc.edu/'
__copyright__ = 'Copyright (c) 2011 Univeristy of Kansas Medical Center'
__license__ = 'Apache 2'
__docformat__ = "restructuredtext en"

def makeBrandPair(nickname):
    '''Returns a Sealer/Unsealer pair
    identified with a new unique brand of the specified (non-unique) name.
    
      >>> s, u = makeBrandPair('bob')
      >>> s
      <bob sealer>
      >>> u
      <bob unsealer>
      >>> x = s.seal('abc')
      >>> x
      <bob sealed box>
      >>> u.unseal(x)
      'abc'

      >>> ss, uu = makeBrandPair('evil')
      >>> uu.unseal(x)
      Traceback (most recent call last):
      ...
      UnsealingException

    '''

    noObject = object()
    # python closures are read only, so we close over a mutable list.
    shared = [noObject]

    def makeSealedBox(obj):
        # python lambda expressions can't contain statements,
        # so we define an auxiliary function
        def _shareContent():
            shared[0] = obj
        box = EDef(shareContent = _shareContent,
                   __repr__ = lambda: '<%s sealed box>' % nickname
                   )
        return box

    sealer = EDef(
        seal = makeSealedBox,
        __repr__ = lambda: '<%s sealer>' % nickname
        )

    def _unseal(box):
        shared[0] = noObject
        box.shareContent()
        if (shared[0] is noObject): raise UnsealingException
        contents = shared[0]
        shared[0] = noObject
        return contents

    unsealer = EDef(unseal = _unseal,
                    __repr__ = lambda: '<%s unsealer>' % nickname
                    )

    return (sealer, unsealer)


class UnsealingException(Exception):
    pass

class EDef:
    '''Imitate e object definition using 'anonymous' python classes.

    ack: `The Python IAQ: Infrequently Answered Questions`__
    by Peter Norvig

    __ http://norvig.com/python-iaq.html

    Note the use of old-style classes.
    '''
    def __init__(self, **entries): self.__dict__.update(entries)

    def __repr__(self):
        args = ['%s=%s' % (k, repr(v)) for (k,v) in vars(self).items()]
        return '<%s>' % ', '.join(args)
