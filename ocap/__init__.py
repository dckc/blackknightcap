'''admin_lib -- Provide HERON policy administration independent of Web layer.

AuthorityInjection: Capability-based Security and Dependency Injection
----------------------------------------------------------------------

The `Object-capability model`__ is useful for establishing security
properties of a large system in terms of properties of the parts:

  Advantages that motivate object-oriented programming, such as
  encapsulation or information hiding, modularity, and separation of
  concerns, correspond to security goals such as `least privilege`__ and
  privilege separation in capability-based programming.

__ http://en.wikipedia.org/wiki/Object-capability_model
__ http://en.wikipedia.org/wiki/Principle_of_least_privilege

This package makes extensive use of AuthorityInjection__, which is the
use of dependency injection in service of both separation of concerns
(and hence testability) and secure composition.  See
:mod:`heron_wsgi.admin_lib.rtconfig` for details on the dependency
injection API and its use in runtime configuration.

__ http://informatics.kumc.edu/work/wiki/AuthorityInjection

The RunTime modules are trusted; they serve as a sort of powerbox.
See also integration testing below.

Unit Testing with doctest
-------------------------

Unit testing is done with :mod:`doctest`; to run the unit tests
for one module::

  $ python -m doctest medcenter.py

.. note:: You can run the tests for most (all?) of the modules in this
          package with `tests.py`, but this is a kludge that should be
          replaced by using nose__ and `--with-doctest`.

__ http://readthedocs.org/docs/nose/en/latest/

Integration Testing: running modules as scripts
-----------------------------------------------

Many of the modules in this package run from the command line.
For example::

  $ python medcenter.py somebody

It relies on an `integration-test.ini` file (see
:file:`integration-test.ini.example` and ask around for the various
unpublished details.)

.. todo:: document integration-test.ini better

To find out the command line arguments, just run::

  $ python medcenter.py

and the stacktrace should give a pretty good clue.

'''
