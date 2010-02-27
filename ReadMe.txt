pyAA wraps and extends the Microsoft Active Accessibility API. This
extension module builds with Python 2.2, SWIG 1.3.17 and MSVC. You
might need the platform SDK for some of the include files. You should
be able to say:

'python setup.py install'

and have everything you need.

'AA.py' -- is the high-level wrapper code.

'Watcher.py' -- is a wrapper for monitoring create/destroy events.

'pyAAc.i' -- is the SWIG interface file for the extension.

'tests.py' -- is a set of unit tests for the library.

'setup.py' -- is the 'distutils' setup script. I specialized the building
of the extension to control SWIG.

Modified by
Peter Parente
17 November 2004

Original by
Gary Bishop
18 February 2003
