FVI -- Vim paired with Grep
===========================

:Author: Ken Kundert
:Version: 1.4.0
:Released: 2021-11-10

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
Python's docutils. Also uses ack if available.

Install using::

   pip install fvi

Installs both the program an its manpage. Once installed, you can get more 
information using::

   man fvi


Configuration
-------------
The file ~/.config/fvi/settings.nt is read if it exists.  This is a NestedText_
file that can contain four settings: *vim*, *gvim*, *grep*, and *ack*.  These 
contain the commands used to invoke vim, gvim, grep, and ack.  For example::

    vim: vimx
    gvim: gvim
    grep: grep
    ack: ag

These are actually the default values.  vimx is used rather than vim so that 
copy and paste using the X11 works as expected and The Silver Searcher, ag, is 
used rather than ack.  On Ubuntu, *ack* is installed with a non-standard name, 
so if you want to use ack use::

   ack: ack-grep

.. _NestedText: https://nestedtext.org
