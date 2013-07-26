'''ocap -- object capability support
====================================

The `Object-capability model`__ is useful for establishing security
properties of a large system in terms of properties of the parts:

  Advantages that motivate object-oriented programming, such as
  encapsulation or information hiding, modularity, and separation of
  concerns, correspond to security goals such as `least privilege`__ and
  privilege separation in capability-based programming.

__ http://en.wikipedia.org/wiki/Object-capability_model
__ http://en.wikipedia.org/wiki/Principle_of_least_privilege

Unit Testing with doctest
-------------------------

Unit testing is done with :mod:`doctest`; to run the unit tests
for one module::

  $ python -m doctest medcenter.py

If you have nose__ installed, you can test all modules::

  $ nosetests --with-doctest

__ http://readthedocs.org/docs/nose/en/latest/

'''
