#! /usr/bin/env python
# coding:utf-8


from kovot.util import ClassInitReplMixin
from kovot.util import ClassAttrEqMixin


class Response(ClassInitReplMixin, ClassAttrEqMixin):
    def __init__(self,
                 text,
                 score,
                 id_=None,
                 user=None,
                 message=None,
                 source=None):
        self.text = text
        self.score = score
        self.id_ = id_
        self.user = user
        self.message = message
        self.source = source


class ResponseTransformer:
    def transform(self, response):
        return response
