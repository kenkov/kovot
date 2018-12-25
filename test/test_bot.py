#! /usr/bin/env python
# coding:utf-8


import unittest
from kovot import Bot
from kovot import Response
from kovot import Message
from kovot import Speaker


class EchoMod:
    def generate_responses(self, bot, message):
        res = Response(score=1.0,
                       text=message.text)
        return [res]


class BotTest(unittest.TestCase):
    def test_talk(self):
        msg = Message(text="テスト",
                      speaker=Speaker(name="話し✋"))
        bot = Bot(mods=[EchoMod()])

        res = bot.talk(msg)
        self.assertEqual(res, Response(score=1.0, text="テスト"))
