FVI
===

Vim paired with grep.

Given a pattern and a list of files, fvi first greps the files to find which 
contain the pattern, and then opens only those files in vim. Use *N* to move to 
next occurrence of pattern and Ctrl-N to move to next file.

Install on Unix systems by running ./install. Requires Python 2.6 or later or 
Python 3.2 or later.

Arguments
---------
``fvi`` [options] *pattern* *file* [ ... ]

Optional Arguments
------------------
-h, --help         Show this help message and exit.
-w, --word         Match a word.
-i, --ignore-case  Ignore case.
-m, --magic        Treat pattern as a vim magic or grep basic regular
                   expression.
-v, --very-magic   Treat pattern as a vim very magic or grep extended
                   regular expression.
-g, --gvim         Open files in gvim.

