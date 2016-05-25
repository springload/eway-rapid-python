#!/usr/bin/env python


from sys import version_info
from setuptools import setup, find_packages


requirements = ['requests>=2.10.0']

if version_info.major < 3 or (version_info.major == 3 and version_info.minor < 4): # Python < 3.4
    requirements.append('enum34>=1.1.6') 


setup(
    name = 'eway-rapid-python',
    description = 'Python client implementation for eWAY Rapid API v3',
    version = '0.7.1',
    packages = find_packages(exclude=('tests',)),
    install_requires = requirements,
    extras_require = {'testing': ['hypothesis>=3.1.3', 'coverage']},
    author = 'Sergey Latyntsev at Springload',
    author_email = 'dnsl48@gmail.com',
    license = 'MIT',
    keywords = 'eway',
    url = 'https://github.com/springload/eway-rapid-python'
)