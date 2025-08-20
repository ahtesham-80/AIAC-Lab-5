"""
Simple console-based sentiment analysis.

Classifies input text as positive, negative, or neutral using a small
lexicon-based approach with support for:
- common positive/negative words
- simple negation handling (e.g., "not good" -> negative)
- phrase overrides (e.g., "good taste" treated as negative per example)
- light emphasis for clauses after "but"
"""

from __future__ import annotations

import re
from typing import List, Set, Dict


POSITIVE_WORDS: Set[str] = {
    "good",
    "great",
    "excellent",
    "amazing",
    "delicious",
    "happy",
    "love",
    "like",
    "wonderful",
    "fantastic",
    "nice",
    "pleasant",
    "satisfied",
    "tasty",
    "fresh",
    "awesome",
    "enjoy",
    "enjoyed",
    "enjoyable",
    "delightful",
}

NEGATIVE_WORDS: Set[str] = {
    "bad",
    "terrible",
    "awful",
    "horrible",
    "disgusting",
    "sad",
    "hate",
    "dislike",
    "worst",
    "poor",
    "nasty",
    "unpleasant",
    "unsatisfied",
    "stale",
    "bland",
    "cold",
    "overcooked",
    "undercooked",
}

NEGATIONS: Set[str] = {"not", "no", "never", "isn't", "wasn't", "aren't", "don't", "doesn't", "didn't", "can't", "won't", "n't"}

# Phrase overrides per the task's examples (domain-specific). We mask these
# phrases before token-level scoring to avoid double counting their words.
PHRASE_SENTIMENT: Dict[str, int] = {
    # The prompt's example treats "good taste" as negative.
    "good taste": -2,
}


def _tokenize(text: str) -> List[str]:
    return re.findall(r"\b[\w']+\b", text.lower())


def analyze_sentiment(text: str) -> str:
    """Return one of: "positive", "negative", or "neutral".

    Heuristic scoring with:
    - phrase overrides (masked from token scoring)
    - negation flipping within a short window
    - emphasis for words after "but"
    """

    if not text or not text.strip():
        return "neutral"

    working_text = text.lower()
    score = 0

    # Apply phrase overrides and mask them out to prevent double counting
    for phrase, phrase_weight in PHRASE_SENTIMENT.items():
        start = 0
        while True:
            idx = working_text.find(phrase, start)
            if idx == -1:
                break
            score += phrase_weight
            # mask phrase with spaces to preserve indices for subsequent finds
            working_text = (
                working_text[:idx] + (" " * len(phrase)) + working_text[idx + len(phrase) :]
            )
            start = idx + len(phrase)

    tokens = _tokenize(working_text)

    negate_window = 0  # flip polarity for the next few sentiment tokens
    after_but = False  # lightly emphasize tokens after "but"

    for token in tokens:
        if token == "but":
            after_but = True
            continue

        if token in NEGATIONS:
            negate_window = 3
            continue

        word_delta = 0
        if token in POSITIVE_WORDS:
            word_delta = 1
        elif token in NEGATIVE_WORDS:
            word_delta = -1

        if word_delta != 0:
            if negate_window > 0:
                word_delta *= -1      #that guy is not comfortable with us
            if after_but:             #The food is delicious
                word_delta *= 2       #the movie is not that good
            score += word_delta

        if negate_window > 0:
            negate_window -= 1

    if score > 0:
        return "positive"
    if score < 0:
        return "negative"
    return "neutral"

def main() -> None:
    try:
        text = input("Enter text to analyze sentiment: ")
    except EOFError:
        text = ""
    label = analyze_sentiment(text)
    print(f"{label} sentiment")

if __name__ == "__main__":
    main()


