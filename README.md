# piphub: pip wrapper for GitHub

piphub is a trivial wrapper for doing developer installs of Python projects from GitHub with pip.

To install:

    pip install piphub

or:

    ln -s "$(PWD)/piphub.py" ~/bin/piphub

or:

    curl -L https://raw.github.com/minrk/piphub/master/piphub.py > ~/bin/piphub

or `/usr/local/bin` or wherever you like.

Run `piphub --config` and edit `~/.piphub` if you don't like my defaults
(`--user install`, repos in ~/dev/py)

Usage:

    piphub numpy cython pydata/pandas

All it does is expand the command, so:

    piphub numpy
    
is really just

    pip install --src ~/dev/py -e git+https://github.com/numpy/numpy#egg=numpy
