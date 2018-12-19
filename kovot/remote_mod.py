#! /usr/bin/env python
# coding:utf-8


import requests
import logging
from kovot.response import Response


class RemoteCallerMod:
    def __init__(self, server, port):
        self._root_url = "http://{}:{}".format(server, port)

    def generate_responses(self, bot, message):
        url = "{}/api/generate_responses".format(self._root_url)
        logging.debug("{} requests to {}".format(self.__class__.__name__, url))
        json = {"message": message.dict()}
        res = requests.post(url=url, json=json)
        return [Response.from_dict(res_)
                for res_ in res.json()["responses"]]