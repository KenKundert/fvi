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
    version='1.1.6',
    description="Search for a pattern in a set of files and edit the files that contain the pattern.",
    author="Ken Kundert",
    author_email='fvi@nurdletech.com',
    download_url='git@github.com:KenKundert/fvi.git',
    scripts=['fvi'],
    data_files=[
        ('man/man1', ['fvi.1'])
    ],
    license='GPLv3+',
    requires=[
        'docopt',
        'docutils',
        'inform',
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
