#! /usr/bin/env python
# coding:utf-8


import logging


class Preprocessor:
    def process(self, message):
        """
        Args:
            message (Message):
        """
        return message


class Postprocessor:
    def process(self, response):
        """
        Args:
            message (Response):
        """
        return response


class ResponseSelector:
    """もっとも適切なレスポンスを選択するクラス"""
    def select(self, responses, num=10):
        """レスポンスのうち、スコアが大きい方からデフォルトで 10 個を返す。
        Args:
            responses (List[Response]):
            num (int): レスポンスの数

        Returns (Response):
        """
        score_descending_reses = list(sorted(responses,
                                             key=lambda res: res.score,
                                             reverse=True))
        selected_reses = score_descending_reses[:num]
        return selected_reses


class ModuleManager:
    def __init__(self, mods):
        """
        Args:
            modules (List[Mod]): モジュールのリスト
        """
        self._mods = mods

    def get_responses(self, message):
        mods_available = [mod for mod in self._mods
                          if mod.is_available(message)]

        return sum([module.get_responses(message)
                   for module in mods_available],
                   [])

    def show_modules(self):
        logging.info("using mods:\n{}".format(
            "\n".join("    - {}".format(str(mod)) for mod in self._mods)
        ))


# Kovot
class Kovot:
    """対話システム実行クラス"""
    def __init__(self,
                 stream,
                 bot,
                 module_manager,
                 response_selector,
                 preprocessor,
                 postprocessor):
        self.stream = stream
        self.bot = bot
        self.module_manager = module_manager
        self.response_selector = response_selector
        self.preprocessor = preprocessor
        self.postprocessor = postprocessor

    def run(self):
        self.module_manager.show_modules()

        for message in self.stream:
            # preprocessing
            message = self.preprocessor.process(message)

            # get responses from mods
            responses = self.module_manager.get_responses(message)

            # select responses by Selector
            selected_resposes = self.response_selector.select(responses,
                                                              num=10)
            postprocessed_reponses = [self.postprocessor.process(res)
                                      for res in selected_resposes]

            # log
            logging.info("### aswer candidates ###")
            for response in postprocessed_reponses:
                logging.info(f"[{response.source}] "
                             f"{response.score:.4} "
                             f"{response.text}")
            logging.info("########################")

            # post
            res = postprocessed_reponses[0]
            self.stream.post(res)
