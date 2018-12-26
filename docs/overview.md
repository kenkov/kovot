# Overview

Kovot consists of three classes as follows;

1. Bot
1. Mod
1. Stream

First, the class `Bot` provides an entry point to Kovot.
`Bot.talk` requires `Message` object as an input utterance,
then it returns `Response` object as a response utterance.

Second, `Mod` is a class for response generation.
In a `Bot` object, it passes `Message` object to `Mod.generate_responses` method to generate responses.
You implement `Mod` classes to build your chatbot in Kovot.

At last, `Stream` is a class to get input utterance ans post a response from services outside.
`StdIO`, for example, gets an input utterance from stdin, and outputs a response to stdout.
In addition to `StdIO`, Kovot provides several `Stream` classes to work with general services like Slack.
