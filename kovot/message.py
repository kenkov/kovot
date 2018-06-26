#! /usr/bin/env python
# coding:utf-8


class Message:
    def __init__(self, text, id_=None, user=None):
        self.text = text
        self.id_ = id_
        self.user = user

    def __eq__(self, other):
        return all([self.text == other.text,
                    self.id_ == other.id_,
                    self.user == other.user])

    def __repr__(self):
        fmt = "Message(text={x.text}, id_={x.id_}, user={x.user})"
        return fmt.format(x=self)


class MessageTransformer:
    def transform(self, message):
        return message
