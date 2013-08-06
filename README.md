# piphub: pip for GitHub

piphub is a trivial wrapper for installing Python projects from GitHub with pip.

To install:

    ln -s "$(PWD)/piphub" ~/bin/piphub

or `/usr/local/bin` or wherever you like.

Go ahead and edit SRC and INSTALL in the piphub script if you don't like my defaults
(`--user install`, repos in ~/dev/py)

Usage:

    piphub numpy cython pydata/pandas

