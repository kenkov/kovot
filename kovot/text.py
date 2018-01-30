#! /usr/bin/env python
# coding:utf-8


from cabocha.analyzer import CaboChaAnalyzer


class Text:
    def __init__(self,
                 text,
                 analyzer=CaboChaAnalyzer):
        """
        Args:
            text (str): 本文
            analyzer (object): 本文を解析するオブジェクト。
                analyze メソッドを実装し、戻り値が wakati 属性を
                持つことを求める。
        """
        self._text = text
        self._wakati = None
        self._analyzer = analyzer

    @property
    def text(self):
        return self._text

    @property
    def wakati(self):
        """本文の分かち書きを返す"""
        if self._wakati:
            return self._wakati
        self._wakati = self._analyzer.analyze(self._text).wakati
        return self._wakati

    def __str__(self):
        return self._text
