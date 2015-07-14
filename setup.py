#!/usr/bin/env python
from setuptools import setup, find_packages
from os.path import dirname, join

here = dirname(__file__)

setup(name='bitmex-easy-data-scripts',
      version='0.1',
      description='Simple scripts for fetching account data from BitMEX.',
      long_description=open(join(here, 'README.md')).read(),
      author='Samuel Reed',
      author_email='sam@bitmex.com',
      url='',
      install_requires=[
          'requests'
      ]
      )
