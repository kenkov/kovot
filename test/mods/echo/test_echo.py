#! /usr/bin/env python
# coding:utf-8


import unittest
from test.test_mod import ModInterfaceTestMixin
from kovot.mod.echo.echo import EchoMod
from kovot.message import Message


class TestEcho(unittest.TestCase, ModInterfaceTestMixin):
    def setUp(self):
        self.object = EchoMod()

    def test_get_responses(self):
        message = Message(text="おはよう")
        reses = self.object.get_responses(message)
        self.assertEqual(len(reses), 1)
        res = reses[0]
        self.assertEqual(res.text, "おはよう")
        self.assertEqual(res.score, 1)
