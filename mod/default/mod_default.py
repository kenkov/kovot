#! /usr/bin/env python
# coding:utf-8


from kovot.mod import Mod
import random
import os


class ModDefault(Mod):
    def __init__(
        self,
        filename=None,
        logger=None
    ):
        Mod.__init__(self, logger)
        text_path = filename or os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "default.txt"
        )
        self.default_texts = [line.strip() for line in open(text_path)]

    def can_utter(self, message, master):
        return True

    def utter(self, message, master):
        return [
            (random.uniform(0, 0.2),
             text, "default", dict())
            for text in self.default_texts
        ]
