#! /usr/bin/env python
# coding: utf-8


import unittest
from collections import namedtuple
from kovot.text import Text


class AnalyzerInterfaceTestMixin:
    def test_implements_analyze(self):
        self.assertTrue(hasattr(self.object, "analyze"))


TreeStub = namedtuple("TreeStub", ["wakati"])


class AnalyzerStub:
    def analyze(self, text):
        return TreeStub("疲れた ので 寝たい")


class TestAnalyzerStub(unittest.TestCase, AnalyzerInterfaceTestMixin):
    def setUp(self):
        self.object = AnalyzerStub()


class TestText(unittest.TestCase):
    def test_wakati(self):
        analyzer = AnalyzerStub()
        text = Text(text="疲れたので寝たい",
                    analyzer=analyzer)
        self.assertEqual(text.text, "疲れたので寝たい")
        self.assertEqual(text.wakati, "疲れた ので 寝たい")
