FVI
===

Vim paired with grep.

Given a pattern and a list of files, **fvi** first runs *grep* on the given 
files to find which contain the pattern, and then opens only those files in 
*vim*. Use *N* to move to next occurrence of pattern and *Ctrl-N* to move to 
next file. *vim* is run with *autowrite* set. Any directories, unreadable files, 
or binary files in the file list are ignored.

If no file list is given on the command line, **fvi** then uses *ack* rather 
than *grep* to find which files contain the pattern. Generally *ack* will look 
at all regular files in the current working directory and all subdirectories, 
however this can be controlled using .ackrc files.

Install on Unix systems by running ./install.  Requires Python 2.6 or later or 
Python 3.2 or later.

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
