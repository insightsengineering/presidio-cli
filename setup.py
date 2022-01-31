# -*- coding: utf-8 -*-

from setuptools import setup

from yamllint import (
    __author__,
    __license__,
    APP_NAME,
    APP_VERSION,
    APP_DESCRIPTION,
)


setup(
    name=APP_NAME,
    version=APP_VERSION,
    author=__author__,
    description=APP_DESCRIPTION.split("\n")[0],
    long_description=APP_DESCRIPTION,
    license=__license__,
)
