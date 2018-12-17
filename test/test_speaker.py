#! /usr/bin/env python
# coding:utf-8


import unittest
from kovot.speaker import Speaker


class SpeakerTest(unittest.TestCase):
    def test_dict(self):
        speaker = Speaker(name="太郎")
        self.assertEqual(speaker.dict(), {"name": "太郎"})

    def test_from_dict(self):
        dic = {"name": "太郎"}

        self.assertEqual(Speaker.from_dict(dic), Speaker(name="太郎"))
