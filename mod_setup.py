#! /usr/bin/env python
# coding:utf-8

import os
import sys
from logging import getLogger


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
        logger.info("add PYTHONPATH: {}".format(mod_path))
