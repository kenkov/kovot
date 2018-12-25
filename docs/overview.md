# Overview

Kovot は大きく3つのクラスからできています。

1. Bot
1. Mod
1. Stream

`Bot` は、Kovotのエントリポイントとなるクラスです。
`Bot.talk` メソッドに発話を `Message` オブジェクトとして入力すると、
応答として `Response` オブジェクトが返ります。

`Mod` は、応答を生成するクラスです。
`Bot` 内部では、`Message` オブジェクトを `Mod.generate_responses` メソッドに渡すことで
`Response` を生成します。
Kovotでのチャットボット作成は `Mod` クラスを実装することになります。

最後に `Stream` は、入出力の対象を表すクラスです。
例えば `StdIO` は標準入力から発話を受け取り、標準出力に応答を出力します。
`Stream` として Twitter や Slack を使うことで、簡単にそれらの上で動作する
チャットボットを作成できます。
