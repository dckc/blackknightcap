'''admin_lib -- Provide HERON policy administration independent of Web layer.

Unit Testing
------------

Unit testing is done with :mod:`doctest`; to run the unit tests
for one module::

  $ python -m doctest medcenter.py

.. note:: You can run the tests for most (all?) of the modules in this
          package with `tests.py`, but this is a kludge that should be
          replaced by `nosetests`.

Integration Testing
-------------------

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
