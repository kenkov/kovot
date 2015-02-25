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
    """
    def __init__(
        self,
        logger=None,
    ):
        self.logger = logger if logger else getLogger(__file__)

    def is_fire(self, message, master):
        return True

    @abc.abstractmethod
    def reses(self, message, master):
        pass

    def __str__(self):
        return self.__class__.__name__
