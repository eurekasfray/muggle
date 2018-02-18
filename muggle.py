from server import WSGIServer
from kernel import Kernel

"""
host and port used in this program. host is localhost.
In this way, you can visit the service (when it is running)
in a browser at localhost:8888
Or you can visit it manually for example through
telnet localhost 8888
"""
SERVER_ADDRESS = (HOST, PORT) = '', 8888

"""
Function that builds a WSGIServer object (the gateway),
using the given server_address and the given application.
The WSGI is something in between, which lets server and
application/framework communicate. This is where the
initialization is done.
"""
def make_server(server_address, application):
    # Builds WSGIServer object
    server = WSGIServer(server_address)
    # Sets the application
    server.set_app(application)
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
    # check that there is at least a command line argument
    #if len(sys.argv) < 2:
    #    sys.exit('Provide a WSGI application object as module:callable')
    """
    the first argument (after the executable's name) is the app path
    in the format NAMEOFAPP:app
    * NAMEOFAPP is the name of the app (e.g. if you have an app called
                pyramidapp.py, NAMEOFAPP = pyramidapp)
    * app is just the word 'app'. Inside the application module, there
                must be an object called app which represents the app
    """
    #app_path = sys.argv[1]
    #app_path = 'noodle:app'
    # splits nameofthemodule and 'app'
    #module, application = app_path.split(':')
    # import the module and returns it
    #module = __import__(module)
    # gets the object 'app' from the imported module, and
    # saves a referenece to the app object in 'application'
    #application = getattr(module, application)
    # builds the WSGI server at localhost
    httpd = make_server(SERVER_ADDRESS, Kernel.app)
    # print information about the running server
    print('{server}: Serving HTTP on port {port} ...\n'.format(server=WSGIServer.SERVER_NAME,port=PORT))
    # start serving, until manually interrupted, waiting for requests
    # and serving responses by printing them in the terminal
    httpd.serve_forever()
