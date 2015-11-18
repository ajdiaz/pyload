Security notes
==============

Ofuscate code
-------------
Pyload is intented to be a way to distribute your app without dependencies,
but it's not designed to ofuscate your code.

All the python files (compiled and in plain text) are included in the binary
as ZIP file. So is easy to extract them. You can ofuscate your code using
any ofuscate library available for python or compile to python object
(*pyo*) and remove references to source code.

Environmental variables
-----------------------
Pyload start ``PyMain()``, so any environmental variable understable by
python will be recognized by Pyload, like ``PYTHONVERBOSE`` or similar.
