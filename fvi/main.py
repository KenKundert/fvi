#!/usr/bin/env python3
# DESCRIPTION {{{1
"""
fvi

Searches through a list of files to find a string, and then sequentially opens
each file that contains that string in Vim.

Usage:
    fvi [options] [--] <pattern> [<file>...]

Options:
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

Vim will open the first file that contains the pattern and place the cursor on
the first occurrence. Use n to go to the next occurrence and ctrl-n to go to the
next file and ctrl-p to go to the previous file. Autowrite is on by default,
so any changes you make are automatically saved before moving to the next file.

The pattern is a literal text string.  Regular expressions are not supported.

Use -- to terminate the command line options.  Any thing that follows -- is
treated as a pattern or filename.  You can search for patterns that start with
- by preceding the pattern with --.
"""


# LICENSE {{{1
# Copyright (C) 2013-2023 Kenneth S. Kundert
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see http://www.gnu.org/licenses/.


# IMPORTS {{{1
from appdirs import user_config_dir
from docopt import docopt
from fnmatch import fnmatch
from inform import (
    Error, codicil, cull, display, is_str, os_error, plural, terminate, warn
)
from shlib import Run, brace_expand, set_prefs, to_path, leaves
import nestedtext as nt
import codecs
import re
import os

# DEFAULTS & CONSTANTS {{{1
DEFAULT_GUI = False
DEFAULT_VIM = "vim"
DEFAULT_GVIM = "gvim"

# do not change these
__version__ = '2.2'
__released__ = '2023-03-18'
version = f"{__version__} ({__released__})"
set_prefs(use_inform=True)

# UTILITIES {{{1
# eliminate duplicate files {{{2
def eliminate_duplicates(files):
    seen = set()
    todo = []
    ignore = []
    for fn in files:
        try:
            nfo = os.stat(fn)
            if nfo.st_ino in seen:
                ignore.append(fn)
            else:
                seen.add(nfo.st_ino)
                todo.append(fn)
        except OSError as e:
            warn(os_error(e), 'Skipping ...')
            ignore.append(fn)
    if ignore:
        display('Ignoring duplicate files:\n    {}'.format('\n    '.join(ignore)))
    return todo

def vim_escape(pattern):
    return r'\V' + pattern.replace('\\', '\\\\').replace('/', '\\/')
        # \V is 'very no magic' flag in Vim

# MAIN {{{1
def main():
    try:
        # Read the settings {{{2
        settings_file = to_path(user_config_dir("fvi"), "settings.nt")
        settings = {}
        try:
            settings = nt.load(settings_file, 'dict')
        except FileNotFoundError:
            pass
        except nt.NestedTextError as e:
            e.report()
        except OSError as e:
            warn(os_error(e))
        vim = settings.get('vim', DEFAULT_VIM).split()
        gvim = settings.get('gvim', DEFAULT_GVIM).split()
        gui = settings.get('gui', DEFAULT_GUI)
        if is_str(gui):
            useGUI = gui.lower() in ['y', 'yes']
        else:
            useGUI = DEFAULT_GUI

        # Read the command line {{{2
        cmdline = docopt(__doc__, version=version)
        warn.output = cmdline['--warn']

        # Initialization {{{2
        vim_flags = ['aw', 'nofen']  # enable autowrite and disable folds in vim
        re_flags = 0
        cmd = None

        # Process the command line {{{2
        # <pattern> {{{3
        pattern = cmdline['<pattern>']
        re_pattern = re.escape(pattern)
        vim_pattern = vim_escape(pattern)

        # <file> {{{3
        files = eliminate_duplicates(cmdline['<file>'])

        # --ignore-case {{{3
        if cmdline['--ignore-case']:
            re_flags += re.IGNORECASE
            vim_pattern = r'\c' + vim_pattern

        # --word {{{3
        if cmdline['--word']:
            re_pattern = r'\b' + re_pattern + r'\b'
            vim_pattern = r'\<' + vim_pattern + r'\>'

        # --vim and --gvim {{{3
        if cmdline['--vim']:
            useGUI = False
        if cmdline['--gvim']:
            useGUI = True
        editor = gvim if useGUI else vim

        # --only {{{3
        if cmdline['--only']:
            globs = list(brace_expand(cmdline['--only']))
            def acceptable(path):
                for glob in globs:
                    if fnmatch(path.name, glob):
                        return True

        else:
            def acceptable(path):
                return True

        # --exclude {{{3
        if cmdline['--exclude']:
            globs = list(brace_expand(cmdline['--exclude']))
            def exclude(path):
                for glob in globs:
                    if fnmatch(path.name, glob):
                        return True
        else:
            def exclude(path):
                return False

        # Find files to edit {{{2
        if not files:
            files = leaves('.', hidden=cmdline['--hidden'])

        # Eliminate undesirable files {{{2
        #     those that do not contain the pattern,
        #     those don’t match only glob,
        #     those that match exclude glob, or
        #     directories and unreadable or binary files
        filtered_files = set()
        regex = re.compile(re_pattern, re_flags)
        err_handler = 'ignore' if cmdline['--binary'] else 'strict'
        for path in files:
            if is_str(path):
                path = to_path(path)
            if exclude(path) or not acceptable(path):
                continue
            try:
                with codecs.open(path, 'r', 'utf-8', err_handler) as f:
                    contents = f.read()
                    if regex.search(contents, re_flags):
                        filtered_files.add(path.resolve())
                             # resolve path to eliminate duplicates due to symlinks
            except OSError as e:
                warn(os_error(e), 'Skipping ...')
            except UnicodeDecodeError as e:
                warn("is a binary file, skipping ...", culprit=path)
                codicil(str(e))
                begin = max(e.start-25, 0)
                codicil('    ', e.object[begin:e.end+25])
                codicil('    ', (2+e.start-begin)*' ' + (e.end-e.start)*'^')
        files = sorted(cull(filtered_files))

        # Exit if there are no files {{{2
        if not files:
            display("Pattern not found.")
            terminate()

        # Edit the files {{{2
        assert files
        vim_options = 'set %s' % ' '.join(vim_flags)
        # Configure ctrl-N to move to first occurrence of search string in next file   
        # while suppressing the annoying 'press enter' message and echoing the
        # name of the new file so you know where you are.
        next_file_map = 'map <C-N> :silent next +//<CR> :file<CR>'
        prev_file_map = 'map <C-P> :silent previous +//<CR> :file<CR>'
        search_pattern = f"silent /{vim_pattern}"
        vim_cmds = [vim_options, next_file_map, prev_file_map, search_pattern]
        cmd = editor + ['+' + '|'.join(vim_cmds)] + files
        vim = Run(cmd, modes='soEW*')
        terminate(vim.status)

    except KeyboardInterrupt:
        display('Killed by user.')
        terminate(0)
    except Error as e:
        e.terminate()

# vim: set sw=4 sts=4 et:
