#! /usr/bin/env python
# coding:utf-8


import unittest
from kovot.response import Response
from kovot.response import ResponseTransformer
from kovot.response import ResponseSelector


class ResponseTest(unittest.TestCase):
    def test_response(self):
        text = "京都にいます"
        score = 1.2
        res = Response(text=text, score=score)
        self.assertEqual(res.text, text)
        self.assertEqual(res.score, score)


class TransformerTest(unittest.TestCase):
    def test_transformer(self):
        text = "京都にいます"
        score = 1.2
        res = Response(text=text, score=score)
        transformer = ResponseTransformer()

        self.assertEqual(transformer.transform(res), res)


class SelectorTest(unittest.TestCase):
    def test_select(self):
        x = Response(text="ひとつめ", score=1.2)
        y = Response(text="ふたつめ", score=3.2)
        z = Response(text="みっつめ", score=0.8)
        selector = ResponseSelector()
        self.assertEqual(selector.select([x, y, z]), [y, x, z])
        
    def test_select_with_num(self):
        x = Response(text="ひとつめ", score=1.2)
        y = Response(text="ふたつめ", score=3.2)
        z = Response(text="みっつめ", score=0.8)
        selector = ResponseSelector()
        self.assertEqual(selector.select([x, y, z], num=2),
                         [y, x])