#! /usr/bin/env python
# coding:utf-8


import logging


class Mod:
    def get_responses(self, bot, message):
        """レスポンスを返す

        Args:
            message (Message):

        Returns
            List[Response]:
        """
        pass


class ModManager:
    def __init__(self, mods):
        """
        Args:
            modules (List[Mod]): モジュールのリスト
        """
        self._mods = mods

    def get_responses(self, bot, message):
        reses_list = [module.get_responses(bot, message)
                      for module in self._mods]
        return sum(reses_list, [])

    def show_mods(self):
        logging.info("using mods:\n{}".format(
            "\n".join("    - {}".format(str(mod)) for mod in self._mods)
        ))
