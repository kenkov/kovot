#! /usr/bin/env python
# coding:utf-8


from logging import getLogger
from selector import Selector
from postprocessing import PostProcessing
import traceback


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
            for module in self.modules
            if module.can_utter(message, self.master)
        ]

        return sum(
            [module.utter(message, self.master) for module in modules],
            []
        )

    def show_modules(self) -> None:
        self.logger.info("using mods:\n{}".format(
            "\n".join("    - {}".format(str(mod)) for mod in self.modules)
        ))

    def run(self, log_file: str=""):
        self.show_modules()

        if log_file:
            try:
                log_fd = open(log_file, "a")
            except:
                traceback.print_exc()
                return
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
                if log_file and post_answers:
                    print("あなた>\t{}".format(message["text"]), file=log_fd)
                    print(
                        "{}>\t{}".format(
                            self.master["name"],
                            post_answers[0][1]
                        ),
                        file=log_fd
                    )

                # post
                self.stream.say(
                    message,
                    post_answers
                )

        # close log file
        if log_file:
            log_fd.close()
