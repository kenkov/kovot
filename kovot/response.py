#! /usr/bin/env python
# coding:utf-8


from kovot.util import ClassInitReplMixin
from kovot.util import ClassAttrEqMixin
from kovot.speaker import Speaker


class Response(ClassInitReplMixin, ClassAttrEqMixin):
    def __init__(self,
                 text,
                 score,
                 id_=None,
                 speaker=None,
                 message=None,
                 source=None):
        self.text = text
        self.score = score
        self.id_ = id_
        self.speaker = speaker
        self.message = message
        self.source = source

    @classmethod
    def from_dict(cls, dic):
        # convert to Speaker and Message object from dictionary
        if "speaker" in dic and dic["speaker"]:
            speaker = Speaker.from_dict(dic["speaker"])
        else:
            speaker = None
        if "message" in dic and dic["message"]:
            message = Speaker.from_dict(dic["message"])
        else:
            message = None

        return cls(text=dic["text"],
                   score=dic["score"],
                   id_=dic.get("id_"),
                   speaker=speaker,
                   message=message,
                   source=dic.get("source"))


class ResponseTransformer:
    def transform(self, response):
        return response


class ResponseSelector:
    """もっとも適切なレスポンスを選択するクラス"""
    def select(self, responses, num=None):
        """レスポンスのうち、スコアが大きい方からデフォルトで 10 個を返す。
        Args:
            responses (List[Response]):
            num (int): レスポンスの数

        Returns (Response):
        """
        score_descending_reses = list(sorted(responses,
                                             key=lambda res: res.score,
                                             reverse=True))
        selected_reses = score_descending_reses
        if num:
            selected_reses = score_descending_reses[:num]
        return selected_reses
