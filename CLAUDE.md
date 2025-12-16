# CLAUDE.md

## German Dictionary App

This project creates a German dictionary app in IOS and Android.
The app looks like "德语助手Dehelper德语词典翻译工具". 
It translates German words to Chinese, and vice versus.

## Coding Style

The app will run in both IOS and Android. 
Therefore, you need to consider reusability of code. 
As a first step, consider only running the code in IOS.

When you write code, make the code organized, maintainable, and clean.

When you change code, try to make minimal code change so that I as a human can understand easier. 

## Features

As the starting point, the app runs fully offline, meaning that we don't consider any remote API call.

### Search
This is the top priority.
This allows user to search a German word for Chinese explanation, or search a Chinese word for German explanation.
It should support auto-completion and fuzzy matching.

#### When a word and its explanation is shown, 
- it shows word and its tranlation, usage, examples, etc
- it also has a button to play the audio
- it should allow user to add it to a notebook so that user can practice in flash cards.

### Flash cards
This is the second priority.
It creates flash cards for users to practice words.

