#!/usr/bin/env python
from setuptools import setup
from os.path import dirname, join, isfile
from shutil import copyfile

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

if not isfile('settings.py'):
    copyfile('_settings_base.py', 'settings.py')
print("\n**** \nImportant!!!\nEdit settings.py before starting the script.\n****")
