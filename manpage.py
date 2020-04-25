#!/usr/bin/env python
# FVI Documentation
#
# Converts a restructured text version of the manpages to nroff.

# License {{{1
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.

# Imports {{{1
from docutils.core import publish_string
from docutils.writers import manpage
from textwrap import dedent

# Program version {{{1
version = '1.3.0'
date = '2020-04-16'

# Program Manpage {{{1
programManpage = {
    'name': 'fvi',
    'sect': '1',
    'contents': r"""{
        =====
         fvi
        =====

        ------------------------------------------
        find and edit files that contain a pattern
        ------------------------------------------

        :Author: Ken Kundert <fvi@nurdletech.com>
        :Date: {date}
        :Version: {version}
        :Manual section: 1

        .. :Copyright: public domain
        .. :Manual group: Utilities

        SYNOPSIS
        ========
        **fvi** [*options*] pattern [*files*]

        OPTIONS
        =======

        Usage::

            fvi [-h] [-w] [-i] [-m] [-v] [-g] pattern [file [file ...]]

        -h, --help          show help message and exit
        -w, --word          match a word
        -i, --ignore-case   ignore case
        -m, --magic         treat a pattern as a vim magic or grep basic regular 
                            expression
        -v, --very-magic    treat a pattern as a vim very magic or grep extended 
                            regular expression

        -g, --gvim          open files in gvim rather than vim

        DESCRIPTION
        ===========
        **fvi** searches for files that contain a pattern and then open them in 
        *vim* or *gvim*.

        BASIC USE
        ---------

        A typical use of **fvi** would be to search a list of files looking for 
        the use of a particular pattern and then edit those files. For example, 
        imagine you want to search your python source code looking for uses of 
        the function 'generate'. You can do so with::

            fvi generate *.py

        This searches through the files that end in .py in the current working 
        directory, finds those that contains 'generate', and then runs *vim* on 
        just those files (it silently ignores directories, binary files, and 
        unreadable files that are given in the file list).

        When running *vim*, **fvi** enables the autowrite feature, and disables 
        folds.  It also positions the cursor on the first occurrence of the 
        pattern when it opens a file.  Finally, it maps N to move to the next 
        occurrence of the pattern and maps Ctrl-N to move to the next file.  
        Since autowrite is enabled, you do not have to explicitly write out the 
        file after making a change. Just moving to the next file will write out 
        any changes you made to a file.

        Words
        ~~~~~

        Using::

            fvi generate *.py

        will find every occurrence of 'generate', but it will also find 
        occurrences of 'generated'. Using the ``-w`` or ``--word`` command line 
        option you can limit the pattern to only match complete words, in this 
        case 'generate'::

            fvi -w generate *.py

        Case Sensitivity
        ~~~~~~~~~~~~~~~~

        Normally the pattern is case sensitive. Using ``-i`` or 
        ``--ignore-case`` causes the case of the letters in the pattern to be 
        ignored. So::

            fvi -i generate *.py

        will find occurrences of 'generate', 'Generate', 'GENERATE', and the 
        like.

        gvim
        ~~~~

        By default, **fvi** opens *vim* in the terminal. By adding the ``-g`` or 
        ``--gvim`` command line option you instruct **fvi** to instead use 
        *gvim*, which opens the files in a dedicated gvim window.

        Ack
        ~~~

        If you leave off the list of files to be searched, then *ack* is used 
        find the files. By default *ack* searches all regular non-binary file in 
        the current working directory and all its subdirectories, however you 
        can use .ackrc files to control this behavior (run 'man ack' for more 
        information).

        ADVANCED USE
        ------------

        It is possible to use regular expressions for the search pattern.  
        However, **fvi** faces a challenge in doing so. When a regular 
        expression is given, **fvi** uses the regular expression capabilities of 
        *grep* or *ack* to search the files looking for the ones to edit, and 
        then uses the regular expression capabilities of *vim* after opening the 
        files. Unfortunately the same regular expression is used in both cases 
        and these capabilities are not completely compatible.

        Grep
        ~~~~

        When you use **fvi** with a regular expression pattern and a file list, 
        *grep* is used to identify which files contain that pattern. *grep* and 
        *vim* both provide two kinds of regular expressions that are closely 
        related.  *Grep* supports basic and extended GNU regular expressions.  
        *Vim* supports magic and very magic regular expressions.  The basic GNU 
        and Vim magic regular expressions correspond, and similarly the extended 
        GNU and Vim very magic regular expressions correspond, however this 
        correspondence is not exact.  I have not mapped the degree to which they 
        do not correspond, but here are some examples of things that are known 
        to correspond, and things that are known not to correspond.

        Things that are not safe to use
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ``\b``, ``\B`` to match edges of words (available in *grep* but not *vim*).


        Things that are not safe to use in basic/magic
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        None.

        Things that are not safe to use in extended/very magic
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        | beginning of word: use ``\<`` in extended, ``<`` in very magic
        | end of word:       use ``\>`` in extended, ``>`` in very magic


        Things that are safe to use
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        | ``[ ]``  expressions
        | ``\w``
        | ``\W``
        | ``\s``
        | ``\S``
        | ``^``
        | ``$``
        | ``.``
        | ``*``
        | ``+``    use ``\+`` in basic/magic, use ``+`` in extended/very magic
        | ``?``    use ``\?`` in basic/magic, use ``?`` in extended/very magic
        | ``{{``    use ``\{{`` in basic/magic, use ``{{`` in extended/very magic
        | ``}}``    use ``\}}`` in basic/magic, use ``}}`` in extended/very magic
        | ``|``    use ``\|`` in basic/magic, use ``|`` in extended/very magic
        | ``(``    use ``\(`` in basic/magic, use ``)`` in extended/very magic
        | ``)``    use ``\(`` in basic/magic, use ``)`` in extended/very magic
        | ``\d``   matches previously matched group, were *d* is a digit

        Ack
        ~~~

        When you use **fvi** without a file list, *ack* is used to identify 
        which files contain that pattern.  *ack* and *vim* both support regular 
        expressions, but *ack* provides Perl compatible regular expressions and 
        *vim* supports regular expressions similar to the GNU regular 
        expressions. The compatibility between these two types of regular 
        expressions is rough. I recommend that in this situation, you use Perl 
        regular expressions as the pattern given on the **fvi** command line.  
        Then when the files are opened in *vim* you may find that *vm* has 
        trouble finding the pattern. At this point you should simply type ``/`` 
        and then re-enter the search pattern, but this time in a *vim* 
        compatible manner.

        SEE ALSO
        ========
        vim(3), grep(3), ack(3)
    }"""
}

# Generate restructured text {{{1
def write(genRST=False):
    for each in [programManpage]:
        rst = dedent(each['contents'][1:-1]).format(date=date, version=version)

        # generate reStructuredText file (only used for debugging)
        if genRST:
            with open('%s.%s.rst' % (each['name'], each['sect']), 'w') as f:
                f.write(rst)

        # Generate man page
        print("generating %s.%s" % (each['name'], each['sect']))
        with open('%s.%s' % (each['name'], each['sect']), 'w') as f:
            f.write(publish_string(rst, writer=manpage.Writer()).decode())

if __name__ == '__main__':
    write(True)

# vim: set sw=4 sts=4 tw=80 formatoptions=ntcqwa12 et spell:
