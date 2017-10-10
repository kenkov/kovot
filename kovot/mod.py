#! /usr/bin/env python
# coding:utf-8


import os
import sys
from logging import getLogger
import abc


def setup_path(
    mod_dir: str="mod",
    logger=None
):
    logger = logger or getLogger(__name__)
    for mod in os.listdir(mod_dir):
        mod_path = os.path.abspath(
            os.path.join(mod_dir, mod)
        )
        sys.path = [mod_path] + sys.path
        logger.debug("add PYTHONPATH: {}".format(mod_path))


class Mod(metaclass=abc.ABCMeta):
    """
    message の形式
    message:
        "id"
        "text"
        "user":
            "name"
            "screen_name"

    master の形式
    master:
        "name"
        "screen_name"
    """
    def __init__(
        self,
        logger=None,
    ):
        self.logger = logger if logger else getLogger(__file__)

    def can_utter(
        self,
        message: dict,
        master: dict
    ) -> bool:
        """
        発話が必要かどうか判定する
        """
        return True

    @abc.abstractmethod
    def utter(
        self,
        message: dict,
        maste: dict
    ) -> [(float, str, str, dict)]:
        """
        発話情報を返す

        return:
            [(確率, 発話内容, Mod 名, 追加情報の辞書)]
        """
        pass

    def __str__(self):
        return self.__class__.__name__
