#!/usr/bin/env python
"""piphub - shortcut for quick installs from GitHub

`name` only needs to be specified if it differs from `repo`,
If the organization, repo, and name all have the same value (e.g. ipython, numpy, cython),
then you can just specify the one name:

    piphub ipython numpy cython pydata/pandas jtriley/StarCluster/starcluster

If a package is already checked out, it will be updated in place.

You can write and edit the default config file with:

    piphub --config
"""

import argparse
import json
import os
import sys
from subprocess import check_call
from contextlib import contextmanager

pjoin = os.path.join

CONFIG_FILE = os.path.expanduser("~/.piphub")
# the base install command.
INSTALL = ['pip', 'install']

in_env = 'VIRTUAL_ENV' in os.environ


default_config = {
    # where packages will be installed
    'src' : os.path.expanduser(pjoin('~', 'dev', 'py')),
    'pip' : 'pip',
    # can be https, git, http
    'protocol' : 'https',
    # whether to use `--user`.
    # the default is True unless in a virtualenv
    'user' : not in_env,
}

@contextmanager
def cd(path):
    """context manager for running a block with a particular cwd"""
    cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(cwd)

def load_config():
    """load config"""
    cfg = {}
    cfg.update(default_config)
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            cfg.update(json.load(f))
    return cfg

def call(cmd):
    print(' '.join(cmd))
    check_call(cmd)

def piphub(org, repo, name, cfg):
    """install project from piphub"""
    src = cfg['src']
    if not os.path.exists(src):
        os.makedirs(src)
    
    install = [cfg['pip'], 'install']
    if cfg['user']:
        install.append('--user')
    
    dest = os.path.join(src, repo)
    if os.path.exists(dest):
        update(dest, install)
        return
    proto = cfg['protocol']
    url = "git+{proto}://github.com/{org}/{repo}.git#egg={name}".format(**locals())
    cmd = install + ['--src', src, '-e' , url]
    call(cmd)

def update(path, install):
    """update an existing repo"""
    print("upgrading %s" % path)
    with cd(path):
        call(['git', 'pull'])
        call(install + ['-e', '.'])

def write_config():
    """write the default config file"""
    cfg = load_config()
    with open(CONFIG_FILE, 'w') as f:
        json.dump(cfg, f, indent=1)
    print("wrote default config to: %s" % CONFIG_FILE)

def list_packages(src, status=False):
    print("listing packages in %s" % src)
    for pkg in os.listdir(src):
        pkgdir = pjoin(src, pkg)
        if os.path.isdir(pjoin(pkgdir, '.git')) \
            and os.path.isfile(pjoin(pkgdir, 'setup.py')):
            print(pkg)
            if status:
                with cd(pkgdir):
                    check_call(['git', 'log', '-1', '--format=  %h [%ar] %s'])
    

def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    cfg = load_config()
    
    class UserAction(argparse.Action):
        def __call__(self, *args, **kwargs):
            cfg['user'] = True
    
    class NoUserAction(argparse.Action):
        def __call__(self, *args, **kwargs):
            cfg['user'] = False
    
    parser.add_argument("--user", action=UserAction, nargs=0,
        help="""do a `--user` install"""
    )
    parser.add_argument("--no-user", action=NoUserAction, nargs=0,
        help="""don't do a `--user` install"""
    )
    parser.add_argument("packages", type=str, nargs='*',
        help="""the packages to install"""
    )
    parser.add_argument("--src", type=str,
        help="the pip source directory"
    )
    parser.add_argument("--config", action='store_true', dest='write_config',
        help="write the default config file to ~/.piphub"
    )
    parser.add_argument("--list", action='store_true',
        help="list piphub packages",
    )
    parser.add_argument("--status", action='store_true',
        help="list piphub packages and show their status",
    )
    
    args = parser.parse_args()
    if args.write_config:
        write_config()
        sys.exit(0)
    
    if args.src:
        cfg['src'] = args.src
    
    if args.list:
        list_packages(cfg['src'], False)
        sys.exit(0)
    
    if args.status:
        list_packages(cfg['src'], True)
        sys.exit(0)
    
    if not args.packages:
        parser.print_help()
        sys.exit(1)
    
    for pkg in args.packages:
        slashes = pkg.count('/')
        if slashes == 0:
            org = repo = name = pkg
        elif slashes == 1:
            org, repo = pkg.split('/')
            name = repo
        elif slashes == 2:
            org, repo, name = pkg.split('/')
        else:
            print ("Unrecognized repo: %s" % pkg)
            sys.exit(1)
        
        piphub(org, repo, name, cfg)

if __name__ == '__main__':
    main()
