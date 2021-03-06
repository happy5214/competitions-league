# -*- coding: utf-8  -*-
"""A setuptools based setup module."""

from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='competitions-league',
    version='0.1a1',

    description='Generic league competitions',
    long_description=long_description,

    url='https://github.com/happy5214/competitions-league',

    author='Alexander Jones',
    author_email='happy5214@gmail.com',

    license='LGPLv3+',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='competitions leagues roundrobin',

    packages=find_packages(exclude=['docs', 'tests*']),

    namespace_packages=['competitions'],

    test_suite='tests',

    install_requires=['competitions-match>=0.3',
                      'competitions-scheduler>=0.2'],
)
