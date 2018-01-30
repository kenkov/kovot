#! /usr/bin/env python
# coding:utf-8


if __name__ == "__main__":
    from logging import getLogger, basicConfig, INFO, DEBUG
    import argparse
    from kovot.kovot import Kovot
    from kovot.kovot import Preprocessor
    from kovot.kovot import Postprocessor
    from kovot.kovot import ResponseSelector
    from kovot.kovot import ModuleManager
    from kovot.message import User
    from kovot.mod.echo.echo import EchoMod
    from kovot.mod.default.default import DefaultMod
    from kovot.stream.stdin import Stdin

    # parse arg
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="show DEBUG log"
    )
    args = parser.parse_args()

    # logger
    logger = getLogger(__name__)
    basicConfig(
        level=DEBUG if args.verbose else INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )

    # mods
    mods = [EchoMod(), DefaultMod()]

    kovot = Kovot(stream=Stdin(),
                  bot=User(name="botname"),
                  module_manager=ModuleManager(mods),
                  response_selector=ResponseSelector(),
                  preprocessor=Preprocessor(),
                  postprocessor=Postprocessor())

    kovot.run()
