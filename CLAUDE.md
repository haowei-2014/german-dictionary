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

## Impmentation architecture

### Project Structure
```
lib/
├── main.dart
├── core/                  # Constants, theme, utils
├── data/
│   ├── datasources/       # SQLite database access
│   ├── models/            # Data models (word, notebook, flashcard)
│   └── repositories/      # Data access layer
├── presentation/
│   ├── screens/           # search, word_detail, notebook, flashcards
│   ├── widgets/           # Reusable UI components
│   └── providers/         # State management
└── services/              # Audio playback service
```

### Database (SQLite with sqflite)
- **dictionary**: german_word, chinese_translation, part_of_speech, gender, plural, usage, examples, audio_path
- **notebooks**: id, name, created_at
- **saved_words**: word_id, notebook_id, added_at
- **flashcard_progress**: word_id, last_reviewed, next_review, ease_factor, repetitions

### Key Packages
- **sqflite** - Local database
- **provider** - State management
- **just_audio** - Audio playback

### Search
- SQLite FTS5 for fuzzy matching and auto-completion
- Bidirectional: German ↔ Chinese

### Flash Cards
- SM-2 spaced repetition algorithm
- Words pulled from user's notebooks
