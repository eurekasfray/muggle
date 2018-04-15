# TODO

## Proof of concept (early)

* [x] Web server
* [x] Render markdown to client
* [x] Check for default index.md if no file is specified in resource URI path
* [x] Template preprocessor

## Configuration

* [x] Repository directory (e.g. `.muggle`):
  * This directory shall contain all Muggle configuration, allowing users to keep custom settings for specific directory.
* [x] Allow users to specify the serving directory from command line (e.g. `muggle serve <directory path>`). However, if no directory is specified (i.e. `muggle serve`), then it shall serve from the current working directory.
* [x] Configuration file (e.g. ~~`muggle.json` or `.muggle/muggle.json`~~ `.muggle/config.json`): Allow users to configure muggle upon launch
  * [x] Specify location of template source files
  * [ ] Specify the default extension for a Markdown document
* [ ] ~~Template data file: Allows users to input data into template file~~
* [x] Template file: Allow users to design the look of the Markdown presentation

## Server

* [ ] Serve forever without dropping connections
  * The server's connections are randomly dropping out

## Template language

* [ ] Extend template language (logical or logicless? extensive?)
  * [ ] Treat markdown as object with
    * Name
    * Title
    * Content
    * Headings
    * Size
    * Location
    * URL
    * Table of content
    * Flow block list (i.e. a sequence of flow blocks; for example: h1, p, p, ul)
