Good practices
==============

1. Use ``pkg_resources`` to get streams of data into your project, instead
   to read them using ``open`` and ``__file__``. You have a good explanation
   of why in `PATCHING`_ document.

2. Declare all required dependencies in ``setup.py`` or *requirements.txt*
   file. Pyload will also add some dependencies for you, like
   ``setuptools``.

3. Try to import modules using relative import for modules/packages in your
   package. If not possible be sure that the module that you import is
   declared as dependency for your application.


.. _PATCHING: https://github.com/ajdiaz/pyload/blob/master/doc/PATCHING.rst
