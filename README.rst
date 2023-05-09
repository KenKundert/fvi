FVI — Vim paired with Grep
==========================

:Author: Ken Kundert
:Version: 2.2
:Released: 2023-03-18

Opens files that contains a given pattern in *vim*.  You may specify 
a collection of files to search, otherwise all files in the current working 
directory and all sub directories are searched.

Within *vim* use *n* to move to next occurrence of pattern. *Ctrl-n* moves to 
next file and *ctrl-p* moves to the previous file.  *vim* is run with 
*autowrite* set.  Any directories, unreadable files, or binary files in the file 
list are ignored.

The pattern is a literal text string.  Regular expressions are not supported.

Use -- to terminate the command line options.
Any thing that follows -- is treated as the pattern.
You can search for patterns that start with - by preceding the pattern with --.


Arguments
---------

``fvi`` [options] [--] *pattern* [*file* ... ]


Options
-------

-i, --ignore-case     ignore case
-w, --word            match a word
-o, --only <glob>     a glob string used to specify desired files,
                      can use brace expansion to specify multiple globs
-e, --exclude <glob>  a glob string used to filter out unwanted files,
                      can use brace expansion to specify multiple globs
-H, --hidden          include hidden files
-b, --binary          do not skip binary files (any not encoded in ascii or utf-8)
-g, --gvim            open files in gvim rather than vim
-v, --vim             open files in vim rather than gvim
-W, --warn            do not suppress warnings about directories and binary files
-h, --help            show help message and exit

If both ``--only`` and ``--exclude`` are specified, both must be satisfied.


Examples
--------

Search specified files:

    fvi '#\!/usr/bin/env python3' ~/bin/*

Search all files in current hierarchy:

    fvi 'unknown key'


Installation
------------

Runs only on Unix systems.  Requires Python 3.6 or later.

Install using::

   pip install fvi


Configuration
-------------

The file ~/.config/fvi/settings.nt is read if it exists.  This is a NestedText_
file that can contain settings: *vim*, *gvim*, and *gui*.  The first specify the 
commands used to invoke *vim* and *gvim*.  The last is a Boolean that indicates 
whether *gvim* is used by default (use *yes* or *no*).  For example::

    vim: vimx
    gvim: gvim
    gui: yes

In this example, vimx is used rather than vim so that copy and paste using X11 
works as expected.

.. _NestedText: https://nestedtext.org
