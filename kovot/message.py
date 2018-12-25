#! /usr/bin/env python
# coding:utf-8

from kovot.util import ClassInitReplMixin
import kovot.util


class Message(ClassInitReplMixin):
    def __init__(self, text, id_=None, speaker=None):
        self.text = text
        self.id_ = id_
        self.speaker = speaker

    def dict(self):
        d = {"text": self.text,
             "id_": self.id_,
             "speaker": self.speaker}
        return kovot.util.dict(d)

    def __getattr__(self, name):
        return self._argv[name]


class MessageTransformer:
    def transform(self, message):
        return message
