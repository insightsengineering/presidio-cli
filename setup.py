# -*- coding: utf-8 -*-

from setuptools import setup
import os.path

readme = ""
here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, "README.md")
if os.path.exists(readme_path):
    with open(readme_path, "rb") as stream:
        readme = stream.read().decode("utf8")

setup(
    name="presidio_cli",
    version="0.0.1",
    description="CLI tool that analyzes text with Presidio framework",
    author="test",
    author_email="42359321+tomszosz@users.noreply.github.com",
    url="https://github.com/insightsengineering/presidio-cli",
    long_description=readme,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License v2",
        "Operating System :: OS Independent",
    ],
)
