"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies.

    Returns:
        A float. Decide yourself what scale it's on and which direction means
        "more human" — then write that down, because your combining rule
        depends on knowing it.

    A hint on what you're reaching for: the standard deviation of sentence
    lengths, probably divided by the mean so a long text and a short one are
    comparable. `statistics.stdev` is imported for you.

    Watch the edge case: a one-sentence submission has no spread at all, and
    `stdev` raises on fewer than two values. Decide what that should return
    before the attack set decides for you.
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    # One sentence has no spread to measure. 0.0 means "no evidence of
    # variation", which style_signal reads as AI-leaning, so it gets damped
    # there by the short-text pull toward 0.5.
    if len(lengths) < 2:
        return 0.0
    mean = statistics.mean(lengths)
    # Coefficient of variation: stdev / mean. Higher = lumpier = more human.
    return round(statistics.stdev(lengths) / mean, 4)


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words.

    Returns:
        A float between 0 and 1. Higher means more varied vocabulary.

    Worth knowing before you rely on it: this measure falls as text gets
    longer, because common words repeat. Two texts of different lengths aren't
    directly comparable on it, and if your test inputs vary a lot in length,
    that alone can look like a signal.
    """
    toks = words(text)
    if not toks:
        return 0.0
    # Only the first 150 words count, so long and short texts are compared on
    # the same footing (the ratio falls as text grows).
    toks = toks[:150]
    return round(len(set(toks)) / len(toks), 4)


def punctuation_density(text: str) -> float:
    """
    How much punctuation, relative to length.

    Returns:
        A float. Whether you count all punctuation or only some kinds — commas,
        semicolons, dashes — is a real choice. Semicolons and em dashes are
        more interesting than full stops, because they vary more between
        writers.
    """
    toks = words(text)
    if not toks:
        return 0.0
    # Full stops are left out on purpose — every writer uses them. These are
    # the marks that vary between writers: commas, semicolons, colons, dashes,
    # brackets, quotes, question and exclamation marks, ellipses.
    marks = re.findall(r"[,;:()\"!?—–…]|--|-(?=\s)|\.\.\.", text)
    # Per 100 words. Higher = more varied punctuation = more human.
    return round(100 * len(marks) / len(toks), 4)


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.**

    Combine your three measures into one number. Same direction as
    `detector.model_signal`, so that `scoring.combine_signals` can treat them
    the same way — if one of your signals runs backwards, everything above it
    is wrong in a way that's hard to see.

    Two things to decide and write down:

      1. Which direction each measure points. Low spread means more AI-ish, so
         it needs flipping. Work out which of your three need that.
      2. How to get each onto a comparable scale. A raw type-token ratio sits
         between 0 and 1; a raw punctuation count doesn't. Adding them
         unscaled means whichever has the bigger numbers wins by default.

    Test it on the four calibration inputs from Milestone 4 — clearly AI,
    clearly human, plain conventional human writing, lightly-edited AI — before
    you trust it. Plain and ordinary, not formal: formal prose reads as *human*
    to signal one, and it is plain writing that gets accused.
    """
    n_words = len(words(text))
    if n_words == 0:
        return 0.5

    # Each measure becomes a 0–1 "human-ness" by clamping between a floor
    # (reads AI) and a ceiling (reads human). The ranges come from running the
    # calibration inputs — see README, Signals and Scoring.
    def scale(value, low, high):
        return min(max((value - low) / (high - low), 0.0), 1.0)

    spread = scale(sentence_length_spread(text), 0.20, 0.70)
    variety = scale(type_token_ratio(text), 0.55, 0.80)
    punct = scale(punctuation_density(text), 4.0, 14.0)

    # Spread counts most: it's the measure least affected by topic.
    human_ness = 0.45 * spread + 0.30 * variety + 0.25 * punct
    score = 1.0 - human_ness

    # Short text doesn't give these measures enough to work with, so under 60
    # words the score is pulled toward 0.5 ("can't tell") in proportion.
    confidence = min(n_words / 60, 1.0)
    score = 0.5 + (score - 0.5) * confidence
    return round(score, 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
