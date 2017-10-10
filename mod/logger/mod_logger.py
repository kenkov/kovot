#! /usr/bin/env python
# coding:utf-8

from kovot.mod import Mod


class ModLogger(Mod):
    """
    ツイートをチェックしてログとして出力する
    """
    def __init__(
        self,
        logger=None,
    ):
        Mod.__init__(self, logger)

    def can_utter(self, message, master) -> bool:
        self.logger.info(
            "[ModLogger] @{}: {}".format(
                message["user"]["screen_name"],
                message["text"][:20]
            )
        )
        return False

    def utter(self, message, master):
        return []
