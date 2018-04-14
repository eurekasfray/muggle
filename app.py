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

import os
from pathlib import Path
from markdown2 import Markdown
from preprocessor import Preprocessor

class Kernel:

    def app(environ, start_response, config):
        # The path for the markdown file
        path = environ['PATH_INFO']

        # If is root path and no path has been specified, then set the index file as a default fallback.
        if path == '/':
            path = config.index_file_name()
        # Prepare file path by removing prepending slash so that the file
        # can be opened and read successfully.
        else:
            path = path[1:]

        # The markdown file
        markdown_path = config.wd().joinpath(path);

        if not (markdown_path.is_dir()) and markdown_path.exists() and (markdown_path.suffix == '.md' or markdown_path.suffix == '.markdown'):

            # The template file
            template_path = config.template_file_path()

            if (template_path.is_dir() and not template_path.exists()):
                status = b'503 Service Unavailable'
                content = [b'503 - Something went wrong. Template file could not be found. Please provide a template.html file']
            else:
                # The markdown
                markdown = markdown_path.read_bytes()
                markdown += b'\n'
                markdowner = Markdown()
                html = markdowner.convert(markdown)

                # The template
                template = template_path.read_text()

                # Expand the content
                preprocessor = Preprocessor(template, html)
                html = preprocessor.process()
                html = html.encode('utf-8')

                # The return status
                status = '200 OK'
                content = [html]
        else:
            # If index file could not be found, report it.
            if markdown_path.name == config.index_file_name():
                print(
                    "Could not find the directory index file to display. "
                    "Provide a directory index file by saving a file as "
                    "\"{index_file_name}\"".format(index_file_name=config.index_file_name())
                    )

            # The return status
            status = '404 Not Found'
            # The file could not be found.
            if not config.notfound_file_path().is_dir() and config.notfound_file_path().exists():
                html = config.notfound_file_path().read_text()
                html = html.encode('utf-8')
                content = [html]
            # Oh the irony... The 404 error template could not be found, so send hand-written (app generated) error message.
            else:
                content = [
                    b"<h1>404 Not Found</h1>"
                    b"<p>The page you're looking for could not be found.</p>"
                    ]


        # The headers are a list of 2-tuples like (name, type)
        response_headers = [('Content-Type','text/html')]
        # use the start_response function to start a response
        # which will send the headers above as answer to a client's request
        start_response(status, response_headers)
        # return some content along with the headers
        # the 'b' before the string is just for sending a bytes object
        # (remember, the WSGIServer expects bytes strings as a response!)
        return content
