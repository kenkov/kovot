==============================
Kovot
==============================

Python 製の bot フレームワークです。

Mod とよばれるモジュールを追加することによって
カスタマイズすることができます。

`@kovroid <https://twitter.com/kovroid>`_ はこのモジュールを使って
作成されています。

インストール
===============

あらかじめ次をインストールしてください。

*   https://github.com/kenkov/chartype

Kovot をはじめる
=================

``test.py`` はオウム返しする Kovot プログラムです。
まずはこれを実行してみましょう。

.. code-block:: bash

    $ python test.py
    2015-02-25 23:19:43,350 - kovot.py - INFO - using mods:
        - ModEcho
        - ModDefault
        - ModLogger

Kovot は **Mod** というクラスを継承したクラスにより
拡張が可能です。デフォルトでは、上に表示されている

*   ModEcho
*   ModDefault
*   ModLogger

がインストールされています。

``test.py`` は標準入力から文字列を読みこみ、返答をします。例えば「こんばんは」
と入力すると

.. code-block:: bash

    こんばんは
    2015-02-25 23:22:56,563 - __main__ - INFO - [ModLogger] @your_screen_name: こんばんは
    2015-02-25 23:22:56,563 - kovot.py - INFO - ### aswer candidates ###
    2015-02-25 23:22:56,563 - kovot.py - INFO - [echo] 1.0 こんばんは
    2015-02-25 23:22:56,563 - kovot.py - INFO - [default] 0.1221 今日の天気はどうですか？
    2015-02-25 23:22:56,563 - kovot.py - INFO - [default] 0.07895 こんにちは。
    2015-02-25 23:22:56,563 - kovot.py - INFO - [default] 0.06836 お元気ですか？
    2015-02-25 23:22:56,563 - kovot.py - INFO - ########################
    こんばんは

このように「こんばんは」とオウム返しします。

ログに表示されている情報は、返答候補のうちの上位にきているものです。
Kovot では、 ``Mod`` が複数の返答を確率付きで生成し、最も確率が高いものを
最終的な返答として選びます。

Mod を作成する
================

ここでは ``Mod`` の作り方を説明します。例として ``mod/echo/echo.py`` を見てみましょう。

.. code-block:: python


    from mod import Mod


    class ModEcho(Mod):
        def reses(self, message, master) -> [(float, str, str, dict)]:
            return [
                (1.0, message["text"], "echo", dict())
            ]

        def is_fire(self, message, master):
            return True


``message`` は

::

    {"id": 0,
     "text": "こんにちは",
     "user": {
         "name": "けんこふ",
         "screen_name", :"kenkov"
         }
    }

という辞書になっています。``is_fire`` でこのモジュールから返答を生成するかどうか
を真偽値で返します。``ModEcho`` は常に返答を生成するので、この場合は ``True`` を
返しています。

``reses`` で返答のリストを返します。返答は

::

    (確率, 返答文, モジュール名, 追加情報)

の形です。

Mod をストリームに追加する
=============================


ストリームを使い分ける
=========================
