from setuptools import setup
from textwrap import dedent

setup(
    name='fvi'
  , description=dedent("""\
        Search for a pattern in a collection of files and edit the files that
        contain the pattern
    """)
  , author="Ken Kundert"
  , author_email='theNurd@nurdletech.com'
  , download_url='git@github.com:KenKundert/fvi.git'
  , scripts=['fvi']
)
