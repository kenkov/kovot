#! /usr/bin/env python
# coding:utf-8

from distutils.core import setup


setup(
    name="kovot",
    packages=["kovot", "kovot.stream"],
    install_requires=[
        "slackclient==1.2.1",
        "Mastodon.py==1.3.1",
        "requests==2.21.0",
    ],
    version="0.2.4",
    author="kenkov",
    author_email="kenkovtan@gmail.com",
    url="http://kenkov.jp",
)
