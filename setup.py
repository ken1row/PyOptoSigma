#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
if sys.version_info[0] < 3:
    raise Exception('This module only supports Python 3.4 or later. Try use `python3 setup.py`')

from setuptools import setup

long_description = '''
Python module for operating stepping moter stages manufactured by OptoSigma and Sigma Koki.

Requirements
------------
* Python 3.4 or later. (Python 2.x are not supported.)
* pyserial

Setup
-----
::

    $ sudo pip3 pyserial pyOptoSigma
    
* In Ubuntu systems, add an user to dialout group.

::

    $ sudo gpasswd -a [username] dialout
    
History
-------
0.1 (2016-5-28)
~~~~~~~~~~~~~~~
* First release.
* Supports SHOT-702, SHOT-302GS, SHOT-304GS controllers.
* Supports SGSP, OSMS series stages.
'''

classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Manufacturing',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3 :: Only'
]

setup(
    name = 'pyOptoSigma',
    version = '0.1',
    py_modules = ['pyOptoSigma'],
    description = 'Python module for operating stepping moter stages manufactured by OptoSigma and Sigma Koki.',
    long_description = long_description,
    classifiers = classifiers,
    keywords=['OptoSigma', 'Sigma Koki', 'シグマ光機', 'translation stages', 'rotation stages'],
    author = 'Kenichiro Tanaka',
    author_email = 'tanaka@am.sanken.osaka-u.ac.jp',
    url = 'https://github.com/ken1row/PyOptoSigma',
    license='MIT'
    )