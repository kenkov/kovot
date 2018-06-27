#! /usr/bin/env python
# coding:utf-8


import unittest
from kovot.mod import ModManager
from kovot.response import Response
from kovot.message import Message


class ModTestMixin:
    def test_mod(self):
        self.assertTrue(hasattr(self.mod, "get_responses"))


def gen_res(score, source):
    return Response(text="テスト", score=score, source=source)


class ModDouble:
    def __init__(self, mod_name):
        self.mod_name = mod_name

    def _gen_res(self, score):
        return gen_res(score, self.mod_name)

    def get_responses(self, message):
        reses = [self._gen_res(0.1),
                 self._gen_res(0.2)]
        return reses


class ModManagerTest(unittest.TestCase):
    def test_manager(self):
        mod1 = ModDouble("mod1")
        mod2 = ModDouble("mod2")
        manager = ModManager(mods=[mod1, mod2])
        message = Message(text="テストメッセージ")

        res = manager.get_responses(message)
        ans = [gen_res(0.1, "mod1"),
               gen_res(0.2, "mod1"),
               gen_res(0.1, "mod2"),
               gen_res(0.2, "mod2")]

        self.assertEqual(res, ans)
