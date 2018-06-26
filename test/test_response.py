#! /usr/bin/env python
# coding:utf-8


import unittest
from kovot.response import Response
from kovot.response import ResponseTransformer


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
