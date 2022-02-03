# -*- coding: utf-8 -*-

from setuptools import setup
import os.path
from presidio_cli import (
    __author__,
    __author_email__,
    __license__,
    APP_NAME,
    APP_VERSION,
    APP_DESCRIPTION,
)

readme = ""
here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, "README.md")
if os.path.exists(readme_path):
    with open(readme_path, "rb") as stream:
        readme = stream.read().decode("utf8")

setup(
    name=APP_NAME,
    version=APP_VERSION,
    author=__author__,
    author_email=__author_email__,
    #description=APP_DESCRIPTION.split("\n")[0],
    #"CLI tool that analyzes text with Presidio framework",
    url="https://github.com/insightsengineering/presidio-cli",
    license=__license__,
    description=APP_DESCRIPTION.split("\n")[0],
    long_description=APP_DESCRIPTION,
    #long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
