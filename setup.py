#-----------------------------------------------------------------------------
#  Copyright (C) 2013 Min RK
#
#  Distributed under the terms of the 2-clause BSD License.
#-----------------------------------------------------------------------------

import os
import sys
import platform

from distutils.core import setup

setup_args = dict(
    name = "piphub",
    version = '0.0.2',
    py_modules = ["piphub"],
    scripts = ["piphub"],
    author = "Min Ragan-Kelley",
    author_email = "benjaminrk@gmail.com",
    url = 'http://github.com/minrk/piphub',
    download_url = 'http://github.com/minrk/piphub/releases',
    description = "Shortcuts for installing packages from GitHub",
    long_description = "",
    license = "BSD",
    classifiers = [
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ],
)

setup(**setup_args)

