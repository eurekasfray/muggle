"""
Simple WSGI web application. Built from scratch, without using
any python web framework (e.g. flask, pyramid, django).
You can use this app in combination with a server and an WSGI
interface which let this app and the server talk
"""

"""
A barebones WSGI application. Note that we need a method which
takes the environ dictionary (dictionary with environment variables)
and a function start_response with signature
start_response(status, response_headers).
"""

from pathlib import Path
from markdown2 import Markdown
from expander import Expander

class Kernel:

    def app(environ, start_response):
        # The path for the markdown file
        path = environ['PATH_INFO']

        # The current working directory
        cwd = Path.cwd()
        cwd = Path.as_posix(cwd)

        # If is root path and no path has been specified, then set the index.md file as a default fallback.
        if path == '/':
            path = 'index.md'
        # Prepare file path by removing prepending slash so that the file
        # can be opened and read successfully.
        else:
            path = path[1:]

        # The markdown file
        markdown_file = Path(path);

        if not (markdown_file.is_dir()) and markdown_file.exists() and (markdown_file.suffix == '.md' or markdown_file.suffix == '.markdown'):

            # The template file
            template_file = Path('template.html')

            if (template_file.is_dir() and not template_file.exists()):
                status = b'503 Service Unavailable'
                content = [b'503 - Something went wrong. Template file could not be found. Please provide a template.html file']
            else:
                # The markdown
                markdown = markdown_file.read_bytes()
                markdown += b'\n'
                markdowner = Markdown()
                html = markdowner.convert(markdown)

                # The template
                template = template_file.read_text()

                # Expand the content
                #expander = Expander('<html><body>Hello {\{ content \}}</body></html>', html)
                expander = Expander(template, html)
                html = expander.expand()
                html = html.encode('utf-8')

                # The return status
                status = b'200 OK'
                content = [html];
        else:
            # The return status
            status = b'404 Not Found'
            # The file could not be found
            content = [b'404 - Not found\n'];


        # The headers are a list of 2-tuples like (name, type)
        response_headers = [('Content-Type','text/html')]
        # use the start_response function to start a response
        # which will send the headers above as answer to a client's request
        start_response(status, response_headers)
        # return some content along with the headers
        # the 'b' before the string is just for sending a bytes object
        # (remember, the WSGIServer expects bytes strings as a response!)
        return content
