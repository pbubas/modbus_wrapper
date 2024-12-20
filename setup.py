#!/usr/bin/env python

from setuptools import setup

setup(
    name='modbus-wrapper',
    version='2.0.4a',
    description='wrapper for pyModbusTCP accepting all Modbus numbers with Fatek support',
    author='Przemyslaw Bubas',
    author_email='bubasenator@gmail.com',
    url='https://github.com/pbubas/modbus_wrapper',
    install_requires=[
        'pymodbus==3.6.9',
        'pyserial==3.5'
        ],
    keywords="modbus fatek",
    python_requires='>=3.10'
    )