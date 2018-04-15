# Muggle, a markdown server

Muggle is a simple Markdown web server written in Python. It serves rendered Markdown to your browser. I wrote it to _1)_ enable the practice of [Docs as Code][docascode_article]; _2)_ because I believe that having the big picture of your documentation can make documentation easier to read, more enjoyable, and easier to compose; _3)_ I wanted to build a server. I was inspired by [g3doc](https://www.usenix.org/sites/default/files/conference/protected-files/srecon16europe_slides_macnamara.pdf) by Google and [allmark](https://allmark.io/).

*Status: Unstable*

# Features

- Render markdown from a directory
- View the rendered markdown from your browser

# Build your own server

I've always wanted to make build a server. In this project, I built my first server via [Ruslan Spivak](https://ruslanspivak.com/) in his [three](https://ruslanspivak.com/lsbaws-part1/) [part](http://ruslanspivak.com/lsbaws-part2/) [series](http://ruslanspivak.com/lsbaws-part3/): *Let's Build A Web Server*. If you're interested in building your own server, you may want to visit [mujina93/WSGIServer][wsgiserver_github], because some code in the series are no longer compatible since the introduction of Python 3. The [mujina93/WSGIServer][wsgiserver_github] repository provides Python 3 compatible code with extensive code documentation explains how Ruslan's code works.

# Credit

* [`server.py`](https://github.com/mujina93/WSGIServer/blob/master/webserver2.py) was forked from [mujina93/WSGIServer][wsgiserver_github] in order to learn from it. I've decided not to remove it so that I may learn more about how a web server works as I continue to develop Muggle.
* [`markdown2.py`](https://github.com/trentm/python-markdown2/blob/master/lib/markdown2.py) was taken from [trentm/python-markdown2](https://github.com/trentm/python-markdown2). It is used to render Markdown to HTML.
* http://alexmic.net/building-a-template-engine/

[wsgiserver_github]: https://github.com/mujina93/WSGIServer
[docascode_article]: http://www.writethedocs.org/guide/docs-as-code/
