#! /usr/bin/env python
# coding:utf-8

import kovlive


class PostProcessing:
    def convert(self, message, answer, master) -> (float, str, str):
        return answer


class Ja2Kov(PostProcessing):
    def __init__(self, phrasemodel, bigrammodel):
        self.kl = kovlive.KovLang(phrasemodel, bigrammodel)

    def convert(self, message, answer, master) -> (float, str, str):
        prob, text, source, info = answer
        mod_text = self.kl.search(text)

        return (prob, mod_text, source, info)
