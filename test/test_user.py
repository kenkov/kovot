#! /usr/bin/env python
# coding:utf-8


import unittest
from kovot.speaker import Speaker


class SpeakerTest(unittest.TestCase):
    def test_user(self):
        name = "hoge"
        message = Speaker(name=name)
        self.assertEqual(message.name, name)
