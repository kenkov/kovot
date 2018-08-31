#! /usr/bin/env python
# coding:utf-8


import logging
from kovot.mod import ModManager


# Kovot
class Bot:
    """対話システム実行クラス"""
    def __init__(self,
                 mods,
                 speaker=None,
                 preprocessor=None,
                 response_selector=None,
                 postprocessor=None):

        self.module_manager = ModManager(mods=mods)

        if not speaker:
            from kovot.speaker import Speaker
            speaker = Speaker(name="bot")

        if not preprocessor:
            from kovot.message import MessageTransformer
            preprocessor = MessageTransformer()

        if not response_selector:
            from kovot.response import ResponseSelector
            response_selector = ResponseSelector()

        if not postprocessor:
            from kovot.response import ResponseTransformer
            postprocessor = ResponseTransformer()

        self.speaker = speaker
        self.response_selector = response_selector
        self.preprocessor = preprocessor
        self.postprocessor = postprocessor

        # debug
        self.module_manager.show_mods()

    def talk(self, message):
        message = self.preprocessor.transform(message)

        # get responses from mods
        responses = self.module_manager.get_responses(self, message)

        # select responses by Selector
        selected_resposes = self.response_selector.select(responses,
                                                          num=10)
        postprocessed_reponses = [self.postprocessor.transform(res)
                                  for res in selected_resposes]

        # log
        logging.info("### answer candidates ###")
        for response in postprocessed_reponses:
            logging.info(f"[{response.source}] "
                         f"{response.score:.4} "
                         f"{response.text}")
        logging.info("########################")

        # choose the best response
        res = postprocessed_reponses[0]

        return res

    def run(self, stream):

        for message in stream:
            res = self.talk(message)
            stream.post(res)
