#! /usr/bin/env python
# coding:utf-8


import subprocess


class KyTea:
    def __init__(
        self,
        kytea_command="kytea",
        option: list=[],
    ):
        self._kytea = subprocess.Popen(
            [kytea_command, "-notag", "2"] + option,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)

    def _str2morph(self, xs: str) -> (str, str):
        return xs.split("/")

    def _morph2str(self, xs: (str, str)) -> str:
        word, tag = xs
        return "{}/{}".format(word, tag)

    def _morph2annot(self, morph: (str, str)) -> str:
        word, tag = morph
        return self._morph2str(("-".join(word), tag))

    def morph2annot(self, xs: [(str, str)]) -> str:
        return "|".join([self._morph2annot(_) for _ in xs])

    def morph2fullannot(self, xs: [(str, str)]) -> str:
        return " ".join("{}/{}".format(word, tag) for word, tag in xs)

    def analyze(self, ipt: str) -> [(str, str)]:
        kytea_ipt = ipt + "\n"
        self._kytea.stdin.write(kytea_ipt.encode('utf-8'))
        self._kytea.stdin.flush()
        morph = self._kytea.stdout.readline().decode('utf-8').rstrip().split()
        self._kytea.stdout.flush()
        return [self._str2morph(xs) for xs in morph]
