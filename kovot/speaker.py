#! /usr/bin/env python
# coding:utf-8

from kovot.util import ClassAttrEqMixin
import kovot.util


class Speaker(ClassAttrEqMixin):
    def __init__(self, name):
        self.name = name

    def dict(self):
        return kovot.util.dict({"name": self.name})

    @classmethod
    def from_dict(cls, dic):
        return cls(name=dic["name"])
