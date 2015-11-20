======
Pyload
======

*Binary static generator for python apps*

Synopsis
--------

For distribution purposes many times you want to compile all your python
code into a one unique static linked binary, like other languages (i.e.
golang) does. While python do not support a native way to do this,
**pyload** can help you in that job.

Pyload is just a small binary (compiled for some architectures for now),
which simply loads a ZIP file from the same binary, and run it via
`zipimport <https://docs.python.org/3.4/library/zipimport.html>`_ module.

The python binary code (libpython) is statically linked to the pyload
binary, and required standard libraries are also provided inside the binary
too. PyLoad do not use any temporary directory to decompress ZIP, but load
files on-the-fly.

If you are interesting in knowing more about how pyload works, please read
the INTERNALS_ documentation page.

.. _INTERNALS: https://github.com/ajdiaz/pyload/blob/master/doc/INTERNALS.rst

If you have concerns about security of pyload, read the `Security Notes`_

.. _`Security Notes`:
  https://github.com/ajdiaz/pyload/blob/master/doc/SECURITY.rst


Installation
------------

Just install as any other python package::

  pip install pyload

Please note that pyload only works in i686 and x86_64 architecture on Linux
systems.


Usage
-----

Just type::

  pyload <package>

Where package could by any pip valid package, like file path, a tar.gz file,
a git repository and so on...

Other valid options are available typing ``pyload -h``.


Limitations
-----------

1. Pyload always create binaries for that package, that means that if other
   console scripts provide for any dependency of the package is declared,
   then will be created also. You can filter what binary do you want using
   ``--binary`` flag.

2. Some packages does not include some *basic* dependencies, like
   setuptools, distribute and similar. In that case pyload generate binary
   should fail. You need to add these modules by hand (because pyload only
   get dependencies from dependencies listed in the package) using
   ``--include``.

3. Some libraries and applications do not load resources from the package
   using ``pkg_resources`` package, but try to open file directly using
   ``open`` builtin. There are many reasons to avoid it in your python apps,
   but if you need to deal with it, you probably need to use the ``--patch``
   flag.

Read more in PATCHING_ and GOODPRACTICES_ documentation.

.. _PATCHING:
  https://github.com/ajdiaz/pyload/blob/master/doc/PATCHING.rst

.. _GOODPRACTICES:
  https://github.com/ajdiaz/pyload/blob/master/doc/GOODPRACTICES.rst


Contributions
-------------
Bug reports and code and documentation patches are greatly appretiated. You
can also help by using the development version of Pyload and reporting any
bugs you might encounter.

**It's important that you provide the full command argument list as well as
the output of the failing command.**

Before working on a new feature or a bug, please browse `existing issues`_ to
see whether it has been previously discussed. If the change in question is
a bigger one, it's always good to discuss before your starting working on
it.

Please for any PR or change in the code, try to follow the  `Style Guide for
Python Code (PEP8) <http://python.org/dev/peps/pep-0008/>`_.

.. _`existing issues`: https://github.com/ajdiaz/pyload/issues?state=open

License
-------
The MIT License (MIT)

Copyright (c) 2015  Andrés J. Díaz

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


.. admonition:: Note

  Some software required by pyload is conforming other licenses, check the
  license of each component to include them in your projects.
