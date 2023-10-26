from setuptools import setup

import re

from pathlib import Path

__version__ = re.findall(
    r"""__version__ = ["']+([0-9\.\-dev]*)["']+""",
    open('testflo/__init__.py').read(),
)[0]

with open(Path(__file__).parent / "README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(name='testflo',
      version=__version__,
      description="A simple flow-based testing framework",
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: Apache Software License',
          'Natural Language :: English',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX :: Linux',
          'Operating System :: Microsoft :: Windows',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: Implementation :: CPython',
      ],
      license='Apache 2.0',
      install_requires=[
        'coverage>=6.0'
      ],
      packages=['testflo'],
      entry_points="""
          [console_scripts]
          testflo=testflo.main:main
      """
      )
