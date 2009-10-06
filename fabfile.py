from fabric.api import local
import os

POSSIBLE_CONFIGS = {
    "local": {
        "cmd": local,
    },
}

def local():
    env.config = POSSIBLE_CONFIGS['local']

def run_commands(*commands):
    for command in commands:
        env.config['cmd'](command)

def initialize_south_svn_repo():
    """Copy security cert files needed to talk to South"""
    expected_svn_file = "~/.subversion/auth/svn.ssl.server/d8d7447008e2fea69c388d7ff0ba3448"
    local_file = os.path.join(os.path.dirname(__file__), 'resources', "svn.aeracode.org.ssl-cert")
    run_commands("if [ ! -f %s ]; then cp %s %s; fi" % (
        expected_svn_file,
        local_file,
        expected_svn_file,
    ),)

def bootstrap():
    run_commands(
        "if [ ! -d downloads ]; then mkdir downloads; fi",
        "python bootstrap.py",
    )

def buildout():
    initialize_south_svn_repo()
    run_commands("bin/buildout", )

def update_db():
    run_commands(
        "bin/django syncdb",
        "bin/django migrate",
    )

def initialize():
    bootstrap()
    buildout()
    update_db()

