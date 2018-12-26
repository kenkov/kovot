#! /usr/bin/env python
# coding:utf-8

from kovot.util import ClassInitReplMixin
from kovot.util import ClassAttrEqMixin
from kovot.speaker import Speaker
import kovot.util


class Message(ClassInitReplMixin, ClassAttrEqMixin):
    def __init__(self, text, id_=None, speaker=None):
        self.text = text
        self.id_ = id_
        self.speaker = speaker

    def dict(self):
        d = {"text": self.text,
             "id_": self.id_,
             "speaker": self.speaker}
        return kovot.util.dict(d)

    @classmethod
    def from_dict(cls, dic):
        speaker = dic.get("speaker")
        if speaker:
            speaker = Speaker.from_dict(speaker)

        m = Message(text=dic["text"],   
                    id_=dic.get("id_"),
                    speaker=speaker)
        return m

    def __getattr__(self, name):
        return self._argv[name]


class MessageTransformer:
    def transform(self, message):
        return message
