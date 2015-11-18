Patching
========
Some applications try to load resources from the package directly using
``open`` call, instead of using ``pkg_resources`` package. In that case open
is unable to locate files, because there are inside the ZIP into the binary.

In cases like this, if you cannot change the app to use ``pkg_resources``,
then Pyload offers you the option to monkey patching the offending library.
To do that, just create a python file, which import the function which
fails, and you need to rewrite it in a proper way.

For example, if the original library (called ``origlib`` in this example)
contains a method ``load_json`` like this:


.. code-block:: python

  import os
  import json

  def load_json():
    with open(os.path.join(os.path.dirname(__file__), "myfile.json")) as r:
      return json.loads(r.read())

As you can see in this example, the ``load_json`` function of the library
try to load a ``myfile.json`` file located in the same path of the library.

When you compile this code and generate the pyload binary related, this code
will fail, because ``__file__`` will point to the binary itself, and of
course there are no file named ``executable.exe/myfile.json``.

So, let's write the patch for this code, creating the following
``mypatch.py`` file:

.. code-block:: python

  import json
  import origlib
  import pkg_resources

  def _monkey_path_load_json():
    with pkg_resources.resource_stream("origlib", "myfile.json") as r:
      return json.loads(r.read())

  # monkey patching
  origlib.load_json = _monkey_path_load_json

So, when the app calls ``load_json`` of ``origlib``, it will be called
really our monkey patched version, which uses ``pkg_resources``.

Please, read the `Good Practices Guide`_ to see how to avoid this problem
when you write your code.

.. _`Good Practices Guide`:
  https://github.com/ajdiaz/pyload/blob/master/doc/GOODPRACTICES.rst


