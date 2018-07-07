#! /usr/bin/env python
# coding:utf-8


from kovot.mod import Mod
from kovot.response import Response
from kovot.bot import Bot
from kovot.stream.stdio import StdIO


class EchoMod(Mod):
    def get_responses(self, bot, message):
        res = Response(score=1.0,
                       text=message.text,
                       message=message,
                       source=self.__class__.__name__)
        return [res]


if __name__ == "__main__":
    from logging import basicConfig, INFO

    basicConfig(
        level=INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )

    # mods
    mods = [EchoMod()]
    kovot = Bot(mods=mods)
    stdin_stream = StdIO()

    kovot.run(stdin_stream)
