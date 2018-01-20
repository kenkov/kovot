#! /usr/bin/env python
# coding:utf-8


from collections import namedtuple


class Message:
    def __init__(self, text, id_=0, user=None):
        self.text = text
        self.id_ = id_
        self.user = user


User = namedtuple("User", ["name"])
