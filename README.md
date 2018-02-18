# Muggle, a markdown server

Muggle is a simple markdown web server written in Python. It serves rendered markdown to clients.

## Goal

- Build a markdown web server to enable [Docs as Code][docascode_article]

## Design

- Store markdown in codebase
- Serve rendered version as webpage
- rendered markdown to HTML with neatly designed theme
- Small codebase

## Why make it?

- If we can document with rendered markdown, it would be easier to read documentation, enjoy it, structure it (because we now have it's big picture)
- I love wikis because they are pleasant for viewing and reading, but they wikis are separate from code and can become out of sync.
- I wanted to make build a server. I built my first server from [Ruslan Spivak](https://ruslanspivak.com/) in his [three](https://ruslanspivak.com/lsbaws-part1/) [part](http://ruslanspivak.com/lsbaws-part2/) [series](http://ruslanspivak.com/lsbaws-part3/): *Let's Build A Web Server*. If your interested, you may want to visit [mujina93/WSGIServer][wsgiserver_github], because some code in the series are no longer compatible since the introduction of Python 3. The [mujina93/WSGIServer][wsgiserver_github] repository provides Python 3 compatible code with extensive code documentation that dives into how Ruslan's code works.

## Inspiration

* [g3doc](https://www.usenix.org/sites/default/files/conference/protected-files/srecon16europe_slides_macnamara.pdf) by Google
* [allmark](https://allmark.io/)

## Features

* Templating
* Markdown

## Roadmap

### Proof of concept (early)

* [x] Web server
* [x] Render markdown to client
* [x] Check for default index.md if no file is specified in resource URI path
* [x] Template preprocessor

### Later

* [ ] Allow users to specify the serving directory from command line (e.g. `muggle serve <directory path>`). However, if no directory is specified (i.e. `muggle serve`), then it shall serve from the current working directory.
* [ ] Server forever without dropping connections:
  * Currently connections are randomly dropping out
* [ ] Repository directory (e.g. `.muggle`):
  * This directory shall contain all custom muggle specifications, allowing users to keep custom settings for specific directory.
  * [ ] Configuration file: Allow users to configure muggle upon launch
    * [ ] Specify location of template file
  * [ ] Template file: Allow users to
* [ ] Extensive template language (logical or logicless?)
  * [ ] Treat markdown as object with
    * Name
    * Title
    * Content
    * Headings
    * Size
    * Location
    * Table of content

## Credit

* [`server.py`](https://github.com/mujina93/WSGIServer/blob/master/webserver2.py) was forked from [mujina93/WSGIServer][wsgiserver_github] in order to learn from it. I've decided not to remove it so that I may learn more about how a web server works as I continue to develop Muggle.
* [`markdown2.py`](https://github.com/trentm/python-markdown2/blob/master/lib/markdown2.py) was taken from [trentm/python-markdown2](https://github.com/trentm/python-markdown2). It is used to render Markdown to HTML.

[wsgiserver_github]: https://github.com/mujina93/WSGIServer
[docascode_article]: http://www.writethedocs.org/guide/docs-as-code/
