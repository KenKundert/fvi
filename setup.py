from distutils.core import setup
    # must use distutils rather than the newer setuptools because setuptools 
    # will not place the manpage where it belongs

# Create/update manpage before installing
try:
    import manpage
    manpage.write()
except ImportError:
    # distutils is not installed yet, so just use the existing version of the 
    # manpage rather than try to recreate/update it.
    pass

setup(
    name='fvi',
    version='1.1.7',
    description="Combines grep/ack with vim to quickly find and edit files that contain a pattern",
    author="Ken Kundert",
    author_email='fvi@nurdletech.com',
    url='http://nurdletech.com/linux-utilities/fvi',
    download_url='https://github.com/kenkundert/fvi/tarball/master',
    scripts=['fvi'],
    data_files=[
        ('man/man1', ['fvi.1'])
    ],
    license='GPLv3+',
    requires=[
        'docopt',
        'docutils',
        'inform (>=1.2)',
        'shlib',
    ],
    keywords=[
        'vim',
        'grep',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
    ],
)
# vim: set sw=4 sts=4 et:
