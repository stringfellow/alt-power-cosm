#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="altpower",
    version="0.1",
    packages=find_packages(),
    dependency_links=[
        "https://github.com/stringfellow/cosmSender/tarball/master",
    ],
    author="Steve Pike",
    author_email="altpower@stevepike.co.uk",
    description="Tools for rigging arduino monitoring for alt power",
    license="",
    keywords="solar arduino firmata cosm python",
    url="http://github.com/stringfellow/alt-power-cosm",
    long_description="",
)