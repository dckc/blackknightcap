'''setup -- blackknightcap package information

cribbed from http://docs.python.org/2.6/distutils/setupscript.html
'''

__author__ = 'Dan Connolly <dconnolly@kumc.edu>'
__copyright__ = '(c) 2012 University of Kansas Medical Center'
__contact__ = 'http://informatics.kumc.edu/'
__license__ = 'Apache 2'
__version__ = '0.1'

from distutils.core import setup

setup(name='blacknightcap',
      version=__version__,
      author=__author__,
      description=__doc__.split('\n')[0],
      packages=['ocap'],
      )
