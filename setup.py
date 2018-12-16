#! /usr/bin/env python
# coding:utf-8

from distutils.core import setup


setup(
    name="kovot",
    packages=["kovot", "kovot.stream"],
    install_requires=[
        "slackclient>=1.2.1",
        "requests>=2.21.0",
    ],
    version="0.1.1",
    author="kenkov",
    author_email="kenkovtan@gmail.com",
    url="http://kenkov.jp",
)
