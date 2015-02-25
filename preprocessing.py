#! /usr/bin/env python
# coding:utf-8

import re


class Preprocess:

    def __init__(self):
        self.html_regex = re.compile(
            r'(http|https)://[a-zA-Z0-9-./"#$%&\':?=_]+')
        self.newline_regex = re.compile(r'\n')
        self.cont_spaces_regex = re.compile(r'\s+')

    def _subs(self, regex: "re obj", repl: str, text: str):
        return regex.sub(repl, text)

    def remove_link(self, text: str) -> str:
        return self._subs(self.html_regex, "", text)

    def remove_newline(self, text: str) -> str:
        return self._subs(self.newline_regex, "", text)

    def remove_spaces(self, text: str) -> str:
        return self._subs(self.cont_spaces_regex, "", text)

    def convert_cont_spaces(self, text: str) -> str:
        return self._subs(self.cont_spaces_regex, " ", text)

    def strip(self, text: str) -> str:
        return text.strip()

    def execute(self, text: str) -> str:
        funcs = [
            self.remove_newline,
            self.remove_link,
            self.convert_cont_spaces,
            self.strip]
        _text = text
        for func in funcs:
            _text = func(_text)
        return _text


class Twitter(Preprocess):

    def __init__(self):
        Preprocess.__init__(self)
        username = r'@[a-zA-Z0-9_]+'
        tag = r'#[a-zA-Z0-9_]+'
        self.mention_regex = re.compile(r'{}'.format(username))
        self.retweet_regex = re.compile(r'RT {}:'.format(username))
        self.tag_regex = re.compile(r'{}'.format(tag))

    def remove_mention(self, text: str) -> str:
        return self._subs(self.mention_regex, "", text)

    def remove_retweet(self, text: str) -> str:
        return self._subs(self.retweet_regex, "", text)

    def remove_tag(self, text: str) -> str:
        return self._subs(self.tag_regex, "", text)

    def execute(self, text: str) -> str:
        funcs = [
            self.remove_newline,
            self.remove_link,
            self.remove_retweet,
            self.remove_mention,
            self.remove_tag,
            self.convert_cont_spaces,
            self.strip]
        _text = text

        for func in funcs:
            _text = func(_text)

        return _text


if __name__ == '__main__':
    import sys

    pre = Preprocess()

    for filename in sys.argv[1:]:
        print(filename)
        with open(filename, "r") as f:
            for line in f:
                _line = line.strip()
                print(pre.execute(_line))
