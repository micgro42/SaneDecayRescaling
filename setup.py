# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
else:
    from setuptools.command.test import test as TestCommand
import os
import sys

# test implementation taken from: http://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

config = {
    'name': 'SaneDecayRescaling',
    'description': 'My Project',
    'author': 'Michael Groﬂe',
    'url': 'https://github.com/micgro42/SaneDecayRescaling',
    'download_url': 'https://github.com/micgro42/SaneDecayRescaling',
    'author_email': 'micgro42@physik.hu-berlin.de',
    'version': '0.0.1',
    'install_requires': [],
    'tests_require': ['pytest'],
    'cmdclass': {'test': PyTest},
    'extras_require': {
        'testing': ['pytest'],
    },
    'packages': ['sanedecayrescaling','sanedecayrescaling.tests'],
    'scripts': [],
    'long_description': open('README.rst', 'r').read(),
}

setup(**config)
