#! /usr/bin/env python
# coding:utf-8


import unittest
from kovot.mod import ModManager
from kovot.response import Response
from kovot.message import Message


class ModTestMixin:
    def test_satisfy_interface(self):
        self.assertTrue(hasattr(self.mod, "generate_responses"))


def gen_res(score, source):
    return Response(text="テスト", score=score, source=source)


class ModDouble:
    def __init__(self, mod_name):
        self.mod_name = mod_name

    def _gen_res(self, score):
        return gen_res(score, self.mod_name)

    def generate_responses(self, bot, message):
        reses = [self._gen_res(0.1),
                 self._gen_res(0.2)]
        return reses


class KovotDouble:
    pass


class ModManagerTest(unittest.TestCase):
    def test_manager(self):
        mod1 = ModDouble("mod1")
        mod2 = ModDouble("mod2")
        bot = KovotDouble()
        manager = ModManager(mods=[mod1, mod2])
        message = Message(text="テストメッセージ")

        res = manager.generate_responses(bot, message)
        ans = [gen_res(0.1, "mod1"),
               gen_res(0.2, "mod1"),
               gen_res(0.1, "mod2"),
               gen_res(0.2, "mod2")]

        self.assertEqual(res, ans)
