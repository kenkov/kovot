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

    def test_message_with_argv(self):
        text = "京都にいます"
        in_reply_to_id = 100
        message_with_id = Message(text=text,
                                  in_reply_to_id=in_reply_to_id)
        self.assertEqual(message_with_id.text, text)
        self.assertEqual(message_with_id.in_reply_to_id,
                         in_reply_to_id)


class TransformerTest(unittest.TestCase):
    def test_transformer(self):
        text = "京都にいます"
        message = Message(text=text)
        transformer = MessageTransformer()

        self.assertEqual(transformer.transform(message),
                         message)