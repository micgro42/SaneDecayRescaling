# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import os

config = {
    'name': 'SaneDecayRescaling',
    'description': 'My Project',
    'author': 'Michael Große',
    'url': 'https://github.com/micgro42/SaneDecayRescaling',
    'download_url': 'https://github.com/micgro42/SaneDecayRescaling',
    'author_email': 'micgro42@physik.hu-berlin.de',
    'version': '0.0.1',
    'install_requires': ['nose'],
    'packages': ['sanedecayrescaling','sanedecayrescaling.tests'],
    'scripts': [],
    'long_description': open('README.rst', 'r').read(),
}

setup(**config)
