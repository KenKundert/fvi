from setuptools import setup
from textwrap import dedent

# Create/update manpage before installing
import manpage
manpage.write()

setup(
    name='fvi'
  , description=dedent("""\
        Search for a pattern in a collection of files and edit the files that
        contain the pattern.
    """)
  , author="Ken Kundert"
  , author_email='theNurd@nurdletech.com'
  , version=manpage.version
  , download_url='git@github.com:KenKundert/fvi.git'
  , scripts=['fvi']
  , data_files=[
        ('man/man1', ['fvi.1']),
    ]
  , license='GPLv3'
)
