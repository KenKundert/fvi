FVI -- Vim paired with Grep
===========================

:Author: Ken Kundert
:Version: 1.3.0
:Released: 2020-04-16

Given a pattern and a list of files, **fvi** first runs *grep* on the given 
files to find which contain the pattern, and then opens only those files in 
*vim*. Within *vim* use *n* to move to next occurrence of pattern and *Ctrl-n* 
to move to next file. *vim* is run with *autowrite* set. Any directories, 
unreadable files, or binary files in the file list are ignored.

If no file list is given on the command line, **fvi** then uses *ack* rather 
than *grep* to find which files contain the pattern. Generally *ack* will look 
at all regular files in the current working directory and all subdirectories, 
however this can be controlled using .ackrc files.

Arguments
---------

``fvi`` [options] *pattern* [*file* [ *file* ... ]]

Options
-------

-h, --help         Show this help message and exit.
-w, --word         Match a word.
-i, --ignore-case  Ignore case.
-m, --magic        Treat pattern as a vim magic or grep basic regular
                   expression.
-v, --very-magic   Treat pattern as a vim very magic or grep extended
                   regular expression.
-g, --gvim         Open files in gvim.


Installation
------------

Runs only on Unix systems.  Requires Python 3.5 or later.  It also requires 
Python's docutils. Also uses ack if available. Install using::

   pip install fvi

Installs both the program an its manpage. Once installed, you can get more 
information using::

   man fvi


Configuration
-------------
You can use the VIM, GVIM, GREP, and ACK environment variables to control which 
versions of these programs should be used. By default, VIM=vim, GVIM=gvim, 
GREP=grep, and ACK=ack.  For example, if you wish to replace ack with The Silver 
Searcher, add the following to your .bashrc file::

   export ACK=ag

On Ubuntu, *ack* is installed with a non-standard name, so you will want to 
put::

   export ACK=ack-grep

into your ~/.bashrc file.

If you wish to use the Silver Searcher to replace ack, use::
. You will need to modify the *fvi* file and replace ``ack`` with ``ack-grep`` 
to address this issue.
