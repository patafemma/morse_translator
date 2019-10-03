# Python Morse Translator

## Description

Python Morse Translator is a simple python package for translating English
strings into morse code and vice versa. It can be used either as a dependency
or run as a standalone command line tool.

## Requirements

The project requires Python 3.2 or later and has no external dependencies. If
you want to run the test suite, you will need to install pytest which is the
testing framework used.

## Usage

You can import the package and use the translator as simply as:

```
>>> from morse_translator import get_translator
>>> english_to_morse = get_translator("english", "morse")
>>> english_to_morse.translate("Hello World")
'****.*.*-**.*-**.---/*--.---.*-*.*-**.-**'
```

Running the package as a commad line tool is also simple:

```
python -m morse_translator [-t TARGET_LANG] [-s SOURCE_LANG] output_file input_file
```

So if you have a file `english.txt`, running the command
`python -m morse_translator morse.txt english.txt`
will produce a file `morse.txt` containing the translated contents of the original
file.

## Testing

The project contains rudimentary test suite which can be run with command `pytest`
if you have pytest installed.
