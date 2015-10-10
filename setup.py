#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup

from pip.req import parse_requirements
import pip

# requirements = [
    # str(req.req) for req in parse_requirements('requirements.txt', session=pip.download.PipSession())
# ]


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-docker',
    version='0.1.0',
    author='John Dennison',
    author_email='dennison.john@gmail.com',
    maintainer='John Dennison',
    maintainer_email='dennison.john@gmail.com',
    license='MIT',
    url='https://github.com/jofusa/pytest-docker',
    description='Plugin to help launch docker containers',
    long_description=read('README.rst'),
    py_modules=['pytest_docker'],
    install_requires=['pytest', 'docker-py'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
    ],
    entry_points={
        'pytest11': [
            'docker = pytest_docker',
        ],
    },
)
