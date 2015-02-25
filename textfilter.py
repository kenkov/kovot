#! /usr/bin/env python
# coding:utf-8

import preprocessing
import chartype
import re


class Preprocess:
    def sub(self, xs: str) -> str:
        return xs

    def filter(self, xs: str) -> bool:
        return True


class TwitterPreprocess(Preprocess):
    def _is_nihongo(self, s):
        ct = chartype.Chartype()
        ex_set = {"！", "？"}
        return all(
            ct.is_nihongo(char) or
            ct.is_ascii(char) or
            char in ex_set for char in s
        )

    def _convert_slash(self, xs: str) -> str:
        """
        形態素解析のため
        """
        slash_regex = r"/"
        return re.sub(slash_regex, "／", xs)

    def sub(self, xs: str) -> str:
        convert = preprocessing.Twitter()
        # Do
        #   remove_newline
        #   remove_link
        #   remove_retweet
        #   remove_mention
        #   remove_tag
        #   convert_cont_spaces
        #   strip
        #
        #   remove spaces
        convtw = xs
        for func in [
                convert.execute,
                convert.remove_spaces,
                self._convert_slash,
        ]:
            convtw = func(convtw)

        return convtw

    def filter(self, xs: str) -> bool:
        return self._is_nihongo(xs) and xs


class TwitterFilter:
    def __init__(self):
        self.preprocess = TwitterPreprocess()

    def filter(self, lines: [str]) -> [str]:
        for text in lines:
            try:
                # CharType が
                #   ValueError: no such name
                # をだす可能性がある
                convtw = self.preprocess.sub(text)
                if self.preprocess.filter(convtw):
                    yield convtw
            except ValueError:
                continue
