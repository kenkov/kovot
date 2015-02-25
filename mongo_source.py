#! /usr/bin/env python
# coding:utf-8


import pymongo as pm
import preprocessing
import sys
import re
import os


def twitter(
    db: str,
    coll: str,
    target: str,
    logger,
    target_dir: str="source",
    sfilter: dict={},
    delimiter: str=",",
    limit: int=0,
    verbose: bool=True,
    host: str="localhost",
    port: int=27017,
):

    # mongo
    client = pm.MongoClient(host, port)
    colld = client[db][coll]

    # converter
    # do
    #   self.remove_newline,
    #   self.remove_link,
    #   self.convert_cont_spaces,
    #   self.strip
    convert = preprocessing.Preprocess()

    text_file = os.path.join(
        target_dir,
        "{}.txt".format(target)
    )
    conv_file = os.path.join(
        target_dir,
        "{}.conv.txt".format(target)
    )

    #
    # text
    textd = open(text_file, "a")
    text_count = 0

    for i, tweet in enumerate(colld.find(
            {"text": {"$exists": True}},
            timeout=False,
            limit=limit
    )):
        text = convert.execute(tweet["text"])
        if text:
            print(text, file=textd)
            text_count += 1
        if (i + 1) % 10000 == 0:
            logger.debug("text extracted: {}".format(i+1))
    textd.close()
    logger.info(
        "{}/{} texts extracted in {}".format(text_count, i+1, text_file)
    )

    #
    # conversation
    #
    convd = open(conv_file, "a")
    conv_count = 0

    flt = {"text": {"$exists": True},
           "in_reply_to_status_id": {"$ne": None}
           }
    flt.update(sfilter)

    # delimiter regex
    re_del = re.compile(r"{}".format(delimiter))

    for i, tweet in enumerate(colld.find(
            flt,
            limit=limit
    )):
        try:
            origtw = colld.find_one({
                "text": {"$exists": True},
                "id": tweet["in_reply_to_status_id"]})
            if origtw:
                orig = convert.execute(origtw["text"])
                reply = convert.execute(tweet["text"])
                # Output to files
                if orig and reply and \
                        (not re_del.search(orig)) and \
                        (not re_del.search(reply)):
                    print("{}{}{}".format(orig, delimiter, reply), file=convd)
                    conv_count += 1
        except KeyboardInterrupt:
            sys.exit(1)
        except:
            logger.exception("error raised while extraction conversation")
        if (i + 1) % 10000 == 0:
            logger.debug("conv extracted: {}".format(i+1))
    convd.close()
    logger.info(
        "{}/{} conversations extracted in {}".format(
            conv_count, i+1, conv_file
        )
    )


if __name__ == '__main__':
    from logging import getLogger, basicConfig, DEBUG, INFO
    import argparse

    # parse arg
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "db",
        type=str,
        help="database name"
    )
    parser.add_argument(
        "coll",
        type=str,
        help="collection name"
    )
    parser.add_argument(
        "target",
        type=str,
        help="target name"
    )
    parser.add_argument(
        "-t", "--target-dir",
        type=str,
        nargs="?",
        default="source",
        help="target name"
    )
    parser.add_argument(
        "-d", "--delimiter",
        type=str,
        nargs="?",
        default=",",
        help="target name"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="show DEBUG log"
    )
    parser.add_argument(
        "-l", "--limit",
        type=int,
        nargs="?",
        default=0,
        help="the number of extracted documents"
    )
    args = parser.parse_args()

    # log
    logger = getLogger(__name__)
    basicConfig(
        level=DEBUG if args.verbose else INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )

    # args
    db = args.db
    coll = args.coll
    target = args.target
    target_dir = args.target_dir
    delimiter = args.delimiter
    limit = args.limit

    logger.info("processing coll {}".format(coll))
    twitter(
        db=db,
        coll=coll,
        target=target,
        logger=logger,
        target_dir=target_dir,
        sfilter={"user.screen_name": "kenkov"},
        delimiter=delimiter,
        limit=limit,
    )
