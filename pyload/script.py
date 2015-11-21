#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""The main module which contains command line program
"""

import os
import pip
import shutil
import zipfile
import argparse
import tempfile
import contextlib
import pkg_resources
from fnmatch import fnmatch

from . import DESCRIPTION, NAME
from six import b


INCLUDE = ["setuptools"]
EXCLUDE = []


@contextlib.contextmanager
def chdir(dirname):
    """A context to work in a specific directory:

    >>> with chdir(".."):
    ...   # do stuff
    """
    curdir = os.getcwd()
    try:
        os.chdir(dirname)
        yield
    finally:
        os.chdir(curdir)


@contextlib.contextmanager
def directory():
    """Create temporary directory and destroy it after use

    >>> with directory() as d:
    ...    # do stuff
    """
    temp_dir = tempfile.mkdtemp()
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)
        pass


class PyLoadBuilder(object):
    def __init__(self,
                 packages,
                 out_dir,
                 include=INCLUDE,
                 exclude=EXCLUDE,
                 single=False):
        """Create a new pyload builder object.

        :param packages: a list of valid package source (in any format
            recognized by pip)
        :param out_dir: the directory where binaries must saved in.
        :param include: a list of packages to be included in resulting
            binary that are NOT defined explicitly as requirement for the
            source packages.
        :param exclude: a list of packages/modules that should not be packed
            in the resulting binary.
        :param single: if true use packages as standalone python files
        """
        self.packages = packages
        self.out_dir = out_dir
        self.include = include
        self.exclude = exclude
        self.contents = {}
        self.single = single

        if single:
            for fname in self.packages:
                with open(fname, 'r') as f:
                    self.contents[fname] = f.read().split('\n')

    def install_packages(self, target_dir):
        """Install required packages in target_dir passed as argument"""
        cmd = ['install', '--target=%s' % (target_dir,)]
        if not self.single:
            cmd.extend(self.packages)

        cmd.extend(self.include)
        pip.main(cmd)

    def scripts(self, target_dir, binaries):
        if self.single:
            for name in self.packages:
                if not binaries or name in binaries:
                    yield (name, None, os.path.splitext(name)[0])
            return
        # add the temporary dir to the current working_set
        pkg_resources.working_set.add_entry(target_dir)

        installed = {p.project_name.lower(): p
                     for p in pkg_resources.working_set}

        for dist in [x for x in installed.values()]:
            if dist.has_metadata('entry_points.txt'):
                enabled = False
                for line in dist.get_metadata_lines('entry_points.txt'):
                    if line == "[console_scripts]":  # XXX find better way
                        enabled = True
                    elif line[0] == '[':  # stop parsing on other section
                        enabled = False
                    elif enabled and "=" in line:
                        name, pointer = [x.strip()for x in line.split("=")]
                        if binaries and name not in binaries:
                            continue
                        if ":" in pointer:
                            mod, fun = pointer.split(":")
                            yield (mod, fun, name)
                        else:
                            yield (pointer, '', name)

    def add_libraries(self, tmp, lib, compile_python=True):
        with chdir(tmp):
            # for any library in project and base library...
            for root, dirs, files in os.walk("."):
                for fname in files:

                    fname = os.path.join(root, fname)
                    # ignore if excluded
                    if any(map(lambda x: fnmatch(
                               fname, os.path.join(".", x)),
                               self.exclude)):
                        continue

                    # compile if python code
                    if compile_python:
                        if fname.endswith(".py"):
                            base = os.path.dirname(fname)
                            lib.writepy(fname, base)
                        elif fname.endswith(".pyc"):
                            continue
                    lib.write(fname)

    def add_mainpy(self, lib, mod, fun, patch=None):
        # create __main__.py which call script
        lines = []
        if patch:
            lib.write(patch, "__patch__.py")
            lines.extend([
                "try:",
                "  import __patch__",
                "except ImportError:",
                "  pass"
            ])

        if self.single:
            lines = self.contents[mod]
        else:
            lines.extend([
                "import %s" % mod
            ])

            if fun:
                lines.append("%s.%s()" % (mod, fun,))

        lib.writestr("__main__.py", b("\n".join(lines)))

    def create_binaries(
        self,
        binaries=[],
        zipmode=zipfile.ZIP_STORED,
        patch=None,
        compile_python=True,
    ):
        """Create binaries passed as argument (or all found in packages)

        :param binaries: a list of binaries to create or an empty list to
            create all binaries found in the packages.
        :param zipmode: a valid zipmode for the binary payload. By default
            use ZIP_STORED.
        :param patch: a file name where monkey patching for libraries live
        :param compile_python: a boolean which indicates if .py files should
            be compiled and added to the binary payload.
        """
        with directory() as tmp:
            # first install the required package in temporary directory
            self.install_packages(tmp)

            # extract base library
            with pkg_resources.resource_stream(
                'pyload.resources',
                'xlib.zip'
            ) as src_stream:
                with zipfile.ZipFile(src_stream) as z:
                    z.extractall(tmp)

            # for any script defined in project(s)
            for mod, fun, name in self.scripts(tmp, binaries):
                out_file = os.path.join(self.out_dir, name)

                if not os.path.exists(self.out_dir):
                    os.makedirs(self.out_dir)

                with tempfile.TemporaryFile() as f:
                    with zipfile.PyZipFile(f, 'a', zipmode) as lib:
                        self.add_libraries(tmp, lib, compile_python)
                        self.add_mainpy(lib, mod, fun, patch=patch)

                    # rewind stream to read from the beginning
                    f.seek(0)

                    # add pyload core
                    with pkg_resources.resource_stream(
                        'pyload.resources', 'pyload'
                    ) as src_stream:
                        with open(out_file, 'wb') as target_stream:
                            shutil.copyfileobj(src_stream, target_stream)

                    # fill binary with zip payload
                    with open(out_file, 'ab') as d:
                        d.write(f.read())

                os.chmod(out_file, 511)  # 0o777
                print("Successfully create binary %s" % (out_file,))


def main():
    parser = argparse.ArgumentParser(description="%s: %s" % (
        NAME, DESCRIPTION))
    parser.add_argument('arguments', type=str, nargs='+',
                        help='Packages to binarize in pip format')

    parser.add_argument('-o', '--out-dir', dest='out_dir', action='store',
                        default="./out",
                        help='The folder where resulting binaries will '
                             'stored')

    parser.add_argument('-c', '--compress', dest='compress',
                        action='store_true', default=False,
                        help='If set, the payload will be compressed.')

    parser.add_argument('-s', '--single', dest='single',
                        action='store_true', default=False,
                        help='If set, argument is threaten as standalone '
                             'python script file')

    parser.add_argument('-I', '--include', dest='include',
                        action='append', default=INCLUDE,
                        help='Packages to add to the binary which are not '
                             'defined as requirements')

    parser.add_argument('-E', '--exclude', dest='exclude',
                        action='append', default=EXCLUDE,
                        help='Glob patterns for modules/packages to be '
                             'excluded from resulting binary')

    parser.add_argument('-b', '--binary', dest='binaries',
                        action='append', default=[],
                        help='Name of the binaries to make. By default '
                             'create all binaries defined in package '
                             'and its dependencies.')

    parser.add_argument('-p', '--patch', dest='patch',
                        action='store', default=None,
                        help='Patch file to monkey patching the resulting '
                             'payload (read the docs)')

    parser.add_argument('-nC', '--no-compile', dest='compile',
                        action='store_false', default=True,
                        help='Do not compile python files during binary '
                             'creatoion.')

    args = parser.parse_args()

    if args.compress:
        zipmode = zipfile.ZIP_DEFLATED
    else:
        zipmode = zipfile.ZIP_STORED

    builder = PyLoadBuilder(
        args.arguments,
        args.out_dir,
        args.include,
        args.exclude,
        args.single)

    builder.create_binaries(
        args.binaries,
        zipmode,
        args.patch,
        args.compile)
