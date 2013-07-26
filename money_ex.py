'''money_ex -- object capability rights amplification example: simple money

cf. http://www.erights.org/elib/capability/ode/ode-capabilities.html

... let's walk through how Alice pays Bob $10. First, let's model our
initial conditions, where Alice and Bob each have a main purse of the
same currency, and Alice already has at least $10.

  >>> carolMint = Mint("Carol")
  >>> carolMint
  <Carol's mint>

  >>> aliceMainPurse = carolMint.makePurse(1000)
  >>> aliceMainPurse
  <has 1000 Carol bucks>

  >>> bobMainPurse = carolMint.makePurse(0)
  >>> bobMainPurse
  <has 0 Carol bucks>

Let's imagine that Carol (the mint owner) sends these purses as
arguments in messages to Alice and Bob respectively.

First, playing Alice, we would sprout a new purse from our main purse,
and then transfer $10 into it::

  >>> paymentForBob = aliceMainPurse.sprout()
  >>> paymentForBob
  <has 0 Carol bucks>

  >>> paymentForBob.deposit(10, aliceMainPurse)

Then, we send a foo request to Bob, providing the purse containing $10
as payment::

  bob.foo(..., paymentForBob, ...)

What might Bob's foo method look like?

  >>> def bob_foo(payment):
  ...     bobMainPurse.deposit(10, payment)

So playing Bob, we perform::

  >>> bob_foo(paymentForBob)

Our new balances are::

  >>> bobMainPurse.getBalance()
  10

  >>> aliceMainPurse.getBalance()
  990

'''

from ocap.encap import ESuite, slot, val, update
from ocap.sealing import makeBrandPair
from ocap.guard import guard, int_ge


class Mint(ESuite):
    def __new__(cls, name):
        sealer, unsealer = makeBrandPair(name)

        def __repr__(_):
            return "<%s's mint>" % name

        @guard(balance=int_ge(0))
        def makePurse(mint, balance):
            balance_ = slot(balance)

            @guard(amount=zero_to(balance_))
            def decr(amount):
                update(balance_, val(balance_) - amount)

            class Purse(ESuite):
                def __new__(cls):
                    def __repr__(_):
                        return "<has %d %s bucks>" % (val(balance_), name)

                    def getBalance(_):
                        return val(balance_)

                    def sprout(_):
                        return mint.makePurse(0)

                    def getDecr(_):
                        return sealer.seal(decr)

                    @guard(amount=int)
                    def deposit(_, amount, src):
                        # TODO: :int guard
                        unsealer.unseal(src.getDecr())(amount)
                        update(balance_, val(balance_) + amount)

                    return cls.make(__repr__, getBalance,
                                    sprout, getDecr, deposit)

            return Purse()

        return cls.make(__repr__, makePurse)


def zero_to(slot):
    '''Dynamic guard between 0 and the value of a slot

    >>> balance_ = slot(5)
    >>> @guard(amt=zero_to(balance_))
    ... def decr(amt):
    ...     update(balance_, val(balance_) - amt)

    >>> decr(3)
    >>> val(balance_)
    2
    >>> decr(3)
    Traceback (most recent call last):
      ...
    TypeError: amt (3) has to be 0..X

    '''
    def req(x):
        return type(x) is int and 0 <= x <= val(slot)
    req.__name__ = '0..X'
    return req
