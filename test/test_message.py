#! /usr/bin/env python
# coding:utf-8


import unittest
from kovot.message import Message
from kovot.message import MessageTransformer


class MessageTest(unittest.TestCase):
    def test_message(self):
        text = "京都にいます"
        message = Message(text=text)
        self.assertEqual(message.text, text)

    def test_message_with_id(self):
        text = "京都にいます"
        id_ = 100
        message_with_id = Message(text=text, id_=id_)
        self.assertEqual(message_with_id.text, text)
        self.assertEqual(message_with_id.id_, id_)

    def test_dict(self):
        message = Message(text="テスト", id_=0)
        self.assertEqual(message.dict(),
                         {"text": "テスト",
                          "id_": 0,
                          "speaker": None})


class TransformerTest(unittest.TestCase):
    def test_transformer(self):
        text = "京都にいます"
        message = Message(text=text)
        transformer = MessageTransformer()

        self.assertEqual(transformer.transform(message),
                         message)