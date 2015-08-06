#!/usr/bin/env python
"""
sentry-s3-nodestore
==============
An extension for Sentry which implements an S3 NodeStorage backend
"""
from setuptools import setup

install_requires = [
    'boto>=2.38.0',
    'sentry>=7.4.0',
]

tests_requires = [
    'moto>=0.4.10'
]

setup(
    name='sentry-s3-nodestore',
    version='1.0.0',
    author='Ernest W. Durbin III',
    author_email='ewdurbin@gmail.com',
    url='http://github.com/ewdurbin/sentry-s3-nodestore',
    description='A Sentry extension to add S3 as a NodeStore backend.',
    long_description=__doc__,
    packages=['sentry_s3_nodestore'],
    license='BSD',
    zip_safe=False,
    install_requires=install_requires,
    tests_requires=tests_requires,
    test_suite='tests',
    include_package_data=True,
    download_url='https://pypi.python.org/pypi/sentry-s3-nodestore',
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
