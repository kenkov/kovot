#! /usr/bin/env python
# coding:utf-8


class ClassInitReplMixin:
    """クラス初期化の書式でオブジェクトを表示する Mixin"""
    def __repr__(self):
        attrs = self.__dict__
        clsname = self.__class__.__name__

        fmt = "{clsname}({attrs_str})"
        attrs_str = ", ".join("{}={}".format(key, val)
                              for key, val in attrs.items()
                              if val)

        return fmt.format(clsname=clsname, attrs_str=attrs_str)


class ClassAttrEqMixin:
    """全てのクラス属性が一致している時等しいとする Mixin"""
    def __eq__(self, other):
        return all(getattr(other, key) == val
                   for key, val in self.__dict__.items())


def dict(dic):
    """
    Args:
        dic (dict): 辞書型のオブジェクト
    """
    def _dict(obj):
        if not obj:
            return obj
        if hasattr(obj, "dict"):
            return obj.dict()
        return obj
    return {key: _dict(val) for key, val in dic.items()}
