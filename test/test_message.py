#! /usr/bin/env python
# coding:utf-8


import unittest
from kovot.message import Message
from kovot.message import MessageTransformer
from kovot.speaker import Speaker


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

    def test_from_dict(self):
        d = {"text": "テスト"}
        self.assertEqual(Message.from_dict(d),
                         Message(text="テスト"))

    def test_from_dict_arg_speaker(self):
        d = {"text": "テスト", "speaker": {"name": "bot"}}
        self.assertEqual(Message.from_dict(d),
                         Message(text="テスト",
                                 speaker=Speaker(name="bot")))


class TransformerTest(unittest.TestCase):
    def test_transformer(self):
        text = "京都にいます"
        message = Message(text=text)
        transformer = MessageTransformer()

        self.assertEqual(transformer.transform(message),
                         message)