#! /usr/bin/env python
# coding:utf-8

from kovot.util import ClassInitReplMixin


class Message(ClassInitReplMixin):
    def __init__(self, text, id_=None, user=None):
        self.text = text
        self.id_ = id_
        self.user = user


class MessageTransformer:
    def transform(self, message):
        return message
