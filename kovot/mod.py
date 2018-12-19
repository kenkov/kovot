#! /usr/bin/env python
# coding:utf-8


import logging


class ModManager:
    def __init__(self, mods):
        """
        Args:
            modules (List[Mod]): モジュールのリスト
        """
        self._mods = mods

    def generate_responses(self, bot, message):
        reses_list = [module.generate_responses(bot, message)
                      for module in self._mods]
        return sum(reses_list, [])

    def show_mods(self):
        logging.info("using mods:\n{}".format(
            "\n".join("    - {}".format(str(mod)) for mod in self._mods)
        ))
