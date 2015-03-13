#! /usr/bin/env python
# coding:utf-8


from mod import Mod


class ModEcho(Mod):
    def utter(self, message, master):
        return [
            (1.0, message["text"], "echo", dict())
        ]

    def is_utterance_needed(self, message, master):
        return True
