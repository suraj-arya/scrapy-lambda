#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

requirements = [
    "boto3"
]


setup(
    name='scrapy-lambda',
    version='0.1.0',
    description="Scrapy pipeline which invokes a lambda with the scraped item",
    author="Suraj Arya",
    author_email='suraj@loanzen.in',
    url='https://github.com/suraj-arya/scrapy-lambda',
    packages=[
        'scrapylambda',
    ],
    package_dir={'scrapylambda':
                 'scrapylambda'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    keywords='scrapy-lambda',
)
