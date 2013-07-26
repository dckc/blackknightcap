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

__ http://www.erights.org/javadoc/org/erights/e/elib/sealing/package-summary.html  # noqa
__ http://wiki.erights.org/wiki/Walnut/Secure_Distributed_Computing/Capability_Patterns#Sealers_and_Unsealers  # noqa

'''

__author__ = 'Dan Connolly'
__contact__ = 'http://informatics.kumc.edu/'
__copyright__ = 'Copyright (c) 2011 Univeristy of Kansas Medical Center'
__license__ = 'Apache 2'
__docformat__ = "restructuredtext en"

from encap import ESuite, slot, val, update


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
      TypeError: invalid box

    '''

    noObject = object()
    shared = slot(noObject)

    class SealedBox(ESuite):
        def __new__(cls, obj):
            def __repr__(_):
                return '<%s sealed box>' % nickname

            def shareContent(_):
                update(shared, obj)

            return cls.make(__repr__, shareContent)

    class Sealer(ESuite):
        def __new__(cls):
            def __repr__(_):
                return '<%s sealer>' % nickname

            def seal(_, obj):
                return SealedBox(obj)

            return cls.make(__repr__, seal)

    class Unsealer(ESuite):
        def __new__(cls):
            def __repr__(_):
                return '<%s unsealer>' % nickname

            def unseal(_, box):
                update(shared, noObject)
                box.shareContent()
                if (val(shared) is noObject):
                    raise TypeError('invalid box')
                contents = val(shared)
                update(shared, noObject)
                return contents

            return cls.make(__repr__, unseal)

    return (Sealer(), Unsealer())
