#!/usr/bin/env python

import pyload as project

import os
from setuptools import setup
from setuptools import find_packages

from setuptools.command.install import install


class MakefileInstall(install):
    def _run_makefile(self):
        bpath = os.path.join(os.path.dirname(__file__), "src")
        ret = os.system("cd " + bpath + " && make")
        if ret != 0:
            raise SystemExit("Unable to make pyload code")

    def initialize_options(self):
        install.initialize_options(self)

    def run(self):
        self._run_makefile()
        install.run(self)


def get_file_content(fname):
    try:
        return open(fname).read()
    except:
        return None


setup(
    name=project.NAME,
    version=project.VERSION,
    description=project.DESCRIPTION,
    author=project.AUTHOR_NAME,
    author_email=project.AUTHOR_EMAIL,
    url=project.URL,
    packages=find_packages(),
    install_requires=["six==1.10.0", "pip>=7.1.2"],
    license=project.LICENSE,
    entry_points={
        'console_scripts': [
            '%s = %s.script:main' % (project.NAME, project.NAME,),
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: C'
    ],
    include_package_data=True,
    cmdclass={'install': MakefileInstall},
)
