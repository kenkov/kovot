#! /usr/bin/env python
# coding:utf-8

try:
    import kovlive
except ImportError:
    pass


class PostProcessing:
    def convert(self, message, answer, master) -> (float, str, str):
        return answer


class Ja2Kov(PostProcessing):
    def __init__(self, phrasemodel, bigrammodel):
        self.kl = kovlive.KovLang(phrasemodel, bigrammodel)

    def convert(self, message, answer, master) -> (float, str, str):
        prob, text, source, info = answer
        mod_text = self.kl.ja2kov(text)

        return (prob, mod_text, source, info)
