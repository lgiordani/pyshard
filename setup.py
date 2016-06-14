#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
]

test_requirements = [
    'pytest',
    'tox'
]

setup(
    name='pyshard',
    version='0.0.1',
    description="A simple sharding system in Python",
    long_description=readme + '\n\n' + history,
    author="Leonardo Giordani",
    author_email='giordani.leonardo@gmail.com',
    url='https://github.com/lgiordani/pyshard',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords=['version', 'management'],
    test_suite='tests',
    tests_require=test_requirements,
)
