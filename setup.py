#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

requirements = [
]

test_requirements = [
    'pytest',
    'tox'
]

setup(
    name='pyshard',
    version='1.0.0',
    description="A simple sharding system in Python",
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
    scripts=[
        'scripts/pyshard_demo.py',
    ]

)
