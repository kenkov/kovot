#! /usr/bin/env python
# coding:utf-8


import unittest
from kovot.bot import Bot
from kovot.response import Response
from kovot.message import Message


class EchoMod:
    def get_responses(self, bot, message):
        res = Response(score=1.0,
                       text=message.text)
        return [res]


class BotTest(unittest.TestCase):
    def test_talk(self):
        msg = Message(text="テスト")
        bot = Bot(mods=[EchoMod()])

        res = bot.talk(msg)
        res == Response(score=1.0, text="テスト")