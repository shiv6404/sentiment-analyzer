"""
AI-Based Sentiment Analyzer
----------------------------
A lexicon-based sentiment scoring engine for analyzing text such as
product reviews or social media posts. Classifies text as
Positive / Negative / Neutral and produces a confidence score.

No external API or internet connection required — works fully offline,
which makes it easy to demo and submit.
"""

import re
import string

# ---------------------------------------------------------------------
# Sentiment lexicons (word : weight). Larger absolute value = stronger.
# ---------------------------------------------------------------------
POSITIVE_WORDS = {
    "good": 2, "great": 3, "excellent": 3, "amazing": 3, "awesome": 3,
    "love": 3, "loved": 3, "like": 1, "liked": 1, "best": 3, "fantastic": 3,
    "perfect": 3, "happy": 2, "wonderful": 3, "nice": 2, "fast": 1,
    "recommend": 2, "recommended": 2, "satisfied": 2, "superb": 3,
    "comfortable": 2, "smooth": 2, "reliable": 2, "affordable": 1,
    "beautiful": 2, "impressive": 2, "easy": 1, "efficient": 2,
    "helpful": 2, "friendly": 2, "quality": 1, "worth": 1, "delight": 2,
    "delighted": 2, "exceeded": 2, "premium": 1, "value": 1, "elegant": 2,
}

NEGATIVE_WORDS = {
    "bad": 2, "terrible": 3, "awful": 3, "horrible": 3, "worst": 3,
    "hate": 3, "hated": 3, "dislike": 2, "poor": 2, "disappointing": 2,
    "disappointed": 2, "slow": 1, "broken": 2, "waste": 2, "useless": 2,
    "annoying": 2, "uncomfortable": 2, "defective": 2, "cheap": 1,
    "overpriced": 2, "rude": 2, "delay": 1, "delayed": 1, "issue": 1,
    "issues": 1, "problem": 2, "problems": 2, "faulty": 2, "fail": 2,
    "failed": 2, "regret": 2, "junk": 2, "scam": 3, "damaged": 2,
}

NEGATIONS = {"not", "no", "never", "n't", "cannot", "can't", "won't", "didn't", "doesn't"}

INTENSIFIERS = {"very": 1.5, "extremely": 2.0, "really": 1.4, "so": 1.3, "too": 1.3}


def _tokenize(text: str):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation.replace("'", "")))
    return text.split()


def analyze_sentiment(text: str) -> dict:
    """
    Analyze a single piece of text and return a dict with:
    - label: 'Positive' | 'Negative' | 'Neutral'
    - score: float (raw weighted score)
    - confidence: float 0-1 (normalized strength)
    - positive_hits / negative_hits: matched words
    """
    tokens = _tokenize(text)
    score = 0.0
    pos_hits, neg_hits = [], []

    i = 0
    while i < len(tokens):
        word = tokens[i]
        multiplier = 1.0

        # check for intensifier just before this word
        if i > 0 and tokens[i - 1] in INTENSIFIERS:
            multiplier *= INTENSIFIERS[tokens[i - 1]]

        # check for negation within previous 2 words
        negated = any(t in NEGATIONS for t in tokens[max(0, i - 2):i])

        if word in POSITIVE_WORDS:
            weight = POSITIVE_WORDS[word] * multiplier
            if negated:
                score -= weight
                neg_hits.append(word + " (negated)")
            else:
                score += weight
                pos_hits.append(word)
        elif word in NEGATIVE_WORDS:
            weight = NEGATIVE_WORDS[word] * multiplier
            if negated:
                score += weight
                pos_hits.append(word + " (negated)")
            else:
                score -= weight
                neg_hits.append(word)
        i += 1

    if score > 0.5:
        label = "Positive"
    elif score < -0.5:
        label = "Negative"
    else:
        label = "Neutral"

    confidence = min(1.0, abs(score) / 10.0)

    return {
        "text": text,
        "label": label,
        "score": round(score, 2),
        "confidence": round(confidence, 2),
        "positive_hits": pos_hits,
        "negative_hits": neg_hits,
    }


def analyze_batch(texts):
    """Analyze a list of texts, return list of results + summary counts."""
    results = [analyze_sentiment(t) for t in texts]
    summary = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for r in results:
        summary[r["label"]] += 1
    return results, summary


if __name__ == "__main__":
    sample_reviews = [
        "The product quality is amazing, I love it!",
        "Terrible experience, the item arrived damaged and support was rude.",
        "It's okay, does the job but nothing special.",
        "Not bad at all, actually quite impressive for the price.",
        "Worst purchase ever, complete waste of money.",
    ]
    results, summary = analyze_batch(sample_reviews)
    for r in results:
        print(f"[{r['label']:8}] ({r['confidence']:.2f}) {r['text']}")
    print("\nSummary:", summary)
