#! /usr/bin/env python
# coding:utf-8


import requests
import logging
from kovot.response import Response


class RemoteCallerMod:
    def __init__(self, server, port, endpoint):
        self._url = "http://{}:{}{}".format(server, port, endpoint)

    def generate_responses(self, bot, message):
        url = self._url
        logging.debug("{} requests to {}".format(self.__class__.__name__, url))
        json = {"message": message.dict(),
                "bot": dict()
                }
        res = requests.post(url=url, json=json)
        return [Response.from_dict(res_)
                for res_ in res.json()["responses"]]
