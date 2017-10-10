#! /usr/bin/env python
# coding:utf-8


from kovot.mod import Mod


class ModEcho(Mod):
    def utter(self, message, master):
        return [
            (1.0, message["text"], "echo", dict())
        ]

    def can_utter(self, message, master):
        return True
