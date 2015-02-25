#! /usr/bin/env python
# coding:utf-8


from logging import getLogger
from selector import Selector
from postprocessing import PostProcessing


class Kovot:

    def __init__(
        self,
        stream,
        master,
        selector=Selector(),
        postprocessing=PostProcessing(),
        logger=None
    ):
        self.stream = stream
        self.master = master
        self.selector = selector
        self.postprocessing = postprocessing

        self.logger = logger if logger else getLogger(__file__)
        self.modules = []

    def is_message(self, message):
        """
        Check essage format:
            "id"
            "text"
            "user":
                "name"
                "screen_name"

        将来的には "type" もいれる
        """
        return (
            "text" in message and
            "user" in message and
            "id" in message and
            "name" in message["user"] and
            "screen_name" in message["user"]
        )

    def add_module(self, module):
        self.modules.append(module)

    def answers(self, message):
        modules = [
            module
            for module in self.modules if module.is_fire(message, self.master)
        ]

        return sum(
            [module.reses(message, self.master) for module in modules],
            []
        )

    def show_modules(self) -> None:
        self.logger.info("using mods:\n{}".format(
            "\n".join("    - {}".format(str(mod)) for mod in self.modules)
        ))

    def run(self):
        self.show_modules()
        for message in self.stream:
            if not self.is_message(message):
                continue
            else:
                # get answers from modules
                answers = self.answers(message)

                # select answers by using a Selector instance
                post_answers = [
                    self.postprocessing.convert(message, answer, self.master)
                    for answer in self.selector.select(answers, num=10)
                ]

                # log
                if post_answers:
                    self.logger.info("### aswer candidates ###")
                    for prob, text, source, info in post_answers:
                        self.logger.info(
                            "[{}] {:.4} {}".format(source, prob, text)
                        )
                    self.logger.info("########################")

                # post
                self.stream.say(
                    message,
                    post_answers
                )
