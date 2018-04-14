import os
import sys
import argparse

from pathlib import Path
from server import WSGIServer
from app import Kernel
from config import Config

"""
Function that builds a WSGIServer object (the gateway),
using the given server_address and the given application.
The WSGI is something in between, which lets server and
application/framework communicate. This is where the
initialization is done.
"""
def make_server(server_address, application, config):
    # Builds WSGIServer object
    server = WSGIServer(server_address)
    # Sets the application
    server.set_app(application)
    # Set the config
    server.set_config(config)
    # Return 'server': the WSGIServer object
    return server

"""
Main program. Execute if this module is run as main file.
[__name__ == '__main__']
When the Python interpreter reads a source file,
it executes all of the code found in it.
Before executing the code, it will define a few special variables.
For example, if the python interpreter is running that module
(the source file) as the main program, it sets the special __name__
variable to have a value "__main__".
If this file is being imported from another module, __name__ will be
set to the module's name.
"""
if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        usage="%(prog)s [--version] [--help] option",
        description="Serve rendered Markdown from a directory to your browser client."
        )
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("-v", "--version",
        help="print Muggle version",
        action="store_true"
        )
    group.add_argument("--init",
        help="create new repository in PATH. If no PATH is supplied, then the new repository is initialized in current working directory.",
        metavar="PATH",
        nargs="?",
        const=os.getcwd()
        )
    group.add_argument("--serve",
        help="serve Markdown from PATH. If no PATH is supplied, then the Markdown is served from the current working directory.",
        metavar="PATH",
        nargs="?",
        const=os.getcwd()
        )

    CONFIG_FILE_NAME = 'config.json'

    args = parser.parse_args()
    if args.init:
        working_dir = args.init
        config = Config(CONFIG_FILE_NAME, working_dir)
        repo_dir = config.rd()
        if (repo_dir.is_dir() and repo_dir.exists()):
            sys.exit( "Muggle repository already exists in \"{working_directory}\"".format(working_directory=os.fspath(repo_dir.parent)) )
        else:
            repo_dir.mkdir()
            sys.exit( "Initialized empty Muggle in \"{repo_dir}\"".format(repo_dir=os.fspath(repo_dir)) )
    elif args.serve:
        working_dir = args.serve
        config = Config(CONFIG_FILE_NAME, working_dir)
        httpd = make_server(config.server_address(), Kernel.app, config)
        # print information about the running server
        print('{server}: Serving HTTP on port {port} ...\n'.format(server=WSGIServer.SERVER_NAME,port=config.server_port()))
        # start serving, until manually interrupted, waiting for requests
        # and serving responses by printing them in the terminal
        httpd.serve_forever()
    elif args.version:
         # display machine-friendly version information
        print(' '.join([ WSGIServer.SERVER_NAME, WSGIServer.VERSION_STRING ]))
    else:
        parser.print_help()
