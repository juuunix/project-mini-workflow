"""Tokenizers under comparison. Each maps text to a list of string tokens."""

import re
from collections.abc import Callable
from functools import cache

from kiwipiepy import Kiwi

Tokenizer = Callable[[str], list[str]]

_WORD = re.compile(r"[0-9A-Za-z가-힣]+")

# Kiwi tags kept by the content-only tokenizer: nouns, verbs, adjectives, roots,
# foreign words, numbers, and hanja.
_CONTENT_TAGS = ("NNG", "NNP", "VV", "VA", "XR", "SL", "SN", "SH")


def words(text: str) -> list[str]:
    return _WORD.findall(text.lower())


def bigrams(text: str) -> list[str]:
    tokens: list[str] = []
    for word in words(text):
        if len(word) == 1:
            tokens.append(word)
        else:
            tokens.extend(word[i : i + 2] for i in range(len(word) - 1))
    return tokens


@cache
def _kiwi() -> Kiwi:
    return Kiwi()


def _morphemes(text: str, keep: Callable[[str], bool]) -> list[str]:
    return [
        token.form.lower()
        for token in _kiwi().tokenize(text)
        if keep(token.tag) and _WORD.fullmatch(token.form)
    ]


def kiwi_all(text: str) -> list[str]:
    return _morphemes(text, lambda tag: True)


def kiwi_content(text: str) -> list[str]:
    return _morphemes(text, lambda tag: tag.startswith(_CONTENT_TAGS))


TOKENIZERS: dict[str, Tokenizer] = {
    "words": words,
    "bigrams": bigrams,
    "kiwi-all": kiwi_all,
    "kiwi-content": kiwi_content,
}
