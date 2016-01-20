from setuptools import setup

# Create/update manpage before installing
message = ''
try:
    import manpage
    manpage.write()
except ImportError:
    # this will let the setup script run, allowing prerequisites to be 
    # installed, but then setup script must be run again so manpage is 
    # generated.
    with open('fvi.1', 'w') as f:
        f.write('')
    message='\nRerun setup in order to generate the manpage.'

with open('README.rst') as f:
    readme = f.read()

setup(
    name='fvi',
    version='1.1.4',
    description="Search for a pattern in a set of files and edit the files that contain the pattern.",
    author="Ken Kundert",
    author_email='fvi@nurdletech.com',
    download_url='git@github.com:KenKundert/fvi.git',
    scripts=['fvi'],
    data_files=[
        ('man/man1', ['fvi.1']),
    ],
    license='GPLv3+',
    install_requires=[
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

print(message)
# vim: set sw=4 sts=4 et:
