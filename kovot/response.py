#! /usr/bin/env python
# coding:utf-8


from kovot.util import ClassInitReplMixin
from kovot.util import ClassAttrEqMixin


class Response(ClassInitReplMixin, ClassAttrEqMixin):
    def __init__(self,
                 text,
                 score,
                 id_=None,
                 user=None,
                 message=None,
                 source=None):
        self.text = text
        self.score = score
        self.id_ = id_
        self.user = user
        self.message = message
        self.source = source


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
