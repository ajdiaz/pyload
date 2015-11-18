Internals: Understanding pyload
===============================

Pyload is composed by a number of pieces which generates, at the end,
a static binary for your python application:

* The pyload launcher binary (or *launcher*)
* The python standard library (or *xlib*)
* The pyload python helper (or *pyload*)

Basically, Pyload works in the following way:

1. First of all during the installation of pyload a launcher and a xlib is
   provided (if installed with wheels both files are part of the wheel).

2. When running pyload over your application, pyload will create a ZIP file
   which contains all libraries in xlib, and also all files declared in your
   package (including data resources of course).

3. Pyload analyzes your package trying to find console scripts. If found,
   then create a ``__main__.py`` which calls the console script and add this
   main file to the ZIP file.

4. Finally, the launcher is prepended to the ZIP file created in 2. And now,
   the ZIP is executable, since the launcher is.

At the end, the resulting binary has the following structure::

  +--------------------------------------------------+
  | pyload launcher code (compiled as static binary) |
  +--------------------------------------------------+
  |                                                  |
  |      ZIP file, including your application        |
  |                         +                        |
  |      python standard library + __main__.py       |
  |                                                  |
  +--------------------------------------------------+


Why it works?
-------------

The launcher is a static compiled binary (you can `read the C code`_ if you are
interesting in how exactly the binary works) which run python with the same
binary as target to be executed.

Python support *via*
`zipimport <https://docs.python.org/3.5/library/zipimport.html>`_ the
capability to execute ZIP files, if they contains a ``__main__.py``.

Since ELF binaries read executabl code until the byte specified in the ELF
header, we are sure that the launcher will never try to run as *machine
code* the ZIP. And also, since ZIP allows any arbitrary garbage before the
ZIP header, we known that when python try to load the result of launcher
plus ZIP file, the binary part will be ignored.

.. _`read the C code`:
  https://github.com/ajdiaz/pyload/blob/master/src/files/pyload.c-3.5.0
