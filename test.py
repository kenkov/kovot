#! /usr/bin/env python
# coding:utf-8


if __name__ == "__main__":
    from logging import getLogger, basicConfig, INFO, DEBUG
    import argparse

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

    # setup path
    from mod import setup_path
    setup_path(
        mod_dir="mod",
        logger=logger
    )

    # setup kovot
    import stream
    from kovot import Kovot

    master = {
        "name": "botの名前",
        "screen_name": "bots_screen_name",
    }
    kovot = Kovot(
        stream.Stdin(
            "あなたの名前",
            "your_screen_name",
            logger
        ),
        master,
    )

    # echo mod
    from mod_echo import ModEcho
    m_echo = ModEcho()
    kovot.add_module(m_echo)

    # default mod
    from mod_default import ModDefault
    m_default = ModDefault()
    kovot.add_module(m_default)

    # logger mod
    from mod_logger import ModLogger
    m_logger = ModLogger(logger)
    kovot.add_module(m_logger)

    kovot.run()
